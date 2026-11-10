from __future__ import annotations

import argparse
import json

import pandas as pd
import pyarrow as pa
import pyarrow.ipc as ipc
import pyarrow.parquet as pq
import pytest
from pandas.testing import assert_frame_equal

from collector import simple_tvdatafeed_collector as collector
from collector.pipeline.raw_archive import verify_archive


@pytest.mark.parametrize("merge_fails", [False, True])
def test_collector_replaces_range_snapshot_and_retains_same_time_candles(tmp_path, monkeypatch, capsys, merge_fails):
    config = tmp_path / "jobs.json"
    config.write_text(json.dumps({"jobs": [
        {"source": "tradingview", "broker": "TEST", "symbol": "TEST", "timeframe": "100R"},
    ]}), encoding="utf-8")
    path = tmp_path / "data" / "tradingview" / "TEST" / "100R" / "TEST" / "2026.parquet"
    path.parent.mkdir(parents=True)
    old = pd.DataFrame({
        "ts": [1, 2, 2, 3, 4, 5],
        "open": 1.0, "high": 2.0, "low": 0.0, "close": 1.5, "volume": 10.0,
    })
    old.to_parquet(path, index=False)
    raw = old.copy()
    raw["ts"] = [1, 2, 2, 3, 5, 6]
    raw["close"] = [2.5, 1.2, 1.3, 1.5, 1.7, 1.6]
    raw = raw.rename(columns={"ts": "timestamp"})
    raw["bar_index"] = range(10, 16)

    class Fetcher:
        def __init__(self, **kwargs):
            self.archive = kwargs["raw_archive"]

        def fetch_latest_range(self, **kwargs):
            with self.archive.request(source="tradingview", symbol=kwargs["symbol"], broker=kwargs["broker"],
                                      timeframe=kwargs["timeframe"], requested_bars=kwargs["n_bars"]) as capture:
                capture.frame(raw)
            return raw

    monkeypatch.setenv("RUN_YEAR", "2026")
    monkeypatch.setattr(collector, "TvDatafeedFetcher", lambda **kwargs: None)
    monkeypatch.setattr(collector, "TradingViewWSFetcher", Fetcher)
    monkeypatch.setattr(collector, "_parse_args", lambda: argparse.Namespace(
        config=str(config), data_root=str(tmp_path / "data"), log_level="INFO",
        range_overlap_bars=3, range_initial_bars=10, range_max_bars=20,
        range_source_policy="report-only",
    ))

    if merge_fails:
        def fail_merge(*args, **kwargs):
            raise RuntimeError("merge failed")
        monkeypatch.setattr(collector, "merge_and_save_parquet", fail_merge)
        with pytest.raises(SystemExit) as exc:
            collector.main()
        assert exc.value.code == 1
    else:
        collector.main()

    run_dir = next((tmp_path / "data" / "raw").glob("tradingview/*/*/manifest.json")).parent
    verify_archive(run_dir)
    events = pq.read_table(run_dir / "data.parquet").to_pylist()
    payload = next(row["payload"] for row in events if row["kind"] == "frame_arrow")
    original = ipc.open_stream(pa.BufferReader(payload)).read_all().to_pandas()
    assert_frame_equal(original, raw)  # Includes the final candle removed by normalization.

    saved = pd.read_parquet(path)
    summary = json.loads(capsys.readouterr().out)
    if merge_fails:
        assert_frame_equal(saved, old)
        assert summary["failed"][0]["error"] == "RuntimeError: merge failed"
        return
    assert saved["ts"].tolist() == [1, 2, 2, 3, 5]
    assert saved["close"].tolist() == [1.5, 1.5, 1.5, 1.5, 1.7]
    assert saved["faraz"].tolist() == [0] * 5
    assert not summary["failed"]
    result = summary["ok"][0]
    assert result["rows_before"] == 6
    assert result["rows_after"] == 5
    assert result["replaced_rows"] == 3
    assert result["deduped"] == 0
