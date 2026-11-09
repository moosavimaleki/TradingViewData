#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import pandas as pd

# Allow running as `python collector/simple_tvdatafeed_collector.py`.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from collector.pipeline.config import is_range_timeframe, load_jobs, normalize_timeframe, resolve_symbol_exchange
from collector.pipeline.fetchers import INTERVAL_MAP, TvDatafeedFetcher, compute_time_n_bars
from collector.pipeline.normalize import normalize_frame
from collector.pipeline.raw_archive import RawArchive, RawArchiveError
from collector.pipeline.storage import (
    RangeBoundaryError,
    load_existing_parquet,
    merge_and_save_parquet,
    range_cutoff_ts,
    validate_range_snapshot,
    year_file_path,
)
from collector.pipeline.ws_fetcher import TradingViewWSFetcher

logger = logging.getLogger("collector.simple_tvdatafeed")


def _ts_to_iso(ts_sec: float | None) -> str | None:
    if ts_sec is None:
        return None
    return datetime.fromtimestamp(float(ts_sec), tz=timezone.utc).isoformat()


def _last_row(df) -> dict | None:
    if df is None or df.empty:
        return None
    row = df.iloc[-1].to_dict()
    out: dict = {}
    for k, v in row.items():
        if pd.isna(v):
            out[k] = None
        elif hasattr(v, "item"):
            out[k] = v.item()
        else:
            out[k] = v
    if "ts" in out and out["ts"] is not None:
        out["ts_iso"] = _ts_to_iso(float(out["ts"]))
    return out


def _setup_logging(level_name: str) -> None:
    level = getattr(logging, str(level_name).strip().upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def _fetch_range_with_overlap(
    *,
    ws_fetcher: TradingViewWSFetcher,
    symbol: str,
    exchange: str,
    timeframe: str,
    existing_df,
    overlap_bars: int,
    initial_bars: int,
    max_bars: int,
) -> tuple[Any, Dict[str, Any]]:
    cutoff_ts = range_cutoff_ts(existing_df, overlap_bars)
    n_bars = max(1, min(int(initial_bars), int(max_bars)))
    fetched = None
    snapshot_first_ts = snapshot_last_ts = None

    for _ in range(10):
        raw = ws_fetcher.fetch_latest_range(
            symbol=symbol,
            broker=exchange,
            timeframe=timeframe,
            n_bars=int(n_bars),
        )
        received = normalize_frame(raw, drop_latest_candle=False, is_range=True)
        snapshot_first_ts = float(received["ts"].iloc[0]) if not received.empty else None
        snapshot_last_ts = float(received["ts"].iloc[-1]) if not received.empty else None
        fetched = received.iloc[:-1].reset_index(drop=True)
        logger.info(
            "range snapshot symbol=%s:%s tf=%s requested=%s stable_rows=%s first_ts=%s last_ts=%s cutoff_ts=%s",
            symbol,
            exchange,
            timeframe,
            n_bars,
            len(fetched),
            float(fetched["ts"].iloc[0]) if not fetched.empty else None,
            float(fetched["ts"].iloc[-1]) if not fetched.empty else None,
            cutoff_ts,
        )
        if fetched.empty or cutoff_ts is None:
            break
        earliest = float(fetched["ts"].min())
        if earliest <= cutoff_ts:
            try:
                # Download depth is not permission to rewrite that history.
                # Validate the actual replacement boundary, never an older
                # reconstructed bar outside the configured overlap.
                bounded = fetched.loc[fetched["ts"] >= cutoff_ts].reset_index(drop=True)
                validate_range_snapshot(
                    existing_df, bounded, overlap_start_ts=cutoff_ts,
                    snapshot_first_ts=snapshot_first_ts, snapshot_last_ts=snapshot_last_ts,
                )
            except RangeBoundaryError:
                if n_bars >= int(max_bars):
                    raise
                logger.warning("range boundary is ambiguous; fetching more history symbol=%s:%s", symbol, exchange)
            else:
                break
        if n_bars >= int(max_bars):
            break
        n_bars = min(int(max_bars), int(n_bars) * 2)

    if fetched is None:
        fetched = normalize_frame(None, drop_latest_candle=True, is_range=True)
    if cutoff_ts is not None and not fetched.empty and float(fetched["ts"].min()) > cutoff_ts:
        raise RuntimeError(
            f"Range snapshot does not cover required overlap: earliest_ts={fetched['ts'].min()} "
            f"cutoff_ts={cutoff_ts} requested_bars={n_bars}. Existing parquet was not changed."
        )
    # Preserve the archive before the overlap, even when a larger download
    # was needed. Include the whole timestamp group at the cutoff so distinct
    # same-time range bars retain their source order.
    if cutoff_ts is not None:
        fetched = fetched.loc[fetched["ts"] >= cutoff_ts].reset_index(drop=True)
    validate_range_snapshot(
        existing_df, fetched, overlap_start_ts=cutoff_ts,
        snapshot_first_ts=snapshot_first_ts, snapshot_last_ts=snapshot_last_ts,
    )
    diag = {
        "cutoff_ts": cutoff_ts,
        "fetched_n_bars": int(n_bars),
        "replacement_start_ts": cutoff_ts if cutoff_ts is not None else snapshot_first_ts,
        "snapshot_first_ts": snapshot_first_ts,
        "snapshot_last_ts": snapshot_last_ts,
    }
    return fetched.reset_index(drop=True), diag


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Simple incremental collector using tvdatafeed + custom TradingView WS for range bars."
    )
    p.add_argument("--config", default="config/collect_jobs.json")
    p.add_argument("--data-root", default="data")
    p.add_argument("--raw-root", default="", help="Raw archive root (default: DATA_ROOT/raw)")
    p.add_argument("--overlap-bars", type=int, default=30)
    p.add_argument("--initial-bars", type=int, default=5000)
    p.add_argument("--max-bars", type=int, default=5000)
    p.add_argument("--range-overlap-bars", type=int, default=300)
    p.add_argument("--range-initial-bars", type=int, default=2000)
    p.add_argument("--range-max-bars", type=int, default=12000)
    p.add_argument("--log-level", default=os.getenv("TV_SIMPLE_COLLECTOR_LOG_LEVEL", "INFO"))
    return p.parse_args()


