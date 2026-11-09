from __future__ import annotations

import pandas as pd
from pandas.testing import assert_frame_equal

from collector.pipeline.normalize import normalize_frame
from collector.pipeline.storage import load_existing_parquet, merge_and_save_parquet
from collector.simple_tvdatafeed_collector import _fetch_range_with_overlap


def candles(times):
    return pd.DataFrame({"ts": list(times), "open": 1.0, "high": 2.0,
                         "low": 0.0, "close": 1.5, "volume": 10.0})


class Fetcher:
    def __init__(self, raw):
        self.raw = raw
        self.requests = []

    def fetch_latest_range(self, **kwargs):
        self.requests.append(kwargs["n_bars"])
        return self.raw.copy()


def collect(tmp_path, old, raw, overlap=3):
    fetcher = Fetcher(raw)
    fetched, diag = _fetch_range_with_overlap(
        ws_fetcher=fetcher, symbol="TEST", exchange="TEST", timeframe="100R",
        existing_df=old, overlap_bars=overlap, initial_bars=20, max_bars=40,
    )
    path = tmp_path / "2026.parquet"
    stats = merge_and_save_parquet(
        path, old, fetched, is_range=True, range_overlap_bars=overlap,
        snapshot_first_ts=diag["snapshot_first_ts"], snapshot_last_ts=diag["snapshot_last_ts"],
    )
    return load_existing_parquet(path, is_range=True), stats, fetcher


def test_repainting_at_cutoff_is_allowed_but_frozen_history_is_unchanged(tmp_path):
    old = candles(range(1, 11))
    old["faraz"] = [1] * 4 + [0] * 6
    raw = candles(range(0, 14))
    raw["close"] = 99.0  # Even the first overlap candle has changed.
    saved, stats, fetcher = collect(tmp_path, old, raw)
    assert_frame_equal(saved[saved["ts"] < 8].reset_index(drop=True),
                       normalize_frame(old[old["ts"] < 8], drop_latest_candle=False, is_range=True))
    assert saved.loc[saved["ts"] >= 8, "close"].tolist() == [99.0] * 5
    assert stats["replaced_rows"] == 3
    assert fetcher.requests == [20]


def test_disappeared_cutoff_candle_is_removed_only_inside_overlap(tmp_path):
    old = candles(range(1, 11))
    raw = candles([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12])
    saved, stats, _ = collect(tmp_path, old, raw)
    assert saved["ts"].tolist() == [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]
    assert stats["replacement_start_ts"] == 8
    assert stats["replaced_rows"] == 3


def test_storage_enforces_overlap_even_if_caller_passes_full_download(tmp_path):
    old = candles(range(1000))
    new = candles(range(1002))
    new["close"] = 99.0
    path = tmp_path / "2026.parquet"
    stats = merge_and_save_parquet(path, old, new, is_range=True, range_overlap_bars=30)
    saved = load_existing_parquet(path, is_range=True)
    assert_frame_equal(saved.iloc[:970], normalize_frame(old.iloc[:970], drop_latest_candle=False, is_range=True))
    assert saved.iloc[970:]["close"].tolist() == [99.0] * 32
    assert stats["replaced_rows"] == 30


def test_same_second_overlap_group_can_repaint_without_deduplication(tmp_path):
    old = candles([1, 2, 2, 2, 3, 4])
    raw = candles([0, 1, 2, 2, 3, 4, 5, 6])
    raw["close"] = [99, 99, 11, 12, 13, 14, 15, 16]
    saved, stats, _ = collect(tmp_path, old, raw, overlap=4)
    assert saved["ts"].tolist() == [1, 2, 2, 3, 4, 5]
    assert saved["close"].tolist() == [1.5, 11, 12, 13, 14, 15]
    # A timestamp group is indivisible; overlap may include more than N rows.
    assert stats["replaced_rows"] == 5


def test_unconfirmed_last_bar_is_excluded_while_covered_tail_can_repaint(tmp_path):
    old = candles(range(1, 11))
    raw = candles([0, 1, 2, 3, 4, 5, 6, 7, 8, 10])
    saved, stats, _ = collect(tmp_path, old, raw)
    assert saved["ts"].tolist() == list(range(1, 9))
    assert stats["replaced_rows"] == 3
