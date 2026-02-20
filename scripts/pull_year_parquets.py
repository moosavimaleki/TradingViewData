#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, List, Set, Tuple

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from collector.pipeline.config import load_jobs, normalize_timeframe, resolve_symbol_exchange


class RcloneCommandError(RuntimeError):
    def __init__(self, label: str, rc: int, output: str) -> None:
        self.label = label
        self.rc = rc
        self.output = output
        super().__init__(f"{label} failed rc={rc}")


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


def _extract_timeframes(targets: Iterable[str]) -> List[str]:
    timeframes: Set[str] = set()
    for rel in targets:
        parts = rel.split("/")
        if len(parts) >= 4:
            timeframes.add(parts[2])
    return sorted(timeframes)


def _run_cmd(cmd: List[str]) -> Tuple[int, str]:
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def _on_retry_sleep(verbose: bool, label: str, attempts: int):
    def _hook(retry_state) -> None:
        if not verbose:
            return
        exc = retry_state.outcome.exception() if retry_state.outcome else None
        rc = getattr(exc, "rc", "unknown")
        print(
            f"[retry] {label} attempt={retry_state.attempt_number}/{attempts} failed rc={rc}",
            flush=True,
        )

    return _hook


def _run_with_retry(
    cmd: List[str],
    *,
    attempts: int,
    delay_seconds: float,
    label: str,
    verbose: bool,
) -> Tuple[int, str]:
    @retry(
        reraise=True,
        stop=stop_after_attempt(attempts),
        wait=wait_fixed(delay_seconds),
        retry=retry_if_exception_type(RcloneCommandError),
        before_sleep=_on_retry_sleep(verbose=verbose, label=label, attempts=attempts),
    )
    def _wrapped() -> str:
        rc, out = _run_cmd(cmd)
        if rc != 0:
            raise RcloneCommandError(label=label, rc=rc, output=out)
        return out

    try:
        output = _wrapped()
        return 0, output
    except RcloneCommandError as exc:
        return exc.rc, exc.output


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
    timeframe_filters: Iterable[str],
    *,
    attempts: int,
    delay_seconds: float,
    verbose: bool,
) -> Tuple[Set[str], str | None]:
    remote_tv_root = _remote_join(remote_data_root, "tradingview")
    cmd = [
        "rclone",
        "lsf",
        remote_tv_root,
        "--recursive",
        "--files-only",
    ]
    filters = [str(tf).strip() for tf in timeframe_filters if str(tf).strip()]
    if filters:
        for tf in sorted(set(filters)):
            cmd.extend(["--include", f"**/{tf}/*/{int(run_year)}.parquet"])
    else:
        cmd.extend(["--include", f"**/{int(run_year)}.parquet"])

    rc, output = _run_with_retry(
        cmd,
        attempts=attempts,
        delay_seconds=delay_seconds,
        label=f"ls year={int(run_year)}",
        verbose=verbose,
    )
    if rc != 0:
        return set(), output

    files: Set[str] = set()
    for raw in output.splitlines():
        line = raw.strip().replace("\\", "/").strip("/")
        if not line:
            continue
        files.add(f"tradingview/{line}")
    return files, None


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


