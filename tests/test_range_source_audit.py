from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from collector.pipeline.range_source import replay_m1
from collector.pipeline.raw_archive import RawArchive
from scripts.audit_range_sources import export_blocks, run, successful_range_frames, write_result


def inputs():
    opening = 5000-np.arange(140)*2
    minute = pd.DataFrame({"ts": 1794232800.+np.arange(140)*60, "open": opening,
                           "high": opening+1.4, "low": opening-1.6, "close": opening-1.2, "volume": 100.})
    raw = replay_m1(minute, 1.)
    raw["bar_index"] = np.arange(len(raw))
    raw["volume"] = 20.
    raw.ts = np.floor(raw.ts/60)*60+12+np.rint(raw.ts.mod(60)*1000)*10
    raw.open = (raw.high+raw.low)/2+.01
    return minute, raw


def meta(run_id="run1", at="2026-11-10T00:00:00Z"):
    return {"run_id": run_id, "request_id": "r1", "captured_at_UTC": at,
            "symbol": "GOLD", "broker": "TEST", "timeframe": "100R", "raw_sha256": "example"}


def test_blocks_never_stitch_over_unknown_interior_rows(tmp_path):
    frame = pd.DataFrame({"source_row": np.arange(30), "ts": np.arange(30)+1794232800.})
    mask = np.ones(30, bool)
    mask[12:16] = False
    records = export_blocks(tmp_path, frame, "candidate", mask)
    assert [(r["first_source_row"], r["last_source_row"]) for r in records] == [(0, 11), (16, 29)]
    for record in records:
        saved = pd.read_parquet(tmp_path/record["file"])
        assert np.all(np.diff(saved.source_row) == 1)


def test_result_is_immutable_and_provenance_allows_later_corroboration(tmp_path):
    minute, raw = inputs()
    output, state = tmp_path/"output", tmp_path/"state"
    first = write_result(output, state, raw, meta(), minute, {"mode": "fixture"})
    second = write_result(output, state, raw, meta("run2", "2026-11-10T03:00:00Z"), minute, {"mode": "fixture"})
    assert first["candidate_exports"] and second["corroborated_exports"]
    saved = pd.read_parquet(first["snapshot_file"])
    np.testing.assert_array_equal(saved[["ts", "open", "high", "low", "close", "volume"]],
                                  raw.iloc[:-1][["ts", "open", "high", "low", "close", "volume"]])
    with pytest.raises(ValueError, match="overwrite"):
        write_result(output, state, raw, meta(), minute, {})


def test_reference_failure_cannot_reuse_previous_candidate_as_certification(tmp_path):
    minute, raw = inputs()
    output, state = tmp_path/"output", tmp_path/"state"
    write_result(output, state, raw, meta(), minute, {})
    report = write_result(output, state, raw, meta("run2", "2026-11-10T03:00:00Z"), None, None, "network failed")
    assert report["candidate_rows"] == 0 and not report["candidate_exports"]
    assert report["counts"] == {"unknown": len(raw)-1}
    retained_state = pd.read_parquet(state/"TEST/100R/GOLD/latest.parquet")
    assert retained_state.run_id.eq("run1").all()


def test_wrong_symbol_in_state_cannot_corroborate(tmp_path):
    minute, raw = inputs()
    output, state = tmp_path/"output", tmp_path/"state"
    write_result(output, state, raw, meta(), minute, {})
    path = state/"TEST/100R/GOLD/latest.parquet"
    previous = pd.read_parquet(path)
    previous["symbol"] = "OTHER"
    previous.to_parquet(path)
    report = write_result(output, state, raw, meta("run2", "2026-11-10T03:00:00Z"), minute, {})
    assert report["state_error"]
    assert not report["corroborated_exports"]


def test_offline_audit_reads_only_successful_sealed_raw_and_writes_reports(tmp_path):
    minute, raw = inputs()
    config = tmp_path/"config.json"
    config.write_text('{"jobs": []}')
    with RawArchive(tmp_path/"raw", config_path=config) as archive:
        with archive.request(source="tradingview", symbol="GOLD", broker="TEST", timeframe="100R", requested_bars=300) as capture:
            capture.frame(raw)
        try:
            with archive.request(source="tradingview", symbol="OTHER", broker="TEST", timeframe="100R", requested_bars=300) as capture:
                capture.frame(raw)
                raise ValueError("failed after frame")
        except ValueError:
            pass
    selected = successful_range_frames(archive.run_dir)
    assert len(selected) == 1 and selected[0][1]["symbol"] == "GOLD"
    minute_path, reference = tmp_path/"m1.parquet", tmp_path/"references.json"
    minute.to_parquet(minute_path)
    reference.write_text(json.dumps({"TEST:GOLD": str(minute_path)}))
    args = argparse.Namespace(raw_run=[str(archive.run_dir)], collect_summary=None, reference_map=str(reference),
                              allow_network=False, output=str(tmp_path/"quality"), state_root=str(tmp_path/"state"),
                              summary=str(tmp_path/"summary.json"), report=str(tmp_path/"report.md"))
    summary = run(args)
    assert len(summary["reports"]) == 1
    assert summary["certified_tick_true_rows"] == 0 and not summary["legacy_archive_modified"]
    report = summary["reports"][0]
    assert report["candidate_exports"]
    assert "TEST:GOLD" in Path(args.report).read_text()


def test_empty_result_does_not_crash_export(tmp_path):
    report = write_result(tmp_path/"out", tmp_path/"state", pd.DataFrame(), meta(), None, None)
    assert report["closed_rows"] == 0 and not report["candidate_exports"]
