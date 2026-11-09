from __future__ import annotations

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from collector.pipeline.normalize import normalize_frame
from collector.pipeline.storage import (
    load_existing_parquet,
    merge_and_save_parquet,
    range_cutoff_ts,
)
from collector.simple_tvdatafeed_collector import _fetch_range_with_overlap
from scripts.build_tv_report import _totals


def candles(timestamps, *, price=1.0):
    return pd.DataFrame(
        {
            "ts": list(timestamps),
            "open": price,
            "high": price + 1,
            "low": price - 1,
            "close": price + 0.5,
            "volume": 10.0,
        }
    )


def test_new_range_snapshot_replaces_all_old_candles_in_covered_suffix(tmp_path):
    # The old timestamp-union merge produces 4916 rows, retaining 55 old bars.
    old = candles(range(4905))
    new = candles([*range(4850), *range(4905, 4916)], price=20.0)
    new.loc[0, ["open", "high", "low", "close", "volume"]] = old.loc[0, ["open", "high", "low", "close", "volume"]]
    assert len(old) == 4905
    assert len(new) == 4861
    path = tmp_path / "2026.parquet"

    stats = merge_and_save_parquet(path, old, new, is_range=True)
    saved = load_existing_parquet(path, is_range=True)

    assert len(saved) == 4861
    assert_frame_equal(saved, normalize_frame(new, drop_latest_candle=False, is_range=True))
    assert stats["replaced_rows"] == 4905
    assert stats["deduped"] == 0
    assert stats["merge_mode"] == "replace_range_suffix"


def test_range_merge_preserves_equal_timestamp_bars_and_snapshot_order(tmp_path):
    old = candles([1, 2, 2, 3, 4])
    old["faraz"] = [1, 0, 0, 0, 0]
    new = candles([2, 2, 3, 3, 4, 5])
    new["close"] = [1.5, 1.5, 11.0, 10.0, 12.0, 13.0]
    path = tmp_path / "2026.parquet"

    stats = merge_and_save_parquet(path, old, new, is_range=True)
    saved = load_existing_parquet(path, is_range=True)

    assert saved["ts"].tolist() == [1, 2, 2, 3, 3, 4, 5]
    assert saved["close"].tolist() == [1.5, 1.5, 1.5, 11, 10, 12, 13]
    assert saved["faraz"].tolist() == [1, 0, 0, 0, 0, 0, 0]
    assert stats["replaced_rows"] == 4
    assert stats["after_last_row"]["close"] == 13

    merge_and_save_parquet(path, saved, new, is_range=True)
    assert_frame_equal(load_existing_parquet(path, is_range=True), saved)


def test_range_normalization_only_drops_final_bar_not_timestamp_group():
    raw = candles([1, 2, 2, 2])
    raw["close"] = [5, 6, 7, 8]
    result = normalize_frame(raw, drop_latest_candle=True, is_range=True)
    assert result["ts"].tolist() == [1, 2, 2]
    assert result["close"].tolist() == [5, 6, 7]


def test_range_cutoff_uses_persisted_sequence():
    # Legacy row order must not be reconstructed by sorting timestamp ties.
    assert range_cutoff_ts(candles([3, 1, 2]), overlap_bars=3) == 3


def test_time_merge_still_updates_one_candle_per_timestamp(tmp_path):
    path = tmp_path / "2026.parquet"
    stats = merge_and_save_parquet(path, candles([1, 2, 3]), candles([2], price=10))
    result = load_existing_parquet(path)
    assert result["ts"].tolist() == [1, 2, 3]
    assert result["close"].tolist() == [1.5, 10.5, 1.5]
    assert stats["deduped"] == 1
    assert stats["replaced_rows"] == 0


def test_empty_range_fetch_keeps_existing_rows(tmp_path):
    path = tmp_path / "2026.parquet"
    old = candles([1, 1, 2])
    merge_and_save_parquet(path, old, candles([]), is_range=True)
    assert load_existing_parquet(path, is_range=True)["ts"].tolist() == [1, 1, 2]


class SnapshotFetcher:
    def __init__(self, frames):
        self.frames = iter(frames)
        self.requests = []

    def fetch_latest_range(self, **kwargs):
        self.requests.append(kwargs["n_bars"])
        return next(self.frames)


def fetch_with_overlap(fetcher, old, *, initial_bars=10, max_bars=20):
    return _fetch_range_with_overlap(
        ws_fetcher=fetcher,
        symbol="TEST",
        exchange="TEST",
        timeframe="100R",
        existing_df=old,
        overlap_bars=3,
        initial_bars=initial_bars,
        max_bars=max_bars,
    )


def test_fetch_keeps_entire_snapshot_including_equal_timestamps():
    raw = candles([0, 1, 2, 2, 3, 4, 5, 6])
    fetcher = SnapshotFetcher([raw])
    fetched, diag = fetch_with_overlap(fetcher, candles([1, 2, 3, 4, 5]))
    assert fetched["ts"].tolist() == [0, 1, 2, 2, 3, 4, 5]
    assert diag["cutoff_ts"] == 3
    assert diag["replacement_start_ts"] == 0


def test_fetch_expands_request_until_required_overlap_is_covered():
    fetcher = SnapshotFetcher([candles([4, 5, 6]), candles([2, 3, 4, 5, 6])])
    fetched, _ = fetch_with_overlap(fetcher, candles([1, 2, 3, 4, 5]))
    assert fetcher.requests == [10, 20]
    assert fetched["ts"].tolist() == [2, 3, 4, 5]


