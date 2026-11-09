from __future__ import annotations

import os
import time

import pandas as pd
import pytest

from collector.pipeline import fetchers


class _FakeTvDatafeed:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def get_hist(self, **kwargs) -> pd.DataFrame:
        return pd.DataFrame(
            {"open": [1.0], "high": [2.0], "low": [0.5], "close": [1.5], "volume": [10.0]},
            index=pd.DatetimeIndex(["2026-08-28 17:00:00"], name="datetime"),
        )


def test_tvdatafeed_naive_host_time_is_normalized_to_utc(monkeypatch) -> None:
    monkeypatch.setattr(fetchers, "TvDatafeed", _FakeTvDatafeed)
    monkeypatch.setenv("TVDATAFEED_NAIVE_TZ", "Asia/Tehran")

    frame = fetchers.TvDatafeedFetcher().fetch_latest(
        symbol="AAPL", exchange="NASDAQ", timeframe="1h", n_bars=1
    )

    assert frame.index.tz is not None
    assert frame.index[0] == pd.Timestamp("2026-08-28 13:30:00Z")


def test_tvdatafeed_timezone_aware_index_is_not_shifted(monkeypatch) -> None:
    class AwareFake(_FakeTvDatafeed):
        def get_hist(self, **kwargs) -> pd.DataFrame:
            frame = super().get_hist(**kwargs)
            frame.index = frame.index.tz_localize("UTC")
            return frame

    monkeypatch.setattr(fetchers, "TvDatafeed", AwareFake)
    frame = fetchers.TvDatafeedFetcher().fetch_latest(
        symbol="AAPL", exchange="NASDAQ", timeframe="1h", n_bars=1
    )

    assert frame.index[0] == pd.Timestamp("2026-08-28 17:00:00Z")


@pytest.mark.parametrize("host_tz, expected", [
    ("UTC", "2026-08-28 17:00:00Z"),
    ("Asia/Tehran", "2026-08-28 13:30:00Z"),
])
def test_naive_time_defaults_to_actual_host_timezone(monkeypatch, host_tz, expected):
    previous_tz = os.environ.get("TZ")
    monkeypatch.delenv("TVDATAFEED_NAIVE_TZ", raising=False)
    monkeypatch.setattr(fetchers, "TvDatafeed", _FakeTvDatafeed)
    try:
        os.environ["TZ"] = host_tz
        time.tzset()
        frame = fetchers.TvDatafeedFetcher().fetch_latest(
            symbol="AAPL", exchange="NASDAQ", timeframe="1h", n_bars=1
        )
        assert frame.index[0] == pd.Timestamp(expected)
        assert frame.index.name == "datetime"
    finally:
        if previous_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = previous_tz
        time.tzset()
