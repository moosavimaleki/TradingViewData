#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable, List, Set, Tuple

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


def _run_cmd(cmd: List[str]) -> Tuple[int, str]:
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def _run_with_retry(
    cmd: List[str],
    *,
    attempts: int,
    delay_seconds: float,
    label: str,
    verbose: bool,
) -> Tuple[int, str]:
    final_rc = 1
    final_out = ""
    for idx in range(1, attempts + 1):
        rc, out = _run_cmd(cmd)
        if rc == 0:
            return rc, out
        final_rc = rc
        final_out = out
        if verbose:
            print(f"[retry] {label} attempt={idx}/{attempts} failed rc={rc}", flush=True)
        if idx < attempts:
            time.sleep(delay_seconds)
    return final_rc, final_out


def _looks_missing(output: str) -> bool:
    low = output.lower()
    return any(
        key in low
        for key in (
            "not found",
            "directory not found",
            "couldn't find file",
            "could not find file",
            "file not found",
            "object not found",
        )
    )


def _list_remote_year_files(
    remote_data_root: str,
    run_year: int,
    *,
    attempts: int,
    delay_seconds: float,
    verbose: bool,
) -> Set[str]:
    remote_tv_root = _remote_join(remote_data_root, "tradingview")
    cmd = [
        "rclone",
        "lsf",
        remote_tv_root,
        "--recursive",
        "--files-only",
        "--include",
        f"**/{int(run_year)}.parquet",
    ]
    rc, output = _run_with_retry(
        cmd,
        attempts=attempts,
        delay_seconds=delay_seconds,
        label=f"ls year={int(run_year)}",
        verbose=verbose,
    )
    if rc != 0:
        print(output, flush=True)
        raise SystemExit("remote year parquet ls failed")

    files: Set[str] = set()
    for raw in output.splitlines():
        line = raw.strip().replace("\\", "/").strip("/")
        if not line:
            continue
        files.add(f"tradingview/{line}")
    return files


def _copyto_with_retry(
    remote_file: str,
    local_file: Path,
    *,
    attempts: int,
    delay_seconds: float,
    verbose: bool,
) -> Tuple[int, str]:
    cmd = ["rclone", "copyto", remote_file, str(local_file), "-v"]
    return _run_with_retry(
        cmd,
        attempts=attempts,
        delay_seconds=delay_seconds,
        label=f"copy {remote_file}",
        verbose=verbose,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Pull only current-year parquet files for enabled TradingView jobs.")
    parser.add_argument("--remote", required=True, help="rclone remote root, e.g. gdrive:market-data")
    parser.add_argument("--local-root", default="data", help="local data root")
    parser.add_argument("--config", default="config/collect_jobs.json", help="jobs config path")
    parser.add_argument("--run-year", type=int, required=True, help="pinned run year (UTC)")
    parser.add_argument("--retries", type=int, default=3, help="retry attempts for ls/copy")
    parser.add_argument("--retry-delay", type=float, default=5.0, help="delay between retries (seconds)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    local_root = Path(args.local_root).resolve()
    local_root.mkdir(parents=True, exist_ok=True)
    config_path = Path(args.config).resolve()
    retries = max(1, int(args.retries))
    retry_delay = max(0.0, float(args.retry_delay))
    run_year = int(args.run_year)

    expected_targets = sorted(_iter_targets(config_path=config_path, run_year=run_year))
    expected_set = set(expected_targets)

    remote_files = _list_remote_year_files(
        remote_data_root=args.remote,
        run_year=run_year,
        attempts=retries,
        delay_seconds=retry_delay,
        verbose=args.verbose,
    )

    remote_absent = 0
    copy_missing = 0
    pulled = 0
    failed = 0

    if args.verbose:
        print(
            f"remote_year_listing run_year={run_year} listed={len(remote_files)} expected={len(expected_targets)}",
            flush=True,
        )

    missing_targets = sorted(expected_set - remote_files)
    if missing_targets:
        for rel in missing_targets:
            print(f"new_or_absent_on_remote: {rel}", flush=True)
        remote_absent += len(missing_targets)

    for rel in expected_targets:
        if rel not in remote_files:
            continue
        remote_file = _remote_join(args.remote, rel)
        local_file = local_root / rel
        local_file.parent.mkdir(parents=True, exist_ok=True)

        rc, output = _copyto_with_retry(
            remote_file=remote_file,
            local_file=local_file,
            attempts=retries,
            delay_seconds=retry_delay,
            verbose=args.verbose,
        )
        if rc == 0:
            if local_file.exists():
                pulled += 1
                if args.verbose:
                    print(f"pulled: {rel}", flush=True)
                continue
            output = f"{output}\ncopy succeeded but local file missing: {local_file}"

        if _looks_missing(output):
            copy_missing += 1
            print(f"missing_after_copy: {rel}", flush=True)
            continue

        failed += 1
        print(f"error pulling {rel}:\n{output}", flush=True)

    print(
        (
            f"year_parquet_pull_summary run_year={run_year} expected={len(expected_targets)} "
            f"listed={len(remote_files)} pulled={pulled} remote_absent={remote_absent} "
            f"copy_missing={copy_missing} failed={failed} retries={retries}"
        ),
        flush=True,
    )

    if copy_missing > 0 or failed > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
