from __future__ import annotations

import pandas as pd
import pyarrow as pa
import pyarrow.ipc as ipc
import pyarrow.parquet as pq
from pandas.testing import assert_frame_equal

from collector.pipeline import fetchers
from collector.pipeline.raw_archive import RawArchive


def test_raw_frame_is_saved_before_downstream_timezone_conversion(monkeypatch, tmp_path):
    source = pd.DataFrame(
        {"open": [1.0], "high": [2.0], "low": [0.5], "close": [1.5], "volume": [10.0]},
        index=pd.DatetimeIndex(["2026-08-28 17:00:00"], name="datetime"),
    )

    class FakeTvDatafeed:
        def __init__(self, **kwargs):
            pass

        def get_hist(self, **kwargs):
            return source.copy()

    config = tmp_path / "jobs.json"
    config.write_text('{"jobs": []}')
    monkeypatch.setattr(fetchers, "TvDatafeed", FakeTvDatafeed)
    monkeypatch.setenv("TVDATAFEED_NAIVE_TZ", "Asia/Tehran")
    with RawArchive(tmp_path / "raw", config_path=config) as archive:
        fetchers.TvDatafeedFetcher(raw_archive=archive).fetch_latest(
            symbol="AAPL", exchange="NASDAQ", timeframe="1h", n_bars=1,
        )
    rows = pq.read_table(archive.run_dir / "data.parquet").to_pylist()
    payload = next(row["payload"] for row in rows if row["kind"] == "frame_arrow")
    original = ipc.open_stream(pa.BufferReader(payload)).read_all().to_pandas()
    assert_frame_equal(original, source)
