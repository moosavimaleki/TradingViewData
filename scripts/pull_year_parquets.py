#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from collector.pipeline.config import load_jobs, normalize_timeframe, resolve_symbol_exchange


def _remote_join(remote_root: str, rel: str) -> str:
    root = remote_root.rstrip("/")
    rel_norm = rel.replace("\\", "/").strip("/")
    if not rel_norm:
        return root
    return f"{root}/{rel_norm}"


def _iter_targets(config_path: Path, run_year: int) -> Iterable[str]:
    jobs = load_jobs(config_path)
    seen: Set[str] = set()

    for job in jobs:
        if job.source not in {"tradingview", "tv"}:
            continue
        symbol, broker = resolve_symbol_exchange(job)
        timeframe = normalize_timeframe(job.timeframe)
        rel = f"tradingview/{broker}/{timeframe}/{symbol}/{int(run_year)}.parquet"
        if rel in seen:
            continue
        seen.add(rel)
        yield rel


def _copyto(remote_file: str, local_file: Path) -> Tuple[int, str]:
    cmd = ["rclone", "copyto", remote_file, str(local_file), "-v"]
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def main() -> None:
    parser = argparse.ArgumentParser(description="Pull only current-year parquet files for enabled TradingView jobs.")
    parser.add_argument("--remote", required=True, help="rclone remote root, e.g. gdrive:market-data")
    parser.add_argument("--local-root", default="data", help="local data root")
    parser.add_argument("--config", default="config/collect_jobs.json", help="jobs config path")
    parser.add_argument("--run-year", type=int, required=True, help="pinned run year (UTC)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    local_root = Path(args.local_root).resolve()
    local_root.mkdir(parents=True, exist_ok=True)
    config_path = Path(args.config).resolve()

    pulled = 0
    missing = 0
    failed = 0

    for rel in _iter_targets(config_path=config_path, run_year=int(args.run_year)):
        remote_file = _remote_join(args.remote, rel)
        local_file = local_root / rel
        local_file.parent.mkdir(parents=True, exist_ok=True)

        rc, output = _copyto(remote_file=remote_file, local_file=local_file)
        if rc == 0:
            pulled += 1
            if args.verbose:
                print(f"pulled: {rel}", flush=True)
            continue

        low = output.lower()
        if "not found" in low or "directory not found" in low or "couldn't find file" in low:
            missing += 1
            if args.verbose:
                print(f"missing: {rel}", flush=True)
            continue

        failed += 1
        print(f"error pulling {rel}:\n{output}", flush=True)

    print(
        f"year_parquet_pull_summary run_year={int(args.run_year)} pulled={pulled} missing={missing} failed={failed}",
        flush=True,
    )

    if failed > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

