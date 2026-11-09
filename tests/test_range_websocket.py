from __future__ import annotations

import asyncio
import json

import pytest

from collector.pipeline import ws_fetcher


def run_snapshot(monkeypatch, *, rows=None, delta=None, completed=True, n_bars=2, raw_archive=None):
    class Clock:
        now = 0.0

        def time(self):
            return self.now

    clock = Clock()

    class Socket:
        def __init__(self):
            self.messages = []

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def send(self, raw):
            request = json.loads(ws_fetcher._ws_decode(raw)[0])
            if request["m"] != "create_series":
                return
            session, series = request["p"][:2]
            self.messages.append({"m": "timescale_update", "p": [session, {
                series: {"s": rows if rows is not None else [
                    {"i": 0, "v": [1000, 1, 2, 0, 1.5, 10]},
                    {"i": 1, "v": [1000, 2, 3, 1, 2.5, 20]},
                ]},
            }]})
            if delta:
                self.messages.append({"m": "du", "p": [session, {series: delta}]})
            if completed:
                self.messages.append({"m": "series_completed", "p": [session, series]})

        async def recv(self):
            if self.messages:
                return json.dumps(self.messages.pop(0))
            clock.now += 1000
            raise asyncio.TimeoutError

    monkeypatch.setattr(ws_fetcher.time, "time", clock.time)
    monkeypatch.setattr(ws_fetcher.websockets, "connect", lambda *args, **kwargs: Socket())
    return ws_fetcher.TradingViewWSFetcher(timeout_sec=30, raw_archive=raw_archive).fetch_latest_range(
        symbol="TEST", broker="TEST", timeframe="100R", n_bars=n_bars
    )


def test_timeout_with_some_bars_is_not_a_completed_snapshot(monkeypatch):
    with pytest.raises(RuntimeError, match="complete"):
        run_snapshot(monkeypatch, completed=False)


def test_uncompleted_history_page_cannot_reuse_initial_page_completion(monkeypatch):
    with pytest.raises(RuntimeError, match="page did not complete"):
        run_snapshot(monkeypatch, n_bars=3)


def test_missing_series_indexes_are_not_silently_accepted(monkeypatch):
    with pytest.raises(RuntimeError, match="gap"):
        run_snapshot(monkeypatch, rows=[
            {"i": 0, "v": [1000, 1, 2, 0, 1.5, 10]},
            {"i": 2, "v": [1001, 2, 3, 1, 2.5, 20]},
        ])


def test_each_delta_bar_keeps_its_own_values_and_same_second_order(monkeypatch):
    frame = run_snapshot(monkeypatch, delta={
        "ns": {"indexes": [0, 1], "d": json.dumps({"data": {"bars": [
            {"open": 1, "high": 2, "low": 0, "close": 1.75, "volume": 11},
            {"open": 2, "high": 3, "low": 1, "close": 2.75, "volume": 21},
        ]}})},
        "lbs": {"bar_close_time": 1000},
    })
    assert frame["bar_index"].tolist() == [0, 1]
    assert frame["timestamp"].nunique() == 1
    assert frame["close"].tolist() == [1.75, 2.75]
    assert frame["volume"].tolist() == [11, 21]


def test_mismatched_delta_bars_and_indexes_cannot_clone_one_bar(monkeypatch):
    with pytest.raises(RuntimeError, match="delta"):
        run_snapshot(monkeypatch, delta={
            "ns": {"indexes": [0, 1], "d": json.dumps({"data": {"bars": [
                {"open": 1, "high": 2, "low": 0, "close": 1.75, "volume": 11},
            ]}})},
            "lbs": {"bar_close_time": 1000},
        })


def test_multi_bar_delta_cannot_invent_a_shared_timestamp(monkeypatch):
    with pytest.raises(RuntimeError, match="per-bar timestamp"):
        run_snapshot(monkeypatch, rows=[], delta={
            "ns": {"indexes": [0, 1], "d": json.dumps({"data": {"bars": [
                {"open": 1, "high": 2, "low": 0, "close": 1.75, "volume": 11},
                {"open": 2, "high": 3, "low": 1, "close": 2.75, "volume": 21},
            ]}})},
            "lbs": {"bar_close_time": 1000},
        })


def test_real_capture_hook_preserves_messages_before_parser_failure(monkeypatch, tmp_path):
    import pyarrow.parquet as pq
    from collector.pipeline.raw_archive import RawArchive, verify_archive

    config = tmp_path / "config.json"
    config.write_text('{"jobs": []}')
    with pytest.raises(RuntimeError, match="delta"):
        with RawArchive(tmp_path / "raw", config_path=config) as archive:
            run_snapshot(monkeypatch, raw_archive=archive, delta={
                "ns": {"indexes": [0, 1], "d": json.dumps({"data": {"bars": [
                    {"open": 1, "high": 2, "low": 0, "close": 1.75},
                ]}})},
            })
    verify_archive(archive.run_dir)
    rows = pq.read_table(archive.run_dir / "data.parquet").to_pylist()
    messages = [json.loads(row["payload"]) for row in rows if row["kind"] == "ws_text"]
    assert [msg["m"] for msg in messages] == ["timescale_update", "du"]
    assert json.loads(rows[-1]["payload"])["status"] == "failed"
