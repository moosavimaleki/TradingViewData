#!/usr/bin/env python3
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from collector.pipeline.config import is_range_timeframe, normalize_timeframe
from collector.pipeline.fetchers import INTERVAL_MAP, TvDatafeedFetcher
from collector.pipeline.ws_fetcher import TradingViewWSFetcher
from collector.pipeline.normalize import normalize_frame

TARGET_SYMBOLS = [
    "BNBUSDT",
    "LUNAUSDT",
    "SHIBUSDT",
    "MANAUSDT",
    "ADAUSDT",
    "USDJPY",
    "EURUSD",
    "GBPUSD",
    "AUDUSD",
    "USDCHF",
    "DOGEUSDT",
]

TIMEFRAMES = ["1m", "10R", "100R", "1000R"]

def main() -> None:
    tv_fetcher = TvDatafeedFetcher()
    ws_fetcher = TradingViewWSFetcher()
    failures: List[str] = []
    for symbol in TARGET_SYMBOLS:
        for timeframe in TIMEFRAMES:
            tf = normalize_timeframe(timeframe)
            exchange = "BINANCE" if symbol.endswith("USDT") else "BLACKBULL" if symbol in {"EURUSD","USDJPY","GBPUSD","AUDUSD","USDCHF"} else "OANDA"
            try:
                if is_range_timeframe(tf):
                    raw = ws_fetcher.fetch_latest_range(symbol=symbol, broker=exchange, timeframe=tf, n_bars=5)
                    normalize_frame(raw, drop_latest_candle=True)
                else:
                    if tf not in INTERVAL_MAP:
                        raise ValueError(f"unsupported timeframe {tf}")
                    raw = tv_fetcher.fetch_latest(symbol=symbol, exchange=exchange, timeframe=tf, n_bars=5)
                    normalize_frame(raw, drop_latest_candle=True)
                logging.info("ok %s %s %s", symbol, exchange, timeframe)
            except Exception as exc:
                logging.error("failed %s %s %s -> %s", symbol, exchange, timeframe, exc)
                failures.append(f"{symbol} {exchange} {timeframe}: {exc}")

    if failures:
        logging.info("failures=%d", len(failures))
        for entry in failures:
            logging.info(" - %s", entry)
    else:
        logging.info("all jobs succeeded")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