def _write_json(path: Path | None, payload: Dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pull only current-year parquet files for enabled TradingView jobs.")
    parser.add_argument("--remote", required=True, help="rclone remote root, e.g. gdrive:market-data")
    parser.add_argument("--local-root", default="data", help="local data root")
    parser.add_argument("--config", default="config/collect_jobs.json", help="jobs config path")
    parser.add_argument("--run-year", type=int, required=True, help="pinned run year (UTC)")
    parser.add_argument("--retries", type=int, default=3, help="retry attempts for ls/copy")
    parser.add_argument("--retry-delay", type=float, default=5.0, help="delay between retries (seconds)")
    parser.add_argument("--out-json", default="", help="optional path to write detailed pull report json")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    local_root = Path(args.local_root).resolve()
    local_root.mkdir(parents=True, exist_ok=True)
    config_path = Path(args.config).resolve()
    retries = max(1, int(args.retries))
    retry_delay = max(0.0, float(args.retry_delay))
    run_year = int(args.run_year)
    out_json = Path(args.out_json).resolve() if str(args.out_json).strip() else None

    expected_targets = sorted(_iter_targets(config_path=config_path, run_year=run_year))
    expected_timeframes = _extract_timeframes(expected_targets)
    report: Dict[str, Any] = {
        "status": "running",
        "run_year": run_year,
        "remote": str(args.remote),
        "local_root": str(local_root),
        "config": str(config_path),
        "retries": retries,
        "retry_delay": retry_delay,
        "expected_count": len(expected_targets),
        "expected_files": expected_targets,
        "expected_timeframes": expected_timeframes,
        "listed_count": 0,
        "listed_files": [],
        "pulled_count": 0,
        "pulled_files": [],
        "remote_absent_count": 0,
        "remote_absent_files": [],
        "copy_missing_count": 0,
        "copy_missing_files": [],
        "failed_count": 0,
        "failed_files": [],
        "ls_error": None,
    }

    if expected_targets:
        remote_files, ls_error = _list_remote_year_files(
            remote_data_root=args.remote,
            run_year=run_year,
            timeframe_filters=expected_timeframes,
            attempts=retries,
            delay_seconds=retry_delay,
            verbose=args.verbose,
        )
    else:
        remote_files, ls_error = set(), None
    if ls_error is not None:
        report["status"] = "ls_failed"
        report["ls_error"] = ls_error
        _write_json(out_json, report)
        print(ls_error, flush=True)
        print(
            (
                f"year_parquet_pull_summary run_year={run_year} expected={len(expected_targets)} "
                f"listed=0 pulled=0 remote_absent=0 copy_missing=0 failed=0 retries={retries}"
            ),
            flush=True,
        )
        raise SystemExit("remote year parquet ls failed")

    expected_set = set(expected_targets)
    listed_files = sorted(remote_files & expected_set)
    report["listed_count"] = len(listed_files)
    report["listed_files"] = listed_files
    report["listed_remote_count_raw"] = len(remote_files)
    report["listed_remote_files_raw"] = sorted(remote_files)

    if args.verbose:
        print(
            (
                f"remote_year_listing run_year={run_year} expected={len(expected_targets)} "
                f"timeframes={','.join(expected_timeframes) if expected_timeframes else '-'} "
                f"listed_raw={len(remote_files)} listed_expected={len(listed_files)}"
            ),
            flush=True,
        )

    missing_targets = sorted(expected_set - remote_files)
    if missing_targets:
        for rel in missing_targets:
            print(f"new_or_absent_on_remote: {rel}", flush=True)
    report["remote_absent_count"] = len(missing_targets)
    report["remote_absent_files"] = missing_targets

    pulled_files: List[str] = []
    copy_missing_files: List[str] = []
    failed_files: List[Dict[str, Any]] = []

    for rel in listed_files:
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
        if rc == 0 and local_file.exists():
            pulled_files.append(rel)
            if args.verbose:
                print(f"pulled: {rel}", flush=True)
            continue

        if rc == 0 and not local_file.exists():
            output = f"{output}\ncopy succeeded but local file missing: {local_file}"

        if _looks_missing(output):
            copy_missing_files.append(rel)
            print(f"missing_after_copy: {rel}", flush=True)
            continue

        failed_files.append({"file": rel, "error": output.strip()})
        print(f"error pulling {rel}:\n{output}", flush=True)

    report["pulled_count"] = len(pulled_files)
    report["pulled_files"] = pulled_files
    report["copy_missing_count"] = len(copy_missing_files)
    report["copy_missing_files"] = copy_missing_files
    report["failed_count"] = len(failed_files)
    report["failed_files"] = failed_files

    print(
        (
            f"year_parquet_pull_summary run_year={run_year} expected={len(expected_targets)} "
            f"listed={len(listed_files)} pulled={len(pulled_files)} remote_absent={len(missing_targets)} "
            f"copy_missing={len(copy_missing_files)} failed={len(failed_files)} retries={retries}"
        ),
        flush=True,
    )

    if len(listed_files) > 0 and len(pulled_files) != len(listed_files):
        report["status"] = "copy_incomplete"
        _write_json(out_json, report)
        raise SystemExit(
            f"strict pull failed: listed={len(listed_files)} but pulled={len(pulled_files)}. refusing to start collector."
        )

    if len(copy_missing_files) > 0 or len(failed_files) > 0:
        report["status"] = "copy_failed"
        _write_json(out_json, report)
        raise SystemExit(1)

    report["status"] = "ok"
    _write_json(out_json, report)


if __name__ == "__main__":
    main()