def _run_collection(args, raw_archive: RawArchive) -> None:
    config_path = Path(args.config).resolve()
    data_root = Path(args.data_root).resolve()
    run_year_raw = str(os.getenv("RUN_YEAR", "")).strip()
    if run_year_raw:
        try:
            run_year = int(run_year_raw)
        except ValueError as exc:
            raise SystemExit(f"Invalid RUN_YEAR={run_year_raw!r}. RUN_YEAR must be an integer year.") from exc
    else:
        run_year = datetime.now(timezone.utc).year

    jobs = load_jobs(config_path)
    tv_fetcher = TvDatafeedFetcher(raw_archive=raw_archive)
    ws_fetcher = TradingViewWSFetcher(
        timeout_sec=int(os.getenv("TV_WS_TIMEOUT_SEC", "30")),
        page_step=int(os.getenv("TV_WS_PAGE_STEP", "2000")),
        raw_archive=raw_archive,
    )

    summary = {"ok": [], "skipped": [], "failed": []}

    for job in jobs:
        if job.source not in {"tradingview", "tv"}:
            summary["skipped"].append(
                {"symbol": job.symbol, "timeframe": job.timeframe, "reason": f"unsupported source={job.source}"}
            )
            continue

        tf = normalize_timeframe(job.timeframe)
        is_range = is_range_timeframe(tf)
        if not is_range and tf not in INTERVAL_MAP:
            summary["skipped"].append(
                {"symbol": job.symbol, "timeframe": job.timeframe, "reason": "unsupported timeframe for tvdatafeed"}
            )
            continue

        try:
            symbol, exchange = resolve_symbol_exchange(job)
            out_file = year_file_path(
                data_root=data_root,
                source="tradingview",
                broker=exchange,
                timeframe=tf,
                symbol=symbol,
                run_year=run_year,
            )
            old_df = load_existing_parquet(out_file, is_range=is_range)

            logger.info(
                "collect symbol=%s:%s tf=%s run_year=%s rows_before=%s mode=%s",
                symbol,
                exchange,
                tf,
                run_year,
                len(old_df),
                "tradingview_ws" if is_range else "tvdatafeed",
            )

            if is_range:
                new_df, diag = _fetch_range_with_overlap(
                    ws_fetcher=ws_fetcher,
                    symbol=symbol,
                    exchange=exchange,
                    timeframe=tf,
                    existing_df=old_df,
                    overlap_bars=max(1, int(args.range_overlap_bars)),
                    initial_bars=max(1, int(args.range_initial_bars)),
                    max_bars=max(1, int(args.range_max_bars)),
                )
                diag["configured_overlap_bars"] = int(max(1, int(args.range_overlap_bars)))
            else:
                n_bars = compute_time_n_bars(
                    existing_df=old_df,
                    timeframe=tf,
                    overlap_bars=max(1, int(args.overlap_bars)),
                    initial_bars=max(1, int(args.initial_bars)),
                    max_bars=max(1, int(args.max_bars)),
                )
                raw = tv_fetcher.fetch_latest(symbol=symbol, exchange=exchange, timeframe=tf, n_bars=n_bars)
                new_df = normalize_frame(raw, drop_latest_candle=True)
                diag = {
                    "fetched_n_bars": int(n_bars),
                    "configured_overlap_bars": int(max(1, int(args.overlap_bars))),
                }

            if new_df.empty:
                summary["skipped"].append(
                    {
                        "symbol": f"{symbol}:{exchange}",
                        "timeframe": tf,
                        "reason": "no stable data returned after dropping latest candle",
                        "details": diag,
                    }
                )
                continue

            old_last_ts = float(old_df["ts"].max()) if not old_df.empty else None
            new_first_ts = float(new_df["ts"].min()) if not new_df.empty else None
            new_last_ts = float(new_df["ts"].max()) if not new_df.empty else None
            overlap_rows = 0
            overlap_seconds = 0.0
            if new_first_ts is not None and not old_df.empty:
                overlap_rows = int((old_df["ts"] >= new_first_ts).sum())
            if old_last_ts is not None and new_first_ts is not None and old_last_ts >= new_first_ts:
                overlap_seconds = float(old_last_ts - new_first_ts)

            merge_stats = merge_and_save_parquet(
                out_file, old_df, new_df, is_range=is_range,
                range_overlap_bars=max(1, int(args.range_overlap_bars)),
                snapshot_first_ts=diag.get("snapshot_first_ts") if is_range else None,
                snapshot_last_ts=diag.get("snapshot_last_ts") if is_range else None,
            )
            logger.info(
                "saved symbol=%s:%s tf=%s merge_mode=%s before=%s fetched=%s replaced=%s deduped=%s after=%s",
                symbol,
                exchange,
                tf,
                merge_stats["merge_mode"],
                merge_stats["rows_before"],
                len(new_df),
                merge_stats["replaced_rows"],
                merge_stats["deduped"],
                merge_stats["rows_after"],
            )

            after_last_ts = None
            after_last_row = merge_stats.get("after_last_row")
            if isinstance(after_last_row, dict) and after_last_row.get("ts") is not None:
                after_last_ts = float(after_last_row["ts"])

            summary["ok"].append(
                {
                    "symbol": f"{symbol}:{exchange}",
                    "timeframe": tf,
                    "mode": "tradingview_ws" if is_range else "tvdatafeed",
                    "run_year": int(run_year),
                    "fetched_rows": int(len(new_df)),
                    "rows_before": int(merge_stats["rows_before"]),
                    "rows_after": int(merge_stats["rows_after"]),
                    "deduped": int(merge_stats["deduped"]),
                    "replaced_rows": int(merge_stats["replaced_rows"]),
                    "merge_mode": merge_stats["merge_mode"],
                    "replacement_start_ts": merge_stats["replacement_start_ts"],
                    "before_last_ts": old_last_ts,
                    "before_last_ts_iso": _ts_to_iso(old_last_ts),
                    "before_last_row": _last_row(old_df),
                    "fetched_first_ts": new_first_ts,
                    "fetched_first_ts_iso": _ts_to_iso(new_first_ts),
                    "fetched_last_ts": new_last_ts,
                    "fetched_last_ts_iso": _ts_to_iso(new_last_ts),
                    "after_last_ts": after_last_ts,
                    "after_last_ts_iso": _ts_to_iso(after_last_ts),
                    "after_last_row": after_last_row,
                    "overlap_rows": int(overlap_rows),
                    "overlap_seconds": round(overlap_seconds, 6),
                    "overlap_ms": int(round(overlap_seconds * 1000.0)),
                    "overlap_minutes": round(overlap_seconds / 60.0, 3),
                    "details": diag,
                    "file": str(out_file),
                }
            )
        except RawArchiveError:
            logger.exception("Raw archive failed; stopping collection before any further merges")
            raise
        except Exception as exc:  # pragma: no cover
            summary["failed"].append(
                {"symbol": job.symbol, "timeframe": job.timeframe, "error": f"{type(exc).__name__}: {exc}"}
            )

    summary["raw_archive"] = {
        "run_id": raw_archive.run_id,
        "directory": str(raw_archive.run_dir),
        "requests": raw_archive.requests,
        "events": raw_archive.sequence,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["failed"]:
        raise SystemExit(1)


def main() -> None:
    args = _parse_args()
    _setup_logging(args.log_level)
    raw_root = Path(getattr(args, "raw_root", "") or Path(args.data_root) / "raw").resolve()
    with RawArchive(raw_root, config_path=Path(args.config).resolve()) as archive:
        logger.info("Raw capture enabled directory=%s", archive.run_dir)
        _run_collection(args, archive)


if __name__ == "__main__":
    main()
