#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from collector.pipeline.config import is_range_timeframe, normalize_timeframe, resolve_symbol_exchange
from collector.pipeline.fetchers import INTERVAL_MAP, TvDatafeedFetcher
from collector.pipeline.ws_fetcher import TradingViewWSFetcher
from collector.pipeline.normalize import normalize_frame

TARGET_SYMBOLS = {
    "US100",
    "US500",
    "US30",
    "GER40",
    "UK100",
    "JP225",
    "VIX",
    "XAUUSD",
    "XAGUSD",
    "USOIL",
    "UKOIL",
    "NATGAS",
    "XCUUSD",
    "US10Y",
    "EURUSD",
    "USDJPY",
    "GBPUSD",
    "AAPL",
    "TSLA",
    "NVDA",
    "MYM1!",
    "ES1!",
    "NQ1!",
    "GC1!",
    "SI1!",
    "DXY",
    "EXY",
    "DJI",
    "LUNAUSDT",
    "SHIBUSDT",
    "MANAUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "SOLUSDT",
    "ADAUSDT",
    "DOGEUSDT",
}

TIMEFRAMES = ["1m", "10R", "100R", "1000R"]

def _build_target_jobs(config_path: Path) -> List[Tuple[str, str, str]]:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    jobs = []
    for job in data.get("jobs", []):
        symbol = job.get("symbol", "")
        if symbol not in TARGET_SYMBOLS:
            continue
        if job.get("broker") not in {"BINANCE", "BLACKBULL", "IG", "OANDA", "CMC Markets", "IBKR", "NinjaTrader", "TradingView (Chart Only)", "IGO (Futures Account)"} and job.get("broker").lower().startswith("ig (futures"):
            continue
        tf = normalize_timeframe(job.get("timeframe", ""))
        if tf not in TIMEFRAMES:
            continue
        jobs.append((symbol, job["broker"], job["timeframe"]))
    return sorted(set(jobs))

def main() -> None:
    config_path = Path("config/collect_jobs.json")
    jobs = _build_target_jobs(config_path)
    tv_fetcher = TvDatafeedFetcher()
    ws_fetcher = TradingViewWSFetcher()
    failures = []

    for symbol, broker, frame in jobs:
        tf_norm = normalize_timeframe(frame)
        exchange = broker
        try:
            if is_range_timeframe(tf_norm):
                raw = ws_fetcher.fetch_latest_range(symbol=symbol, broker=exchange, timeframe=tf_norm, n_bars=10)
                normalize_frame(raw, drop_latest_candle=True)
            else:
                if tf_norm not in INTERVAL_MAP:
                    raise ValueError(f"unsupported timeframe {tf_norm}")
                raw = tv_fetcher.fetch_latest(symbol=symbol, exchange=exchange, timeframe=tf_norm, n_bars=10)
                normalize_frame(raw, drop_latest_candle=True)
            logging.info("ok %s %s %s", symbol, broker, frame)
        except Exception as exc:
            logging.error("failed %s %s %s -> %s", symbol, broker, frame, exc)
            failures.append((symbol, broker, frame, str(exc)))

    if failures:
        logging.info("failures=%s", len(failures))
        for entry in failures:
            logging.info(" - %s %s %s error=%s", *entry)
    else:
        logging.info("all %s targets fetched successfully", len(jobs))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
    main()
