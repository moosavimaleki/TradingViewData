import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging
import re

import pandas as pd

logger = logging.getLogger(__name__)

# Project root: <repo>/data_collector/storage/file_storage.py -> <repo>
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class FileStorage:
    """
    CSV chunk storage optimized for incremental sync.

    Layout:
      data/<source>/<broker>/<timeframe>/<symbol>/
        manifest.json
        <symbol>_0.csv.gz
        <symbol>_1.csv.gz
        ...
    """

    def __init__(
        self,
        base_path: Optional[str] = None,
        max_file_size_mb: int = 100,  # kept for compatibility; not used by chunk strategy
        compression: bool = True,
        chunk_size: int = 10_000,
        merge_tail_chunks: int = 2,
    ):
        self.base_path = Path(base_path) if base_path else (PROJECT_ROOT / "data")
        self.max_file_size_bytes = int(max_file_size_mb * 1024 * 1024)
        self.compression = bool(compression)
        self.chunk_size = max(100, int(chunk_size))
        self.merge_tail_chunks = max(1, int(merge_tail_chunks))
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_storage_path(self, symbol: str, timeframe: str, source: str, broker: Optional[str] = None) -> Path:
        if broker and broker != "unknown":
            return self.base_path / source / broker / timeframe / symbol
        return self.base_path / source / timeframe / symbol

    def _chunk_extension(self) -> str:
        return ".csv.gz" if self.compression else ".csv"

    def _chunk_name(self, symbol: str, idx: int) -> str:
        return f"{symbol}_{int(idx)}{self._chunk_extension()}"

    def _manifest_path(self, storage_path: Path) -> Path:
        return storage_path / "manifest.json"

    def _read_manifest(self, storage_path: Path) -> Optional[Dict[str, Any]]:
        manifest_path = self._manifest_path(storage_path)
        if not manifest_path.exists():
            return None
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            if not isinstance(payload, dict):
                return None
            chunks = payload.get("chunks")
            if not isinstance(chunks, list):
                payload["chunks"] = []
            return payload
        except Exception as e:
            logger.warning(f"Failed to read manifest {manifest_path}: {e}")
            return None

    def _write_manifest(self, storage_path: Path, manifest: Dict[str, Any]) -> None:
        manifest_path = self._manifest_path(storage_path)
        tmp_path = manifest_path.with_name(manifest_path.name + ".tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            tmp_path.replace(manifest_path)
        finally:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)

    def _list_chunk_files(self, storage_path: Path, symbol: str) -> List[Path]:
        pattern = re.compile(rf"^{re.escape(symbol)}_(\d+){re.escape(self._chunk_extension())}$")
        files: List[tuple[int, Path]] = []
        if not storage_path.exists():
            return []
        for p in storage_path.iterdir():
            if not p.is_file():
                continue
            m = pattern.match(p.name)
            if not m:
                continue
            files.append((int(m.group(1)), p))
        files.sort(key=lambda x: x[0])
        return [x[1] for x in files]

    def _read_chunk(self, chunk_path: Path) -> pd.DataFrame:
        try:
            compression = "gzip" if chunk_path.suffix == ".gz" else "infer"
            df = pd.read_csv(chunk_path, compression=compression)
            return self._normalize_df(df)
        except Exception as e:
            logger.warning(f"Failed reading chunk {chunk_path}: {e}")
            return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume", "bar_index"])

    def _write_chunk(self, chunk_path: Path, df: pd.DataFrame) -> None:
        out = df.copy()
        out["timestamp"] = out["timestamp"].apply(lambda x: pd.Timestamp(x).isoformat())
        compression = "gzip" if chunk_path.suffix == ".gz" else None
        tmp_path = chunk_path.with_name(chunk_path.name + ".tmp")
        try:
            out.to_csv(tmp_path, index=False, compression=compression)
            tmp_path.replace(chunk_path)
        finally:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)

    def _normalize_df(self, df: Optional[pd.DataFrame]) -> pd.DataFrame:
        if df is None or df.empty:
            return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume", "bar_index"])
        out = df.copy()
        if "timestamp" not in out.columns:
            return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume", "bar_index"])

        out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, format="mixed", errors="coerce")
        out = out.dropna(subset=["timestamp"])

        for col in ["open", "high", "low", "close"]:
            out[col] = pd.to_numeric(out.get(col), errors="coerce")
        out["volume"] = pd.to_numeric(out.get("volume", 0.0), errors="coerce").fillna(0.0)
        out = out.dropna(subset=["open", "high", "low", "close"])

        if "bar_index" not in out.columns:
            out["bar_index"] = out["timestamp"].apply(lambda x: int(pd.Timestamp(x).timestamp()))
        else:
            out["bar_index"] = pd.to_numeric(out["bar_index"], errors="coerce")
            missing = out["bar_index"].isna()
            if missing.any():
                out.loc[missing, "bar_index"] = out.loc[missing, "timestamp"].apply(
                    lambda x: int(pd.Timestamp(x).timestamp())
                )
            out["bar_index"] = out["bar_index"].astype("int64")

        out = out.sort_values("timestamp")
        out = out.drop_duplicates(subset=["timestamp"], keep="last").reset_index(drop=True)
        return out[["timestamp", "open", "high", "low", "close", "volume", "bar_index"]]

    def _to_utc(self, dt: Optional[datetime]) -> Optional[pd.Timestamp]:
        if dt is None:
            return None
        ts = pd.Timestamp(dt)
        if ts.tzinfo is None:
            ts = ts.tz_localize("UTC")
        else:
            ts = ts.tz_convert("UTC")
        return ts

    def _select_tail_entries(self, manifest: Dict[str, Any], storage_path: Path) -> List[Dict[str, Any]]:
        chunks = list(manifest.get("chunks") or [])
        if not chunks:
            return []
        candidate = chunks[-self.merge_tail_chunks :]
        existing = [entry for entry in candidate if (storage_path / str(entry.get("file", ""))).exists()]
        if existing:
            return existing
        # Fallback: try only latest chunk from manifest
        last = chunks[-1]
        if (storage_path / str(last.get("file", ""))).exists():
            return [last]
        return []

    def save_data(
        self,
        df: pd.DataFrame,
        metadata: Dict[str, Any],
        symbol: str,
        timeframe: str,
        source: str,
        broker: Optional[str] = None,
    ):
        new_df = self._normalize_df(df)
        if new_df.empty:
            logger.warning(f"No data to save for {symbol} {timeframe} {source}")
            return

        storage_path = self._get_storage_path(symbol, timeframe, source, broker)
        storage_path.mkdir(parents=True, exist_ok=True)

        manifest = self._read_manifest(storage_path) or {"version": 1, "chunks": []}
        previous_chunks = list(manifest.get("chunks") or [])

        tail_entries = self._select_tail_entries(manifest, storage_path)
        if previous_chunks:
            required_tail = min(len(previous_chunks), int(self.merge_tail_chunks))
            if len(tail_entries) < required_tail:
                raise RuntimeError(
                    f"Refusing write for {symbol} ({source}/{broker or 'default'}/{timeframe}): "
                    f"manifest exists but local tail chunks are incomplete "
                    f"(have={len(tail_entries)}, need={required_tail}). "
                    "Pull latest tail chunks before writing."
                )
        rewrite_from = int(tail_entries[0]["index"]) if tail_entries else 0

        tail_frames: List[pd.DataFrame] = []
        for entry in tail_entries:
            chunk_path = storage_path / str(entry["file"])
            if chunk_path.exists():
                tail_frames.append(self._read_chunk(chunk_path))
        tail_df = self._normalize_df(pd.concat(tail_frames, ignore_index=True)) if tail_frames else pd.DataFrame()

        merged_df = self._normalize_df(pd.concat([tail_df, new_df], ignore_index=True))
        if merged_df.empty:
            logger.warning(f"No merged data to save for {symbol} {timeframe} {source}")
            return

        rewritten_entries: List[Dict[str, Any]] = []
        written_indices: set[int] = set()

        for offset, start in enumerate(range(0, len(merged_df), self.chunk_size)):
            idx = rewrite_from + offset
            chunk_df = merged_df.iloc[start : start + self.chunk_size].copy()
            chunk_name = self._chunk_name(symbol, idx)
            chunk_path = storage_path / chunk_name
            self._write_chunk(chunk_path, chunk_df)
            written_indices.add(idx)
            rewritten_entries.append(
                {
                    "index": idx,
                    "file": chunk_name,
                    "rows": int(len(chunk_df)),
                    "start_timestamp": pd.Timestamp(chunk_df["timestamp"].iloc[0]).isoformat(),
                    "end_timestamp": pd.Timestamp(chunk_df["timestamp"].iloc[-1]).isoformat(),
                }
            )

        # Remove stale rewritten chunk files (rare, but safe in case of repairs)
        chunk_pattern = re.compile(rf"^{re.escape(symbol)}_(\d+){re.escape(self._chunk_extension())}$")
        for old_file in storage_path.iterdir():
            if not old_file.is_file():
                continue
            m = chunk_pattern.match(old_file.name)
            if not m:
                continue
            idx = int(m.group(1))
            if idx >= rewrite_from and idx not in written_indices:
                old_file.unlink(missing_ok=True)

        # Keep prefix from older untouched chunks
        prefix_entries = [c for c in previous_chunks if int(c.get("index", -1)) < rewrite_from]
        chunks = prefix_entries + rewritten_entries
        chunks = sorted(chunks, key=lambda x: int(x["index"]))

        record_count = int(sum(int(c.get("rows", 0)) for c in chunks))
        first_ts = chunks[0]["start_timestamp"] if chunks else None
        last_ts = chunks[-1]["end_timestamp"] if chunks else None

        manifest_payload: Dict[str, Any] = {
            "version": 1,
            "chunk_size": int(self.chunk_size),
            "merge_tail_chunks": int(self.merge_tail_chunks),
            "format": "csv",
            "compression": "gzip" if self.compression else "none",
            "symbol": symbol,
            "timeframe": timeframe,
            "source": source,
            "broker": broker,
            "record_count": record_count,
            "first_timestamp": first_ts,
            "last_timestamp": last_ts,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata,
            "chunks": chunks,
        }
        self._write_manifest(storage_path, manifest_payload)
        logger.info(
            f"Saved {len(new_df)} new rows for {symbol} ({source}/{broker or 'default'}/{timeframe}); "
            f"rewritten_from={rewrite_from}, chunks_now={len(chunks)}, total={record_count}"
        )

    def load_data(
        self,
        symbol: str,
        timeframe: str,
        source: str,
        broker: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None,
    ) -> pd.DataFrame:
        storage_path = self._get_storage_path(symbol, timeframe, source, broker)
        if not storage_path.exists():
            return pd.DataFrame()

        manifest = self._read_manifest(storage_path)
        if manifest and manifest.get("chunks"):
            chunk_entries = list(manifest["chunks"])
        else:
            # Best-effort fallback when manifest is missing.
            chunk_entries = []
            for path in self._list_chunk_files(storage_path, symbol):
                name = path.name
                idx = int(name.replace(f"{symbol}_", "").replace(self._chunk_extension(), ""))
                chunk_entries.append({"index": idx, "file": name})
            chunk_entries = sorted(chunk_entries, key=lambda x: int(x["index"]))

        if not chunk_entries:
            return pd.DataFrame()

        if count and count > 0:
            selected: List[Dict[str, Any]] = []
            remaining = int(count)
            for entry in reversed(chunk_entries):
                selected.append(entry)
                row_count = int(entry.get("rows") or self.chunk_size)
                remaining -= row_count
                if remaining <= 0:
                    break
            chunk_entries = list(reversed(selected))

        frames: List[pd.DataFrame] = []
        for entry in chunk_entries:
            chunk_path = storage_path / str(entry["file"])
            if not chunk_path.exists():
                continue
            frames.append(self._read_chunk(chunk_path))

        if not frames:
            return pd.DataFrame()

        df = self._normalize_df(pd.concat(frames, ignore_index=True))
        if df.empty:
            return df

        start_ts = self._to_utc(start_date)
        end_ts = self._to_utc(end_date)
        if start_ts is not None:
            df = df[df["timestamp"] >= start_ts]
        if end_ts is not None:
            df = df[df["timestamp"] <= end_ts]
        df = df.reset_index(drop=True)

        if count and count > 0 and len(df) > int(count):
            df = df.tail(int(count)).reset_index(drop=True)
        return df

    def get_latest_timestamp(
        self,
        symbol: str,
        timeframe: str,
        source: str,
        broker: Optional[str] = None,
    ) -> Optional[datetime]:
        storage_path = self._get_storage_path(symbol, timeframe, source, broker)
        manifest = self._read_manifest(storage_path) if storage_path.exists() else None
        if manifest:
            last_ts = manifest.get("last_timestamp")
            if last_ts:
                ts = pd.Timestamp(last_ts)
                if ts.tzinfo is None:
                    ts = ts.tz_localize("UTC")
                else:
                    ts = ts.tz_convert("UTC")
                return ts.to_pydatetime()

        # Fallback if manifest was not available/corrupted.
        files = self._list_chunk_files(storage_path, symbol)
        if not files:
            return None
        last_df = self._read_chunk(files[-1])
        if last_df.empty:
            return None
        return pd.Timestamp(last_df["timestamp"].max()).to_pydatetime()

    def get_available_data(self) -> List[Dict[str, str]]:
        available: List[Dict[str, str]] = []
        if not self.base_path.exists():
            return available

        tf_re = re.compile(r"^(?:[0-9]+[rR]|[0-9]+[smhdw]|[0-9]+m|[0-9]+h|[0-9]+d|[0-9]+w|[0-9]+|D|W|M|1D|1W|1M)$")

        for source_dir in self.base_path.iterdir():
            if not source_dir.is_dir():
                continue

            for level1_dir in source_dir.iterdir():
                if not level1_dir.is_dir():
                    continue

                if tf_re.fullmatch(level1_dir.name):
                    timeframe_dir = level1_dir
                    for symbol_dir in timeframe_dir.iterdir():
                        if not symbol_dir.is_dir():
                            continue
                        if (symbol_dir / "manifest.json").exists():
                            available.append(
                                {
                                    "source": source_dir.name,
                                    "timeframe": timeframe_dir.name,
                                    "symbol": symbol_dir.name,
                                    "broker": None,
                                }
                            )
                    continue

                broker_dir = level1_dir
                for timeframe_dir in broker_dir.iterdir():
                    if not timeframe_dir.is_dir():
                        continue
                    for symbol_dir in timeframe_dir.iterdir():
                        if not symbol_dir.is_dir():
                            continue
                        if (symbol_dir / "manifest.json").exists():
                            available.append(
                                {
                                    "source": source_dir.name,
                                    "timeframe": timeframe_dir.name,
                                    "symbol": symbol_dir.name,
                                    "broker": broker_dir.name,
                                }
                            )

        return available

    def cleanup_redundant_files(self):
        patterns_to_remove = ["*.tmp", "*.temp", "*.bak", "*.old"]
        for pattern in patterns_to_remove:
            for file_path in self.base_path.rglob(pattern):
                try:
                    file_path.unlink(missing_ok=True)
                except Exception as e:
                    logger.error(f"Error removing file {file_path}: {e}")
