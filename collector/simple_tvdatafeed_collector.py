#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

try:
    from tvDatafeed import Interval, TvDatafeed
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "tvDatafeed is not installed.\n"
        "Install it with:\n"
        "pip install --upgrade --no-cache-dir git+https://github.com/rongardF/tvdatafeed.git"
    ) from exc


@dataclass
class Job:
    source: str
    symbol: str
    broker: Optional[str]
    timeframe: str
    enabled: bool


INTERVAL_MAP: Dict[str, object] = {
    "1m": Interval.in_1_minute,
    "3m": Interval.in_3_minute,
    "5m": Interval.in_5_minute,
    "15m": Interval.in_15_minute,
    "30m": Interval.in_30_minute,
    "45m": Interval.in_45_minute,
    "1h": Interval.in_1_hour,
    "2h": Interval.in_2_hour,
    "3h": Interval.in_3_hour,
    "4h": Interval.in_4_hour,
    "1d": Interval.in_daily,
    "1w": Interval.in_weekly,
    "1M": Interval.in_monthly,
}

TIMEFRAME_SECONDS: Dict[str, int] = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "45m": 2700,
    "1h": 3600,
    "2h": 7200,
    "3h": 10800,
    "4h": 14400,
    "1d": 86400,
    "1w": 604800,
    "1M": 2592000,
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _load_jobs(config_path: Path) -> List[Job]:
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    default_cfg = dict(payload.get("default") or {})

    out: List[Job] = []
    for item in payload.get("jobs") or []:
        merged = dict(default_cfg)
        merged.update(item or {})
        out.append(
            Job(
                source=str(merged.get("source", "tradingview")).strip().lower(),
                symbol=str(merged.get("symbol", "")).strip().upper(),
                broker=(str(merged.get("broker")).strip().upper() if merged.get("broker") else None),
                timeframe=str(merged.get("timeframe", "1m")).strip(),
                enabled=bool(merged.get("enabled", True)),
            )
        )
    return [j for j in out if j.enabled]


def _normalize_tf(raw: str) -> str:
    tf = str(raw).strip()
    if tf in {"1D", "D"}:
        return "1d"
    if tf in {"1W", "W"}:
        return "1w"
    return tf


def _resolve_symbol_exchange(job: Job) -> tuple[str, str]:
    symbol = job.symbol
    broker = (job.broker or "").strip().upper()

    if ":" in symbol:
        left, right = symbol.split(":", 1)
        left = left.strip().upper()
        right = right.strip().upper()
        if broker:
            if left == broker:
                return right, broker
            if right == broker:
                return left, broker
            return left, broker
        return left, right

    if not broker:
        raise ValueError(f"job has no broker/exchange: symbol={symbol!r}")
    return symbol, broker


def _job_file_path(data_root: Path, source: str, broker: str, timeframe: str, symbol: str) -> Path:
    return data_root / source / broker / timeframe / symbol / "data.csv"


