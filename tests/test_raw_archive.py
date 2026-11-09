from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
import pytest
from pandas.testing import assert_frame_equal

from collector.pipeline.raw_archive import RawArchive, RawArchiveError, finalize_archive, verify_archive
from scripts.recover_raw_archive import recover_request


@pytest.fixture
def config(tmp_path):
    path = tmp_path / "jobs.json"
    path.write_text('{"jobs": []}', encoding="utf-8")
    return path


def request(archive, symbol="TEST", timeframe="100R"):
    return archive.request(source="tradingview", symbol=symbol, broker="BROKER",
                           timeframe=timeframe, requested_bars=5000)


def test_all_symbols_share_one_archive_and_recovery_is_lossless(tmp_path, config):
    frame = pd.DataFrame({
        "bar_index": [11, 12, 13, 14],
        "close": [1.2345678901234567, -0.0, float("nan"), 1.2345678901234567],
    }, index=pd.DatetimeIndex(["2026-01-01T00:00:00Z"] * 4, name="timestamp"))
    wire = b'~m~8~m~invalid\xff'
    with RawArchive(tmp_path / "raw", config_path=config) as archive:
        with request(archive, "AAA") as capture:
            capture.message(wire)
            capture.message(wire)  # Identical messages and candles are never deduplicated.
            capture.frame(frame)
        with request(archive, "BBB", "1m") as capture:
            capture.frame(frame.iloc[:2])
    manifest = verify_archive(archive.run_dir)
    assert manifest["events"] == 9
    rows = pq.read_table(archive.run_dir / "data.parquet").to_pylist()
    assert [r["payload"] for r in rows if r["kind"] == "ws_bytes"] == [wire, wire]
    assert {r["symbol"] for r in rows if r["kind"] == "frame_arrow"} == {"AAA", "BBB"}
    assert rows[0]["payload"] == config.read_bytes()
    recovered = recover_request(archive.run_dir, "r000001", tmp_path / "recovered")
    restored = pd.read_parquet(next(p for p in recovered if p.name.startswith("frame-")))
    assert_frame_equal(restored, frame)
    assert restored["bar_index"].tolist() == [11, 12, 13, 14]
    with pytest.raises(FileExistsError):
        recover_request(archive.run_dir, "r000001", tmp_path / "recovered")


def test_reruns_and_sealed_archives_are_never_overwritten(tmp_path, config, monkeypatch):
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    monkeypatch.setenv("GITHUB_RUN_ATTEMPT", "1")
    with RawArchive(tmp_path / "raw", config_path=config) as first:
        with request(first) as capture:
            capture.message("first snapshot")
    before = (first.run_dir / "data.parquet").read_bytes()
    with RawArchive(tmp_path / "raw", config_path=config) as second:
        with request(second) as capture:
            capture.message("second snapshot")
    assert first.run_dir != second.run_dir
    first.finalize()
    assert (first.run_dir / "data.parquet").read_bytes() == before
    with pytest.raises(RawArchiveError, match="sealed"):
        first.record({}, "extra", b"cannot append")


def test_interrupted_run_can_be_sealed_from_already_durable_fragments(tmp_path, config):
    archive = RawArchive(tmp_path / "raw", config_path=config)
    capture = request(archive).__enter__()
    capture.message("received before crash")
    (archive.run_dir / "parts" / "999999999999.tmp").write_bytes(b"partial write")
    manifest = finalize_archive(archive.run_dir)
    assert manifest["events"] == 3
    rows = pq.read_table(archive.run_dir / "data.parquet").to_pylist()
    assert rows[-1]["payload"] == b"received before crash"
    assert not any(row["kind"] == "request_end" for row in rows)


def test_parser_failure_still_seals_received_messages(tmp_path, config):
    with pytest.raises(ValueError, match="parser failed"):
        with RawArchive(tmp_path / "raw", config_path=config) as archive:
            with request(archive) as capture:
                capture.message('{"unknown": "future message format"}')
                raise ValueError("parser failed")
    verify_archive(archive.run_dir)
    rows = pq.read_table(archive.run_dir / "data.parquet").to_pylist()
    assert rows[-2]["payload"] == b'{"unknown": "future message format"}'
    assert json.loads(rows[-1]["payload"])["status"] == "failed"


def test_failed_raw_write_stops_capture_and_retains_prior_events(tmp_path, config, monkeypatch):
    archive = RawArchive(tmp_path / "raw", config_path=config)
    capture = request(archive).__enter__()
    def fail_write(*args, **kwargs):
        raise OSError("disk full")
    with monkeypatch.context() as patch:
        patch.setattr(pq, "write_table", fail_write)
        with pytest.raises(RawArchiveError):
            capture.message("must not be processed")
    assert archive.broken
    manifest = archive.finalize()
    assert manifest["events"] == 2  # Config and request start are still recoverable.


def test_corrupted_sealed_archive_is_rejected_without_rewriting_it(tmp_path, config):
    with RawArchive(tmp_path / "raw", config_path=config) as archive:
        with request(archive) as capture:
            capture.message("original")
    path = archive.run_dir / "data.parquet"
    path.write_bytes(path.read_bytes()[:-5] + b"broken")
    corrupted = path.read_bytes()
    with pytest.raises(RawArchiveError, match="checksum"):
        finalize_archive(archive.run_dir)
    assert path.read_bytes() == corrupted


def test_compression_keeps_identical_packets_without_repeating_their_storage_cost(tmp_path, config):
    payload = json.dumps({"bars": [[i, 1234.123456789, 1235.5, 1230.0, 1231.0, 500] for i in range(500)]})
    with RawArchive(tmp_path / "raw", config_path=config) as archive:
        for symbol in ("AAA", "BBB", "CCC"):
            with request(archive, symbol) as capture:
                capture.message(payload)
    manifest = verify_archive(archive.run_dir)
    assert manifest["bytes"] < len(payload.encode()) * 3
    rows = pq.read_table(archive.run_dir / "data.parquet").to_pylist()
    assert [r["payload"] for r in rows if r["kind"] == "ws_text"] == [payload.encode()] * 3
