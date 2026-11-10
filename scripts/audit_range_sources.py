#!/usr/bin/env python3
"""Audit sealed collector runs and export evidence-labelled contiguous blocks.

Never reads or writes the legacy yearly price archive. Failed requests are
excluded. References are freshly captured once per symbol, or supplied offline.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.ipc as ipc
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from collector.pipeline.range_source import classify_snapshot, FINE_LABELS
from collector.pipeline.raw_archive import RawArchive, verify_archive
from collector.pipeline.ws_fetcher import TradingViewWSFetcher, _ws_decode


def safe_component(value):
    if not value or value in (".", "..") or any(c in value for c in ("/", "\\", "\x00")):
        raise ValueError(f"Unsafe source path component: {value!r}")
    return value


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def json_write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def successful_range_frames(directory):
    """Use the original pre-normalization frame with session-local bar indexes."""
    manifest = verify_archive(directory)
    grouped = defaultdict(list)
    for row in pq.read_table(directory/"data.parquet").to_pylist():
        if row["request_id"]:
            grouped[row["request_id"]].append(row)
    found = []
    for request_id, events in grouped.items():
        start = next(r for r in events if r["kind"] == "request")
        if not start["timeframe"].upper().endswith("R"):
            continue
        end = [r for r in events if r["kind"] == "request_end"]
        frames = [r for r in events if r["kind"] == "frame_arrow"]
        if not end or json.loads(end[-1]["payload"])["status"] != "ok" or not frames:
            continue
        frame = ipc.open_stream(pa.BufferReader(frames[-1]["payload"])).read_all().to_pandas()
        if "bar_index" not in frame:
            raise ValueError("Range frame lacks original session-local bar indexes")
        for name in ("broker", "symbol", "timeframe"):
            safe_component(start[name])
        meta = {k: start[k] for k in ("broker", "symbol", "timeframe", "requested_bars")}
        meta.update(run_id=manifest["run_id"], request_id=request_id,
                    captured_at_UTC=start["received_at"].isoformat(), raw_sha256=manifest["sha256"],
                    raw_directory=str(directory), github_run_id=manifest.get("github_run_id"))
        nodes = set()
        for event in events:
            if event["kind"] not in ("ws_text", "ws_bytes"):
                continue
            raw_text = event["payload"].decode("utf-8")
            for payload in _ws_decode(raw_text) or [raw_text]:
                if payload.startswith("~h~"):
                    continue
                message = json.loads(payload)
                if not isinstance(message, dict):
                    continue
                if message.get("m") == "symbol_resolved":
                    resolved = message["p"][-1]
                    meta["resolved_symbol"] = {k: resolved[k] for k in ("name", "timezone", "session", "minmov", "pricescale") if k in resolved}
                if message.get("m") in ("timescale_update", "du"):
                    for series in message["p"][1].values():
                        if isinstance(series, dict) and series.get("node"):
                            nodes.add(series["node"])
        meta["processing_nodes"] = sorted(nodes)
        found.append((frame, meta))
    # Adaptive retries are preserved in raw but only the last successful
    # snapshot per symbol/timeframe enters this run's classification.
    selected = {}
    for frame, meta in sorted(found, key=lambda item: item[1]["captured_at_UTC"]):
        selected[(meta["broker"], meta["timeframe"], meta["symbol"])] = (frame, meta)
    return list(selected.values())


def export_blocks(folder, annotated, label, mask, minimum_rows=8):
    """Never remove ambiguous interior rows and silently stitch the remainder."""
    records = []
    cuts = np.r_[0, np.flatnonzero(mask[1:] != mask[:-1])+1, len(mask)] if len(mask) else []
    for a, b in zip(cuts, cuts[1:]):
        if not mask[a] or b-a < minimum_rows:
            continue
        path = folder/f"{label}-{a:06d}-{b-1:06d}.parquet"
        annotated.iloc[a:b].to_parquet(path, index=False, compression="zstd")
        records.append({"file": path.name, "rows": int(b-a), "first_source_row": int(a), "last_source_row": int(b-1),
                        "sha256": digest(path),
                        "first_UTC": pd.Timestamp(annotated.ts.iloc[a], unit="s", tz="UTC").isoformat(),
                        "last_UTC": pd.Timestamp(annotated.ts.iloc[b-1], unit="s", tz="UTC").isoformat()})
    return records


def write_result(output, state_root, raw, meta, minute, reference, reference_error=None):
    folder = output/meta["run_id"]/meta["broker"]/meta["timeframe"]/meta["symbol"]
    if folder.exists():
        raise ValueError(f"Refuse to overwrite an earlier audit: {folder}")
    state = state_root/meta["broker"]/meta["timeframe"]/meta["symbol"]/"latest.parquet"
    previous = pd.read_parquet(state) if state.exists() else None
    state_error = None
    if previous is not None:
        identity = {"broker": meta["broker"], "symbol": meta["symbol"], "timeframe": meta["timeframe"]}
        if any(k not in previous or not previous[k].eq(v).all() for k, v in identity.items()):
            previous, state_error = None, "Previous state identity invalid; corroboration disabled"
        elif previous.empty or previous.run_id.iloc[0] == meta["run_id"]:
            previous = None
    annotated, report = classify_snapshot(raw, minute, run_id=meta["run_id"], request_id=meta["request_id"],
                                          captured_at_UTC=meta["captured_at_UTC"], previous=previous)
    annotated["policy_version"] = report["schema_version"]
    for k in ("broker", "symbol", "timeframe"):
        annotated[k] = meta[k]
    folder.mkdir(parents=True)
    snapshot_path = folder/"snapshot.parquet"
    annotated.to_parquet(snapshot_path, index=False, compression="zstd")
    report.update(meta, reference=reference, reference_error=reference_error, state_error=state_error,
                  snapshot_file=str(snapshot_path), snapshot_sha256=digest(snapshot_path))
    report["implementation_sha256"] = {"classifier": digest(ROOT/"collector/pipeline/range_source.py"),
                                       "auditor": digest(Path(__file__))}
    report["candidate_exports"] = export_blocks(folder, annotated, "candidate", annotated.copy_candidate.to_numpy(bool))
    report["corroborated_exports"] = export_blocks(folder, annotated, "corroborated", annotated.source_class.eq("corroborated_candidate").to_numpy())
    json_write(folder/"report.json", report)
    # State is only a previous observation, never an accumulated price series.
    # An unknown-only/empty run must not erase previously useful provenance.
    useful = not annotated.empty and (annotated.copy_candidate.any() or previous is None)
    if useful and (previous is None or pd.Timestamp(meta["captured_at_UTC"]) > pd.Timestamp(previous.captured_at_UTC.iloc[0])):
        state.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=state.parent, suffix=".tmp", delete=False) as stream:
            tmp = Path(stream.name)
        try:
            annotated.to_parquet(tmp, index=False, compression="zstd")
            os.replace(tmp, state)
        finally:
            tmp.unlink(missing_ok=True)
    return report


def markdown(reports):
    lines = ["# Range source evidence (UTC)", "",
             "Candidate means subminute evidence, not independently verified tick data. Legacy yearly parquets are unverified.", "",
             "Copy whole exported blocks; do not concatenate across unknown rows or between runs without sequence alignment.", "",
             "| Symbol | TF | M1 replay | Subminute candidate | Corroborated | Unknown | Exported candidate interval(s) |",
             "|---|---|---:|---:|---:|---:|---|"]
    for r in reports:
        counts = r["counts"]
        spans = "; ".join(f"{x['first_UTC']} → {x['last_UTC']} ({x['rows']} bars)" for x in r["candidate_exports"]) or "none"
        lines.append(f"| {r['broker']}:{r['symbol']} | {r['timeframe']} | {counts.get('m1_replay_match', 0)} | "
                     f"{counts.get('subminute_candidate', 0)} | {counts.get('corroborated_candidate', 0)} | {counts.get('unknown', 0)} | {spans} |")
        if r.get("reference_error"):
            lines.extend(["", f"Reference failed for {r['broker']}:{r['symbol']}: {r['reference_error']}"])
    return "\n".join(lines)+"\n"


def run(args):
    directories = [Path(p) for p in args.raw_run]
    if args.collect_summary:
        summary = json.loads(Path(args.collect_summary).read_text())
        directories.append(Path(summary["raw_archive"]["directory"]))
    if not directories:
        raise ValueError("Supply --raw-run or --collect-summary")
    frames = [item for directory in directories for item in successful_range_frames(directory)]
    symbols = set(getattr(args, "symbols", []) or [])
    if symbols:
        frames = [(frame, meta) for frame, meta in frames if meta["broker"]+":"+meta["symbol"] in symbols]
    groups = defaultdict(list)
    for frame, metadata in frames:
        groups[(metadata["broker"], metadata["symbol"])].append((frame, metadata))
    references = json.loads(Path(args.reference_map).read_text()) if args.reference_map else {}
    output, state_root = Path(args.output), Path(args.state_root)
    reports = []
    for (broker, symbol), snapshots in groups.items():
        minute, reference, error = None, None, None
        key = broker+":"+symbol
        try:
            if key in references:
                path = Path(references[key])
                minute = pd.read_parquet(path)
                reference = {"path": str(path), "sha256": digest(path), "mode": "offline supplied M1"}
            elif args.allow_network:
                with RawArchive(Path(args.raw_root), config_path=Path(args.config)) as archive:
                    fetcher = TradingViewWSFetcher(timeout_sec=45, raw_archive=archive)
                    minute = fetcher.fetch_latest_time(symbol=symbol, broker=broker, timeframe="1", n_bars=args.reference_bars)
                manifest = verify_archive(archive.run_dir)
                reference = {"raw_directory": str(archive.run_dir), "raw_sha256": manifest["sha256"],
                             "mode": "paired explicit-epoch M1 websocket", "rows": len(minute)}
            else:
                error = "No offline M1 reference supplied; network disabled"
        except Exception as exc:
            minute, error = None, f"{type(exc).__name__}: {exc}"
        for raw, meta in sorted(snapshots, key=lambda item: item[1]["captured_at_UTC"]):
            reports.append(write_result(output, state_root, raw, meta, minute, reference, error))
    summary = {"schema_version": 1, "generated_UTC": datetime.now(timezone.utc).isoformat(),
               "reports": reports, "certified_tick_true_rows": 0, "legacy_archive_modified": False}
    json_write(Path(args.summary), summary)
    Path(args.report).write_text(markdown(reports), encoding="utf-8")
    print(json.dumps({"range_snapshots_audited": len(reports), "summary": args.summary,
                      "candidate_rows": sum(r.get("candidate_rows", 0) for r in reports),
                      "reference_failures": sum(bool(r["reference_error"]) for r in reports)}), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-run", action="append", default=[])
    parser.add_argument("--collect-summary")
    parser.add_argument("--symbols", nargs="*", help="Optional BROKER:SYMBOL subset for offline review")
    parser.add_argument("--reference-map", help="JSON mapping BROKER:SYMBOL to raw M1 parquet (last row may be forming)")
    parser.add_argument("--allow-network", action="store_true")
    parser.add_argument("--reference-bars", type=int, default=10000)
    parser.add_argument("--raw-root", default="data/raw")
    parser.add_argument("--config", default="config/collect_jobs.json")
    parser.add_argument("--output", default="data/range_quality")
    parser.add_argument("--state-root", default="data/range_quality_state")
    parser.add_argument("--summary", default="range_source_summary.json")
    parser.add_argument("--report", default="range_source_report.md")
    args = parser.parse_args()
    if not 1 <= args.reference_bars <= 12000:
        parser.error("reference-bars must be between1 and12000")
    run(args)


if __name__ == "__main__":
    main()
