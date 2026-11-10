from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from collector.pipeline.range_source import SourcePolicy, classify_snapshot, replay_m1

BASE = 1794232800.


def minute_reference(n=140):
    # Each minute falls sharply and then ends near the low. Widths deliberately
    # differ from the tested range to exercise discrete no-phantom jumps.
    opening = 5000-np.arange(n)*2
    return pd.DataFrame({"ts": BASE+np.arange(n)*60, "open": opening,
                         "high": opening+1.4, "low": opening-1.6, "close": opening-1.2, "volume": 100.})


def classify(frame, minute, **kwargs):
    return classify_snapshot(frame, minute, run_id=kwargs.pop("run_id", "run1"),
                             request_id="r1", captured_at_UTC=kwargs.pop("captured_at_UTC", "2026-11-10T00:00:00Z"), **kwargs)


def fine_reference(minute):
    raw = replay_m1(minute, 1.).copy()
    raw["volume"] = 20.
    # A subminute-shaped alternate path that remains in each known M1 envelope.
    raw["ts"] = np.floor(raw.ts/60)*60+12+np.rint(raw.ts.mod(60)*1000)*10
    raw["open"] = (raw.high+raw.low)/2+.01
    return raw


def test_m1_reconstructed_history_is_not_a_copy_candidate():
    minute = minute_reference()
    raw = replay_m1(minute, 1.)
    annotated, report = classify(raw, minute)
    assert report["counts"]["m1_replay_match"] > 100
    assert not annotated.copy_candidate.any()
    assert report["certified_tick_true_rows"] == 0
    assert report["candidate_suffix"] is None


def test_timestamp_precision_alone_cannot_authorize_copy():
    minute = minute_reference()
    raw = replay_m1(minute, 1.)
    raw.ts = np.floor(raw.ts/60)*60+12+np.rint(raw.ts.mod(60)*1000)*10
    annotated, _ = classify(raw, minute)
    assert annotated.clock_subminute.any()
    assert annotated.m1_price_sequence_match.sum() > 100
    assert not annotated.copy_candidate.any()


def test_subminute_clocks_and_distinct_price_sequences_are_only_candidates():
    minute = minute_reference()
    raw = fine_reference(minute)
    annotated, report = classify(raw, minute)
    assert report["counts"]["subminute_candidate"] > 100
    assert report["certified_tick_true_rows"] == 0
    assert not annotated.source_class.eq("corroborated_candidate").any()


def test_unknown_when_no_m1_and_no_first_bar_clock_guess():
    raw = fine_reference(minute_reference())
    annotated, report = classify(raw, None)
    assert annotated.source_class.eq("unknown").all()
    assert not annotated.copy_candidate.any()
    assert len(annotated) == len(raw)-1


def test_missing_m1_warms_up_again_and_does_not_bridge_gap():
    minute = minute_reference()
    raw = fine_reference(minute)
    minute = minute.drop(index=70)
    annotated, _ = classify(raw, minute)
    # Dropped minute plus the following20minutes cannot borrow evidence from
    # before the missing reference minute.
    after_gap = annotated.ts.between(BASE+70*60, BASE+91*60, inclusive="left")
    assert not annotated.loc[after_gap, "copy_candidate"].any()


def test_outside_m1_envelope_is_unknown_even_with_subminute_clock():
    minute = minute_reference()
    raw = fine_reference(minute)
    raw[["open", "high", "low", "close"]] += 10000
    annotated, _ = classify(raw, minute)
    assert not annotated.copy_candidate.any()


def test_contiguous_unique_contexts_corroborate_only_distinct_later_runs():
    minute = minute_reference()
    raw = fine_reference(minute)
    before, _ = classify(raw, minute)
    after, report = classify(raw, minute, previous=before, run_id="run2", captured_at_UTC="2026-11-10T03:00:00Z")
    assert report["counts"]["corroborated_candidate"] > 100
    same_run, _ = classify(raw, minute, previous=before)
    assert not same_run.source_class.eq("corroborated_candidate").any()
    too_early, _ = classify(raw, minute, previous=after, run_id="run0", captured_at_UTC="2026-11-09T23:00:00Z")
    assert not too_early.source_class.eq("corroborated_candidate").any()


def test_change_to_price_or_time_context_is_not_corroborated():
    minute = minute_reference()
    raw = fine_reference(minute)
    before, _ = classify(raw, minute)
    raw.loc[100, "open"] += .02
    after, _ = classify(raw, minute, previous=before, run_id="run2", captured_at_UTC="2026-11-10T03:00:00Z")
    assert not after.source_class.iloc[100:109].eq("corroborated_candidate").any()


def test_empty_snapshot_has_export_schema():
    data, report = classify(pd.DataFrame(), None)
    assert data.empty and "copy_candidate" in data
    assert report["candidate_rows"] == 0


def test_source_policy_rejects_vacuous_thresholds():
    with pytest.raises(ValueError):
        SourcePolicy(window_bars=1)
    with pytest.raises(ValueError):
        SourcePolicy(minimum_clock_fraction=0)