def _read_existing(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
    df = pd.read_csv(path)
    if "timestamp" not in df.columns:
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
    return df


def _normalize_tv_df(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

    out = df.copy()
    if not isinstance(out.index, pd.RangeIndex):
        out = out.reset_index()

    # tvdatafeed usually returns datetime index and ohlcv columns.
    if "datetime" in out.columns and "timestamp" not in out.columns:
        out = out.rename(columns={"datetime": "timestamp"})
    if "index" in out.columns and "timestamp" not in out.columns:
        out = out.rename(columns={"index": "timestamp"})
    if "time" in out.columns and "timestamp" not in out.columns:
        out = out.rename(columns={"time": "timestamp"})

    if "timestamp" not in out.columns:
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
    keep = ["timestamp", "open", "high", "low", "close", "volume"]
    for col in keep:
        if col not in out.columns:
            out[col] = pd.NA
    out = out[keep]
    out = out.dropna(subset=["timestamp"]).sort_values("timestamp")
    out = out.drop_duplicates(subset=["timestamp"], keep="last")
    return out.reset_index(drop=True)


def _compute_n_bars(
    *,
    existing_df: pd.DataFrame,
    timeframe: str,
    overlap_bars: int,
    initial_bars: int,
    max_bars: int,
) -> int:
    if existing_df.empty:
        return max(1, min(initial_bars, max_bars))

    tf_sec = TIMEFRAME_SECONDS.get(timeframe)
    if not tf_sec:
        return max(1, min(initial_bars, max_bars))

    last_ts = pd.Timestamp(existing_df["timestamp"].max()).to_pydatetime()
    if last_ts.tzinfo is None:
        last_ts = last_ts.replace(tzinfo=timezone.utc)
    now_utc = _utc_now()
    delta_sec = max(0.0, (now_utc - last_ts).total_seconds())
    gap_bars = int(math.ceil(delta_sec / tf_sec))
    n_bars = gap_bars + max(1, overlap_bars)
    n_bars = max(overlap_bars * 3, n_bars)
    return max(1, min(int(n_bars), int(max_bars)))


def _merge_and_save(path: Path, old_df: pd.DataFrame, new_df: pd.DataFrame) -> tuple[int, int]:
    merged = pd.concat([old_df, new_df], ignore_index=True)
    merged = merged.dropna(subset=["timestamp"])
    merged = merged.sort_values("timestamp")
    merged = merged.drop_duplicates(subset=["timestamp"], keep="last").reset_index(drop=True)

    path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(path, index=False)
    return len(old_df), len(merged)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Simple incremental collector using tvdatafeed (no proxy).")
    p.add_argument("--config", default="config/collect_jobs.json")
    p.add_argument("--data-root", default="data")
    p.add_argument("--overlap-bars", type=int, default=30)
    p.add_argument("--initial-bars", type=int, default=5000)
    p.add_argument("--max-bars", type=int, default=5000)
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    config_path = Path(args.config).resolve()
    data_root = Path(args.data_root).resolve()

    jobs = _load_jobs(config_path)
    tv = TvDatafeed()  # no login, no proxy

    summary = {"ok": [], "skipped": [], "failed": []}

    for job in jobs:
        if job.source not in {"tradingview", "tv"}:
            summary["skipped"].append(
                {"symbol": job.symbol, "timeframe": job.timeframe, "reason": f"unsupported source={job.source}"}
            )
            continue

        tf = _normalize_tf(job.timeframe)
        if tf not in INTERVAL_MAP:
            summary["skipped"].append(
                {"symbol": job.symbol, "timeframe": job.timeframe, "reason": "unsupported timeframe for tvdatafeed"}
            )
            continue

        try:
            symbol, exchange = _resolve_symbol_exchange(job)
            out_file = _job_file_path(
                data_root=data_root,
                source="tradingview",
                broker=exchange,
                timeframe=tf,
                symbol=symbol,
            )

            old_df = _read_existing(out_file)
            n_bars = _compute_n_bars(
                existing_df=old_df,
                timeframe=tf,
                overlap_bars=max(1, int(args.overlap_bars)),
                initial_bars=max(1, int(args.initial_bars)),
                max_bars=max(1, int(args.max_bars)),
            )

            raw = tv.get_hist(
                symbol=symbol,
                exchange=exchange,
                interval=INTERVAL_MAP[tf],
                n_bars=n_bars,
            )
            new_df = _normalize_tv_df(raw)

            if new_df.empty:
                summary["skipped"].append(
                    {"symbol": f"{symbol}:{exchange}", "timeframe": tf, "reason": "no data returned"}
                )
                continue

            old_rows, merged_rows = _merge_and_save(out_file, old_df, new_df)
            summary["ok"].append(
                {
                    "symbol": f"{symbol}:{exchange}",
                    "timeframe": tf,
                    "fetched_rows": int(len(new_df)),
                    "rows_before": int(old_rows),
                    "rows_after": int(merged_rows),
                    "file": str(out_file),
                }
            )
        except Exception as exc:  # pragma: no cover
            summary["failed"].append(
                {"symbol": job.symbol, "timeframe": job.timeframe, "error": f"{type(exc).__name__}: {exc}"}
            )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
