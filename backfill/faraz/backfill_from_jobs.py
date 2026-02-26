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

from backfill.faraz.client import (
    FarazClient,
    SUPPORTED_BROKERS,
    UnsupportedFarazSymbolError,
    storage_broker_for_symbol,
)
from backfill.faraz.storage import merge_parquet, parquet_path_for_year, split_by_year
from collector.pipeline.config import is_range_timeframe, load_jobs, normalize_timeframe, resolve_symbol_exchange

logger = logging.getLogger("backfill.faraz.backfill_from_jobs")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Backfill historical candles from Faraz using collect_jobs.json")
    p.add_argument("--config", default="config/collect_jobs.json")
    p.add_argument("--data-root", default="data")
    p.add_argument("--start", default="")
    p.add_argument("--end", default="")
    p.add_argument("--faraz-brokers", default="FXCM,FOREXCOM,OANDA")
    p.add_argument("--base-url", default=os.getenv("FARAZ_BASE_URL", "https://ir2.faraz.io/api/customer/trading-view/history"))
    p.add_argument("--timeout-sec", type=int, default=int(os.getenv("FARAZ_TIMEOUT_SEC", "45")))
    p.add_argument("--max-retries", type=int, default=int(os.getenv("FARAZ_MAX_RETRIES", "3")))
    p.add_argument("--log-level", default=os.getenv("FARAZ_BACKFILL_LOG_LEVEL", "INFO"))
    p.add_argument(
        "--skip-if-local-exists",
        action="store_true",
        help="Skip API fetch when any local parquet already exists under data/faraz/{broker}/{timeframe}/{symbol}",
    )
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


