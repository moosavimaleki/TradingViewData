#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Allow running as `python backfill/faraz/backfill_from_jobs.py`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backfill.faraz.client import FarazClient, SUPPORTED_BROKERS
from backfill.faraz.storage import merge_parquet, parquet_path_for_year, split_by_year
from collector.pipeline.config import is_range_timeframe, load_jobs, normalize_timeframe, resolve_symbol_exchange

logger = logging.getLogger("backfill.faraz.backfill_from_jobs")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Backfill historical candles from Faraz using collect_jobs.json")
    p.add_argument("--config", default="config/collect_jobs.json")
    p.add_argument("--data-root", default="data")
    p.add_argument("--start", default="2017-01-01T00:00:00Z")
    p.add_argument("--end", default="")
    p.add_argument("--faraz-brokers", default="FXCM,FOREXCOM,OANDA")
    p.add_argument("--base-url", default=os.getenv("FARAZ_BASE_URL", "https://ir2.faraz.io/api/customer/trading-view/history"))
    p.add_argument("--timeout-sec", type=int, default=int(os.getenv("FARAZ_TIMEOUT_SEC", "45")))
    p.add_argument("--max-retries", type=int, default=int(os.getenv("FARAZ_MAX_RETRIES", "3")))
    p.add_argument("--log-level", default=os.getenv("FARAZ_BACKFILL_LOG_LEVEL", "INFO"))
    return p.parse_args()


def _parse_iso_utc(raw: str) -> datetime:
    text = str(raw or "").strip()
    if not text:
        return datetime.now(timezone.utc)
    return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)


def _setup_logging(level_name: str) -> None:
    level = getattr(logging, str(level_name).strip().upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def _cookie_from_env() -> str:
    cookie = str(os.getenv("FARAZ_COOKIE_STRING", "")).strip()
    if cookie:
        return cookie
    return str(os.getenv("FARAZ_COOKIES", "")).strip()


def main() -> None:
    args = _parse_args()
    _setup_logging(args.log_level)

    cookie_string = _cookie_from_env()
    if not cookie_string:
        raise SystemExit("Missing Faraz cookie. Set FARAZ_COOKIE_STRING (or FARAZ_COOKIES).")

    faraz_brokers = [x.strip().upper() for x in str(args.faraz_brokers).split(",") if x.strip()]
    invalid = [b for b in faraz_brokers if b not in SUPPORTED_BROKERS]
    if invalid:
        raise SystemExit(f"Unsupported Faraz broker(s): {invalid}. Supported={sorted(SUPPORTED_BROKERS)}")

    config_path = Path(args.config).resolve()
    data_root = Path(args.data_root).resolve()
    start_dt = _parse_iso_utc(args.start)
    end_dt = _parse_iso_utc(args.end) if str(args.end).strip() else datetime.now(timezone.utc)

    client = FarazClient(
        cookie_string=cookie_string,
        base_url=args.base_url,
        timeout_sec=args.timeout_sec,
        max_retries=args.max_retries,
    )

    jobs = load_jobs(config_path)
    summary = {"ok": [], "skipped": [], "failed": []}
    seen = set()

    for job in jobs:
        if str(job.source).strip().lower() not in {"tradingview", "tv"}:
            continue

        tf = normalize_timeframe(job.timeframe)
        if is_range_timeframe(tf):
            summary["skipped"].append(
                {"symbol": job.symbol, "timeframe": tf, "reason": "range timeframe is not supported by Faraz"}
            )
            continue

        try:
            symbol, _ = resolve_symbol_exchange(job)
        except Exception as exc:
            summary["failed"].append({"symbol": job.symbol, "timeframe": tf, "error": f"resolve_error: {exc}"})
            continue

        for faraz_broker in faraz_brokers:
            key = (symbol.upper(), tf, faraz_broker)
            if key in seen:
                continue
            seen.add(key)

            try:
                df, stats = client.fetch_history(
                    symbol=symbol,
                    broker=faraz_broker,
                    timeframe=tf,
                    start_dt=start_dt,
                    end_dt=end_dt,
                )
                if df.empty:
                    summary["skipped"].append(
                        {"symbol": symbol, "broker": faraz_broker, "timeframe": tf, "reason": "no rows returned"}
                    )
                    continue

                file_stats = []
                for year, part in split_by_year(df):
                    path = parquet_path_for_year(
                        data_root=data_root,
                        source="faraz",
                        broker=faraz_broker,
                        timeframe=tf,
                        symbol=symbol,
                        year=year,
                    )
                    merge_stats = merge_parquet(path, part)
                    file_stats.append({"year": int(year), "file": str(path), **merge_stats})

                summary["ok"].append(
                    {
                        "symbol": symbol,
                        "broker": faraz_broker,
                        "timeframe": tf,
                        "rows": int(stats.rows),
                        "pages": int(stats.pages),
                        "first_ts": stats.first_ts,
                        "last_ts": stats.last_ts,
                        "files": file_stats,
                    }
                )
            except Exception as exc:  # pragma: no cover
                summary["failed"].append(
                    {"symbol": symbol, "broker": faraz_broker, "timeframe": tf, "error": f"{type(exc).__name__}: {exc}"}
                )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
