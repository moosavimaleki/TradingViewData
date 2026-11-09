#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.ipc as ipc
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from collector.pipeline.raw_archive import verify_archive


def recover_request(run_dir: Path, request_id: str, output_dir: Path) -> list[Path]:
    verify_archive(run_dir)
    table = pq.read_table(run_dir / "data.parquet")
    selected = table.filter(pc.equal(table["request_id"], request_id))
    if not request_id or selected.num_rows == 0:
        raise ValueError(f"Raw request not found: {request_id!r}")
    output_dir.mkdir(parents=True, exist_ok=False)
    events = output_dir / "events.parquet"
    with events.open("xb") as stream:
        pq.write_table(selected, stream, compression="zstd", compression_level=9)
    files = [events]
    for row in selected.to_pylist():
        if row["kind"] != "frame_arrow":
            continue
        original = ipc.open_stream(pa.BufferReader(row["payload"])).read_all()
        path = output_dir / f"frame-{row['sequence']:012d}.parquet"
        with path.open("xb") as stream:
            pq.write_table(original, stream, compression="zstd", compression_level=9)
        files.append(path)
    return files


def main():
    parser = argparse.ArgumentParser(description="Inspect or recover raw requests without editing processed data")
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--request-id")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if args.request_id:
        if args.output_dir is None:
            parser.error("--output-dir is required with --request-id")
        print(json.dumps([str(path) for path in recover_request(args.run_dir, args.request_id, args.output_dir)]))
        return
    verify_archive(args.run_dir)
    rows = pq.read_table(args.run_dir / "data.parquet", columns=[
        "request_id", "symbol", "broker", "timeframe", "kind", "requested_bars",
    ]).to_pylist()
    print(json.dumps([row for row in rows if row["kind"] == "request"], indent=2))


if __name__ == "__main__":
    main()