def _has_any_local_faraz_data(*, data_root: Path, broker: str, timeframe: str, symbol: str) -> bool:
    base = data_root / "faraz" / str(broker).upper() / str(timeframe).strip() / str(symbol).upper()
    if not base.exists() or not base.is_dir():
        return False
    return any(p.is_file() for p in base.glob("*.parquet"))


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
    if str(args.start).strip():
        start_dt = _parse_iso_utc(args.start)
    else:
        # Blank start means \"fetch as far back as the API can provide\".
        # Use Unix epoch (0) instead of a negative timestamp to avoid API edge cases.
        start_dt = datetime(1970, 1, 1, tzinfo=timezone.utc)
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
    logger.info(
        "Starting Faraz backfill config=%s data_root=%s start=%s end=%s faraz_brokers=%s total_jobs=%s skip_if_local_exists=%s",
        config_path,
        data_root,
        start_dt.isoformat(),
        end_dt.isoformat(),
        faraz_brokers,
        len(jobs),
        bool(args.skip_if_local_exists),
    )

    progress_total = len(jobs)
    progress_idx = 0

    for job in jobs:
        progress_idx += 1
        logger.info(
            "[job %s/%s] source=%s symbol=%s broker=%s timeframe=%s enabled=%s",
            progress_idx,
            progress_total,
            getattr(job, "source", None),
            getattr(job, "symbol", None),
            getattr(job, "broker", None),
            getattr(job, "timeframe", None),
            getattr(job, "enabled", None),
        )
        if str(job.source).strip().lower() not in {"tradingview", "tv"}:
            logger.info("  skip: non-tradingview source=%s", job.source)
            continue

        tf = normalize_timeframe(job.timeframe)
        if is_range_timeframe(tf):
            logger.info("  skip: range timeframe not supported by Faraz tf=%s", tf)
            summary["skipped"].append(
                {"symbol": job.symbol, "timeframe": tf, "reason": "range timeframe is not supported by Faraz"}
            )
            continue

        try:
            symbol, _ = resolve_symbol_exchange(job)
            logger.info("  normalized symbol=%s tf=%s", symbol, tf)
        except Exception as exc:
            logger.exception("  resolve_symbol_exchange failed symbol=%s tf=%s", job.symbol, tf)
            summary["failed"].append({"symbol": job.symbol, "timeframe": tf, "error": f"resolve_error: {exc}"})
            continue

        for faraz_broker in faraz_brokers:
            storage_broker = storage_broker_for_symbol(symbol=symbol, requested_broker=faraz_broker)
            key = (symbol.upper(), tf, storage_broker)
            if key in seen:
                logger.info(
                    "  skip duplicate effective target symbol=%s tf=%s faraz_broker=%s storage_broker=%s",
                    symbol,
                    tf,
                    faraz_broker,
                    storage_broker,
                )
                continue
            seen.add(key)

            try:
                if args.skip_if_local_exists and _has_any_local_faraz_data(
                    data_root=data_root,
                    broker=storage_broker,
                    timeframe=tf,
                    symbol=symbol,
                ):
                    logger.info(
                        "  skip existing local faraz data symbol=%s tf=%s faraz_broker=%s storage_broker=%s",
                        symbol,
                        tf,
                        faraz_broker,
                        storage_broker,
                    )
                    summary["skipped"].append(
                        {
                            "symbol": symbol,
                            "broker": faraz_broker,
                            "storage_broker": storage_broker,
                            "timeframe": tf,
                            "reason": "local faraz parquet already exists",
                        }
                    )
                    continue

                logger.info(
                    "  fetch start symbol=%s tf=%s faraz_broker=%s storage_broker=%s",
                    symbol,
                    tf,
                    faraz_broker,
                    storage_broker,
                )
                df, stats = client.fetch_history(
                    symbol=symbol,
                    broker=faraz_broker,
                    timeframe=tf,
                    start_dt=start_dt,
                    end_dt=end_dt,
                )
                if df.empty:
                    logger.info(
                        "  skip no rows symbol=%s tf=%s faraz_broker=%s storage_broker=%s",
                        symbol,
                        tf,
                        faraz_broker,
                        storage_broker,
                    )
                    summary["skipped"].append(
                        {"symbol": symbol, "broker": faraz_broker, "timeframe": tf, "reason": "no rows returned"}
                    )
                    continue

                file_stats = []
                for year, part in split_by_year(df, default_faraz=1):
                    path = parquet_path_for_year(
                        data_root=data_root,
                        source="faraz",
                        broker=storage_broker,
                        timeframe=tf,
                        symbol=symbol,
                        year=year,
                    )
                    merge_stats = merge_parquet(path, part, default_faraz=1)
                    logger.info(
                        "  file merged symbol=%s tf=%s year=%s faraz_broker=%s storage_broker=%s added=%s deduped=%s after=%s path=%s",
                        symbol,
                        tf,
                        year,
                        faraz_broker,
                        storage_broker,
                        merge_stats.get("added"),
                        merge_stats.get("deduped"),
                        merge_stats.get("after"),
                        path,
                    )
                    file_stats.append({"year": int(year), "file": str(path), **merge_stats})

                logger.info(
                    "  fetch done symbol=%s tf=%s faraz_broker=%s storage_broker=%s rows=%s pages=%s first_ts=%s last_ts=%s",
                    symbol,
                    tf,
                    faraz_broker,
                    storage_broker,
                    int(stats.rows),
                    int(stats.pages),
                    stats.first_ts,
                    stats.last_ts,
                )
                summary["ok"].append(
                    {
                        "symbol": symbol,
                        "broker": faraz_broker,
                        "storage_broker": storage_broker,
                        "timeframe": tf,
                        "rows": int(stats.rows),
                        "pages": int(stats.pages),
                        "first_ts": stats.first_ts,
                        "last_ts": stats.last_ts,
                        "files": file_stats,
                    }
                )
            except UnsupportedFarazSymbolError as exc:
                logger.info(
                    "  skip unsupported symbol=%s tf=%s faraz_broker=%s storage_broker=%s reason=%s",
                    symbol,
                    tf,
                    faraz_broker,
                    storage_broker,
                    exc,
                )
                summary["skipped"].append(
                    {
                        "symbol": symbol,
                        "broker": faraz_broker,
                        "storage_broker": storage_broker,
                        "timeframe": tf,
                        "reason": str(exc),
                    }
                )
            except Exception as exc:  # pragma: no cover
                logger.exception(
                    "  fetch failed symbol=%s tf=%s faraz_broker=%s storage_broker=%s",
                    symbol,
                    tf,
                    faraz_broker,
                    storage_broker,
                )
                summary["failed"].append(
                    {
                        "symbol": symbol,
                        "broker": faraz_broker,
                        "storage_broker": storage_broker,
                        "timeframe": tf,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

    logger.info(
        "Faraz backfill finished ok=%s skipped=%s failed=%s",
        len(summary["ok"]),
        len(summary["skipped"]),
        len(summary["failed"]),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
