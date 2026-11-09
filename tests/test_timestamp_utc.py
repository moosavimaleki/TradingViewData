from __future__ import annotations

from datetime import datetime
import os
import time

import pandas as pd
import pytest

from collector.pipeline import fetchers
from collector.pipeline.normalize import to_epoch_seconds


@pytest.mark.parametrize("value", [
    "2026-11-09T00:00:00Z", "2026-11-09T03:30:00+03:30",
    pd.Timestamp("2026-11-09T00:00:00Z"), 1794182400, 1794182400000,
    1794182400000000, 1794182400000000000,
])
def test_timestamp_inputs_all_represent_the_same_utc_instant(value):
    assert to_epoch_seconds(pd.Series([value])).iloc[0] == 1794182400.0


@pytest.mark.parametrize("unit", ["s", "ms", "us", "ns"])
def test_datetime_resolution_does_not_change_epoch_seconds(unit):
    series = pd.Series(pd.DatetimeIndex(["2026-11-09T00:00:00Z"]).as_unit(unit))
    assert to_epoch_seconds(series).iloc[0] == 1794182400.0


@pytest.mark.parametrize("host_tz", ["UTC", "Asia/Tehran"])
def test_real_provider_fromtimestamp_roundtrip_is_host_timezone_independent(monkeypatch, host_tz):
    previous = os.environ.get("TZ")
    epochs = [1794182400.0, 1785783600.0, pd.Timestamp("2026-12-31T23:59:59Z").timestamp()]
    class Provider:
        def __init__(self, **kwargs):
            pass

        def get_hist(self, **kwargs):
            return pd.DataFrame({"close": [1.0, 2.0, 3.0]}, index=pd.DatetimeIndex([
                datetime.fromtimestamp(epoch) for epoch in epochs
            ], name="datetime"))

    monkeypatch.setattr(fetchers, "TvDatafeed", Provider)
    monkeypatch.delenv("TVDATAFEED_NAIVE_TZ", raising=False)
    try:
        os.environ["TZ"] = host_tz
        time.tzset()
        frame = fetchers.TvDatafeedFetcher().fetch_latest(symbol="TEST", exchange="TEST", timeframe="1m", n_bars=3)
        assert to_epoch_seconds(pd.Series(frame.index)).tolist() == epochs
        assert frame.index[-1].year == 2026
    finally:
        if previous is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = previous
        time.tzset()


def test_nat_is_rejected_instead_of_becoming_a_historical_epoch():
    with pytest.raises(ValueError, match="Could not convert"):
        to_epoch_seconds(pd.Series([pd.NaT], dtype="datetime64[ns]"))


def test_ambiguous_naive_provider_time_is_rejected_instead_of_guessing(monkeypatch):
    previous = os.environ.get("TZ")
    class Provider:
        def __init__(self, **kwargs):
            pass

        def get_hist(self, **kwargs):
            # The naive datetime loses which occurrence of 01:30 was received.
            return pd.DataFrame({"close": [1.0]}, index=pd.DatetimeIndex(["2026-11-01 01:30:00"]))

    monkeypatch.setattr(fetchers, "TvDatafeed", Provider)
    monkeypatch.delenv("TVDATAFEED_NAIVE_TZ", raising=False)
    try:
        os.environ["TZ"] = "America/New_York"
        time.tzset()
        with pytest.raises(ValueError, match="ambiguous"):
            fetchers.TvDatafeedFetcher().fetch_latest(symbol="TEST", exchange="TEST", timeframe="1m", n_bars=1)
    finally:
        if previous is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = previous
        time.tzset()