def test_short_response_does_not_count_as_full_history_or_valid_overlap(tmp_path):
    path = tmp_path / "2026.parquet"
    old = candles([1, 2, 3, 4, 5])
    old.to_parquet(path, index=False)
    before = path.read_bytes()
    fetcher = SnapshotFetcher([candles([4, 5, 6]), candles([4, 5, 6])])
    with pytest.raises(RuntimeError, match="overlap"):
        fetch_with_overlap(fetcher, old)
    assert fetcher.requests == [10, 20]
    assert path.read_bytes() == before


def test_range_merge_rejects_out_of_order_timestamps_before_writing(tmp_path):
    path = tmp_path / "2026.parquet"
    old = candles([1, 2, 3])
    old.to_parquet(path, index=False)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="order"):
        merge_and_save_parquet(path, old, candles([2, 1, 3]), is_range=True)
    assert path.read_bytes() == before


def test_parquet_write_failure_preserves_original_file(tmp_path, monkeypatch):
    path = tmp_path / "2026.parquet"
    candles([1, 2, 3]).to_parquet(path, index=False)
    before = path.read_bytes()

    def failed_write(self, tmp_path, **kwargs):
        tmp_path.write_bytes(b"incomplete parquet")
        raise OSError("disk write failed")

    monkeypatch.setattr(pd.DataFrame, "to_parquet", failed_write)
    with pytest.raises(OSError, match="disk write failed"):
        merge_and_save_parquet(path, candles([1, 2, 3]), candles([2, 3, 4]), is_range=True)
    assert path.read_bytes() == before
    assert list(tmp_path.iterdir()) == [path]


def test_report_counts_range_replacements_separately_from_timestamp_duplicates(tmp_path):
    stats = merge_and_save_parquet(
        tmp_path / "2026.parquet", candles([1, 2, 3]), candles([2, 3]), is_range=True
    )
    totals = _totals([{**stats, "fetched_rows": 2}], [], [])
    assert totals["replaced_total"] == 2
    assert totals["deduped_total"] == 0
    assert totals["rows_before_total"] + totals["rows_new_total"] - totals["replaced_total"] == totals["rows_after_total"]


def test_stale_snapshot_cannot_truncate_newer_existing_history(tmp_path):
    path = tmp_path / "2026.parquet"
    old = candles([1, 2, 3, 4, 5, 6])
    old.to_parquet(path, index=False)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="ends before"):
        merge_and_save_parquet(path, old, candles([2, 3, 4]), is_range=True)
    assert path.read_bytes() == before


def test_snapshot_starting_inside_a_same_second_group_is_rejected(tmp_path):
    path = tmp_path / "2026.parquet"
    old = candles([1, 2, 2, 2, 3, 4])
    old["close"] = [1.5, 11, 12, 13, 1.5, 1.5]
    incoming = candles([2, 2, 3, 4, 5])
    incoming["close"] = [12, 13, 1.5, 1.5, 1.5]
    old.to_parquet(path, index=False)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="boundary"):
        merge_and_save_parquet(path, old, incoming, is_range=True)
    assert path.read_bytes() == before


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf")])
def test_invalid_range_bar_cannot_silently_disappear_from_replacement(tmp_path, bad_value):
    path = tmp_path / "2026.parquet"
    old = candles([1, 2, 3, 4])
    incoming = candles([2, 3, 4, 5])
    incoming.loc[1, "close"] = bad_value
    old.to_parquet(path, index=False)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="invalid"):
        merge_and_save_parquet(path, old, incoming, is_range=True)
    assert path.read_bytes() == before


def test_older_tail_is_rejected_even_when_last_second_matches(tmp_path):
    path = tmp_path / "2026.parquet"
    old = candles([1, 2, 3, 4, 4, 4])
    old.to_parquet(path, index=False)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="same-second tail"):
        merge_and_save_parquet(path, old, candles([1, 2, 3, 4]), is_range=True)
    assert path.read_bytes() == before


def test_ambiguous_start_triggers_a_larger_snapshot_request():
    old = candles([1, 2, 2, 2, 3, 4])
    old["close"] = [1.5, 11, 12, 13, 1.5, 1.5]
    partial = candles([2, 2, 3, 4, 5])
    partial["close"] = [12, 13, 1.5, 1.5, 1.5]
    complete = candles([1, 2, 2, 2, 3, 4, 5])
    complete["close"] = [1.5, 11, 12, 13, 1.5, 1.5, 1.5]
    fetcher = SnapshotFetcher([partial, complete])
    fetched, _ = fetch_with_overlap(fetcher, old)
    assert fetcher.requests == [10, 20]
    assert fetched["close"].tolist() == [1.5, 11, 12, 13, 1.5, 1.5]


@pytest.mark.parametrize("first_ts", [2, 2.5])
def test_timestamp_alone_does_not_establish_a_merge_boundary(tmp_path, first_ts):
    path = tmp_path / "2026.parquet"
    old = candles([1, 2, 3, 4])
    incoming = candles([first_ts, 3, 4, 5], price=20.0)
    old.to_parquet(path, index=False)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="boundary"):
        merge_and_save_parquet(path, old, incoming, is_range=True)
    assert path.read_bytes() == before


def test_hundreds_of_bars_in_one_second_survive_roundtrip_in_source_order(tmp_path):
    path = tmp_path / "2026.parquet"
    incoming = candles([1000] * 500)
    incoming["close"] = [1.0, 1.5] * 250
    empty = normalize_frame(None, drop_latest_candle=False, is_range=True)
    merge_and_save_parquet(path, empty, incoming, is_range=True)
    saved = load_existing_parquet(path, is_range=True)
    assert len(saved) == 500
    assert saved["ts"].nunique() == 1
    assert saved["close"].tolist() == incoming["close"].tolist()
    merge_and_save_parquet(path, saved, incoming, is_range=True)
    assert_frame_equal(load_existing_parquet(path, is_range=True), saved)
