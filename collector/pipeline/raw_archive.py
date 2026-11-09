from __future__ import annotations

import hashlib
import json
import logging
import os
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4

import pyarrow as pa
import pyarrow.ipc as ipc
import pyarrow.parquet as pq

logger = logging.getLogger(__name__)
SCHEMA = pa.schema([
    ("sequence", pa.int64()),
    ("request_id", pa.string()),
    ("source", pa.string()),
    ("symbol", pa.string()),
    ("broker", pa.string()),
    ("timeframe", pa.string()),
    ("requested_bars", pa.int64()),
    ("received_at", pa.timestamp("us", tz="UTC")),
    ("kind", pa.string()),
    ("payload", pa.large_binary()),
], metadata={b"raw_archive_version": b"1"})
PARQUET_OPTIONS = {
    "compression": "zstd",
    "compression_level": 9,
    "use_dictionary": ["request_id", "source", "symbol", "broker", "timeframe", "kind"],
    "write_page_checksum": True,
}


class RawArchiveError(RuntimeError):
    pass


def _write_new(path: Path, payload: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def _file_hash(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _hash_rows(digest, rows) -> None:
    for row in rows:
        payload = row["payload"]
        metadata = {key: value for key, value in row.items() if key != "payload"}
        metadata["received_at"] = metadata["received_at"].isoformat()
        encoded = json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode()
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)


def verify_archive(run_dir: Path) -> dict:
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    path = run_dir / "data.parquet"
    if _file_hash(path) != manifest["sha256"]:
        raise RawArchiveError(f"Raw archive checksum mismatch: {path}")
    parquet = pq.ParquetFile(path, page_checksum_verification=True)
    if not parquet.schema_arrow.equals(SCHEMA, check_metadata=True):
        raise RawArchiveError(f"Raw archive schema mismatch: {path}")
    digest = hashlib.sha256()
    rows = 0
    for batch in parquet.iter_batches(batch_size=128):
        _hash_rows(digest, batch.to_pylist())
        rows += batch.num_rows
    if rows != manifest["events"] or digest.hexdigest() != manifest["events_sha256"]:
        raise RawArchiveError(f"Raw archive contents mismatch: {path}")
    return manifest


def finalize_archive(run_dir: Path) -> dict:
    """Consolidate durable event fragments, including after a collector crash."""
    if (run_dir / "manifest.json").exists():
        return verify_archive(run_dir)
    metadata = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
    parts = sorted((run_dir / "parts").glob("*.parquet"))
    if not parts:
        raise RawArchiveError(f"No durable raw events in {run_dir}")
    path = run_dir / "data.parquet"
    tmp = run_dir / f"{uuid4().hex}.tmp"
    digest = hashlib.sha256()
    events = 0
    # Bounded batches share compression pages across requests and symbols.
    with tmp.open("xb") as stream:
        with pq.ParquetWriter(stream, SCHEMA, **PARQUET_OPTIONS) as writer:
            pending, pending_bytes = [], 0
            for part in parts:
                table = pq.ParquetFile(part, page_checksum_verification=True).read()
                if not table.schema.equals(SCHEMA, check_metadata=True):
                    raise RawArchiveError(f"Invalid raw fragment schema: {part}")
                _hash_rows(digest, table.to_pylist())
                events += table.num_rows
                pending.append(table)
                pending_bytes += table.nbytes
                if len(pending) >= 256 or pending_bytes >= 16 * 1024 * 1024:
                    writer.write_table(pa.concat_tables(pending))
                    pending, pending_bytes = [], 0
            if pending:
                writer.write_table(pa.concat_tables(pending))
        stream.flush()
        os.fsync(stream.fileno())
    # The run directory is unique; an already sealed archive is never rewritten.
    os.replace(tmp, path)
    manifest = {
        **metadata,
        "events": events,
        "events_sha256": digest.hexdigest(),
        "sha256": _file_hash(path),
        "bytes": path.stat().st_size,
    }
    manifest_tmp = run_dir / f"{uuid4().hex}.tmp"
    _write_new(manifest_tmp, json.dumps(manifest, indent=2).encode())
    os.replace(manifest_tmp, run_dir / "manifest.json")
    verify_archive(run_dir)
    logger.info("Raw archive sealed path=%s events=%s bytes=%s", path, events, manifest["bytes"])
    return manifest


class RawRequest:
    def __init__(self, archive, fields):
        self.archive, self.fields = archive, fields

    def __enter__(self):
        self.archive.record(self.fields, "request", b"")
        return self

    def message(self, raw: str | bytes) -> None:
        self.archive.record(self.fields, "ws_text" if isinstance(raw, str) else "ws_bytes",
                            raw.encode("utf-8") if isinstance(raw, str) else raw)

    def frame(self, frame) -> None:
        if frame is None:
            self.archive.record(self.fields, "frame_none", b"")
            return
        # Arrow IPC preserves original columns, dtypes, index and timezone.
        try:
            table = pa.Table.from_pandas(frame, preserve_index=True)
            sink = pa.BufferOutputStream()
            with ipc.new_stream(sink, table.schema) as writer:
                writer.write_table(table)
            self.archive.record(self.fields, "frame_arrow", sink.getvalue().to_pybytes())
        except RawArchiveError:
            raise
        except Exception as exc:
            self.archive.broken = True
            raise RawArchiveError("Could not preserve original dataframe") from exc

    def __exit__(self, exc_type, exc, traceback):
        if not self.archive.broken:
            self.archive.record(self.fields, "request_end", json.dumps({
                "status": "ok" if exc_type is None else "failed",
                "error_type": exc_type.__name__ if exc_type else None,
            }).encode())


class RawArchive:
    def __init__(self, root: Path, *, config_path: Path):
        now = datetime.now(timezone.utc)
        self.run_id = f"{now:%Y%m%dT%H%M%S%fZ}-{uuid4().hex}"
        self.run_dir = root / "tradingview" / f"{now:%Y-%m-%d}" / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=False)
        (self.run_dir / "parts").mkdir()
        self.sequence, self.requests, self.broken = 0, 0, False
        metadata = {
            "version": 1, "run_id": self.run_id, "created_at": now.isoformat(),
            "github_run_id": os.getenv("GITHUB_RUN_ID"),
            "github_run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
            "git_sha": os.getenv("GITHUB_SHA"),
            "host_timezone": datetime.now().astimezone().tzname(),
            "tvdatafeed_naive_tz_override": os.getenv("TVDATAFEED_NAIVE_TZ"),
        }
        _write_new(self.run_dir / "metadata.json", json.dumps(metadata).encode())
        self.record({}, "config_json", config_path.read_bytes())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.finalize()

    def request(self, *, source: str, symbol: str, broker: str, timeframe: str, requested_bars: int):
        self.requests += 1
        return RawRequest(self, {
            "request_id": f"r{self.requests:06d}", "source": source,
            "symbol": symbol, "broker": broker, "timeframe": timeframe,
            "requested_bars": int(requested_bars),
        })

    def record(self, fields: dict, kind: str, payload: bytes) -> None:
        if self.broken or (self.run_dir / "manifest.json").exists():
            raise RawArchiveError("Raw archive is unavailable or already sealed")
        self.sequence += 1
        event = {
            "sequence": self.sequence, "request_id": "", "source": "tradingview",
            "symbol": "", "broker": "", "timeframe": "", "requested_bars": 0,
            **fields, "received_at": datetime.now(timezone.utc), "kind": kind, "payload": payload,
        }
        tmp = self.run_dir / "parts" / f"{self.sequence:012d}.tmp"
        part = tmp.with_suffix(".parquet")
        try:
            with tmp.open("xb") as stream:
                pq.write_table(pa.Table.from_pylist([event], schema=SCHEMA), stream, **PARQUET_OPTIONS)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(tmp, part)
        except Exception as exc:
            self.broken = True
            raise RawArchiveError(f"Could not preserve raw event in {self.run_dir}") from exc

    def finalize(self) -> dict:
        try:
            return finalize_archive(self.run_dir)
        except Exception as exc:
            raise RawArchiveError(f"Could not seal raw archive: {self.run_dir}") from exc
