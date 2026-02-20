#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import math
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

try:
    from tvDatafeed import Interval, TvDatafeed
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "tvDatafeed is not installed.\n"
        "Install it with:\n"
        "pip install --upgrade --no-cache-dir git+https://github.com/rongardF/tvdatafeed.git"
    ) from exc

# Allow running as `python collector/simple_tvdatafeed_collector.py`.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_collector.sources.tradingview_ws import TradingViewWebSocketSource


logger = logging.getLogger("collector.simple_tvdatafeed")


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

RANGE_TF_RE = re.compile(r"^[0-9]+[rR]$")


def _is_range_timeframe(tf: str) -> bool:
    return bool(RANGE_TF_RE.fullmatch(str(tf).strip()))


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
    if _is_range_timeframe(tf):
        return tf.upper()
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
    if "bar_index" in out.columns:
        keep.append("bar_index")
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


def _range_cutoff_timestamp(existing_df: pd.DataFrame, overlap_bars: int) -> Optional[pd.Timestamp]:
    if existing_df.empty or "timestamp" not in existing_df.columns:
        return None
    work = existing_df.copy()
    work["timestamp"] = pd.to_datetime(work["timestamp"], utc=True, errors="coerce")
    work = work.dropna(subset=["timestamp"]).sort_values("timestamp")
    if work.empty:
        return None
    tail = work.tail(max(1, int(overlap_bars)))
    return pd.Timestamp(tail["timestamp"].iloc[0])


def _fetch_range_bars(
    *,
    ws_source: TradingViewWebSocketSource,
    contract_symbol: str,
    timeframe: str,
    existing_df: pd.DataFrame,
    overlap_bars: int,
    initial_bars: int,
    max_bars: int,
) -> tuple[pd.DataFrame, Dict[str, Any]]:
    cutoff_ts = _range_cutoff_timestamp(existing_df, overlap_bars)
    n_bars = max(1, min(int(initial_bars), int(max_bars)))
    fetched = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume", "bar_index"])

    for _ in range(10):
        raw = ws_source.fetch_latest(symbol=contract_symbol, timeframe=timeframe, n_bars=int(n_bars))
        fetched = _normalize_tv_df(raw)
        if fetched.empty or cutoff_ts is None:
            break
        earliest = pd.Timestamp(fetched["timestamp"].min())
        if earliest <= cutoff_ts or n_bars >= int(max_bars):
            break
        n_bars = min(int(max_bars), int(n_bars) * 2)

    if cutoff_ts is not None and not fetched.empty:
        fetched = fetched[fetched["timestamp"] >= cutoff_ts].copy()

    fetched = fetched.sort_values("timestamp").reset_index(drop=True)
    if not fetched.empty:
        # The latest range bar is usually still forming.
        fetched = fetched.iloc[:-1].reset_index(drop=True)

    diag = {
        "cutoff_ts": cutoff_ts.isoformat() if cutoff_ts is not None else None,
        "fetched_n_bars": int(n_bars),
    }
    return fetched, diag


def _merge_and_save(path: Path, old_df: pd.DataFrame, new_df: pd.DataFrame) -> tuple[int, int]:
    merged = pd.concat([old_df, new_df], ignore_index=True)
    merged = merged.dropna(subset=["timestamp"])
    merged = merged.sort_values("timestamp")
    merged = merged.drop_duplicates(subset=["timestamp"], keep="last").reset_index(drop=True)

    path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(path, index=False)
    return len(old_df), len(merged)


def _setup_logging(level_name: str) -> None:
    level = getattr(logging, str(level_name).strip().upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Simple incremental collector using tvdatafeed (no proxy).")
    p.add_argument("--config", default="config/collect_jobs.json")
    p.add_argument("--data-root", default="data")
    p.add_argument("--overlap-bars", type=int, default=30)
    p.add_argument("--initial-bars", type=int, default=5000)
    p.add_argument("--max-bars", type=int, default=5000)
    p.add_argument("--range-overlap-bars", type=int, default=300)
    p.add_argument("--range-initial-bars", type=int, default=2000)
    p.add_argument("--range-max-bars", type=int, default=12000)
    p.add_argument("--log-level", default=os.getenv("TV_SIMPLE_COLLECTOR_LOG_LEVEL", "INFO"))
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    _setup_logging(args.log_level)
    config_path = Path(args.config).resolve()
    data_root = Path(args.data_root).resolve()

    jobs = _load_jobs(config_path)
    tv = TvDatafeed()  # no login, no proxy
    ws_source = TradingViewWebSocketSource(
        config={
            "ws_proxy": "",
            "ws_direct_first": True,
            "ws_direct_fallback": True,
            "max_proxy_attempts": 0,
        }
    )
    # Force direct WS mode regardless of host env vars.
    ws_source.ws_proxy = ""
    ws_source.ws_proxy_pool = []
    ws_source.max_proxy_attempts = 0

    summary = {"ok": [], "skipped": [], "failed": []}

    for job in jobs:
        if job.source not in {"tradingview", "tv"}:
            summary["skipped"].append(
                {"symbol": job.symbol, "timeframe": job.timeframe, "reason": f"unsupported source={job.source}"}
            )
            continue

        tf = _normalize_tf(job.timeframe)
        is_range = _is_range_timeframe(tf)
        if not is_range and tf not in INTERVAL_MAP:
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
            logger.info(
                "collect job symbol=%s:%s timeframe=%s existing_rows=%s mode=%s",
                symbol,
                exchange,
                tf,
                len(old_df),
                "tradingview_ws" if is_range else "tvdatafeed",
            )

            if is_range:
                contract_symbol = f"{symbol}:{exchange}"
                new_df, range_diag = _fetch_range_bars(
                    ws_source=ws_source,
                    contract_symbol=contract_symbol,
                    timeframe=tf,
                    existing_df=old_df,
                    overlap_bars=max(1, int(args.range_overlap_bars)),
                    initial_bars=max(1, int(args.range_initial_bars)),
                    max_bars=max(1, int(args.range_max_bars)),
                )
                logger.info(
                    "range fetch symbol=%s timeframe=%s fetched_rows=%s fetched_n_bars=%s cutoff_ts=%s",
                    contract_symbol,
                    tf,
                    len(new_df),
                    range_diag["fetched_n_bars"],
                    range_diag["cutoff_ts"],
                )
            else:
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
                range_diag = {}

            if new_df.empty:
                summary["skipped"].append(
                    {
                        "symbol": f"{symbol}:{exchange}",
                        "timeframe": tf,
                        "reason": "no stable data returned",
                        **({"details": range_diag} if range_diag else {}),
                    }
                )
                continue

            old_rows, merged_rows = _merge_and_save(out_file, old_df, new_df)
            summary["ok"].append(
                {
                    "symbol": f"{symbol}:{exchange}",
                    "timeframe": tf,
                    "mode": "tradingview_ws" if is_range else "tvdatafeed",
                    "fetched_rows": int(len(new_df)),
                    "rows_before": int(old_rows),
                    "rows_after": int(merged_rows),
                    **({"details": range_diag} if range_diag else {}),
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
