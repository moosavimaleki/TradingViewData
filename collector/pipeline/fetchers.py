from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Dict

import pandas as pd

try:
    from tvDatafeed import Interval, TvDatafeed
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "tvDatafeed is not installed.\n"
        "Install it with:\n"
        "pip install --upgrade --no-cache-dir git+https://github.com/rongardF/tvdatafeed.git"
    ) from exc

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


class TvDatafeedFetcher:
    def __init__(self) -> None:
        self._tv = TvDatafeed()

    def fetch_latest(self, *, symbol: str, exchange: str, timeframe: str, n_bars: int) -> pd.DataFrame:
        return self._tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=INTERVAL_MAP[timeframe],
            n_bars=int(n_bars),
        )


def compute_time_n_bars(
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

    last_ts_sec = float(existing_df["ts"].max())
    last_dt = datetime.fromtimestamp(last_ts_sec, tz=timezone.utc)
    now_utc = datetime.now(timezone.utc)
    delta_sec = max(0.0, (now_utc - last_dt).total_seconds())
    gap_bars = int(math.ceil(delta_sec / tf_sec))

    n_bars = gap_bars + max(1, overlap_bars)
    n_bars = max(overlap_bars * 3, n_bars)
    return max(1, min(int(n_bars), int(max_bars)))
