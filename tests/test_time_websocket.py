"""The source guard's M1 reference must use the ordinary UTC websocket series."""
import json

import pandas as pd
import pytest

from collector.pipeline import ws_fetcher


def test_m1_reference_uses_ordinary_series_and_utc_epochs(monkeypatch):
    sent = []

    class Socket:
        def __init__(self):
            self.pending = []

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def send(self, payload):
            request = json.loads(ws_fetcher._ws_decode(payload)[0])
            sent.append(request)
            if request['m'] == 'create_series':
                session, series = request['p'][:2]
                for message in [
                    {'m': 'timescale_update', 'p': [session, {series: {'s': [
                        {'i': 0, 'v': [1794303900, 100, 101, 99, 100.5, 10]},
                        {'i': 1, 'v': [1794303960, 100.5, 102, 100, 101, 12]},
                    ]}}]},
                    {'m': 'series_completed', 'p': [session, series]},
                ]:
                    self.pending.append(ws_fetcher._ws_frame(json.dumps(message)))

        async def recv(self):
            return self.pending.pop(0)

    monkeypatch.setattr(ws_fetcher.websockets, 'connect', lambda *args, **kwargs: Socket())
    actual = ws_fetcher.TradingViewWSFetcher().fetch_latest_time(
        symbol='XAUUSD', broker='BLACKBULL', timeframe='1', n_bars=2)
    resolve = next(r for r in sent if r['m'] == 'resolve_symbol')
    definition = json.loads(resolve['p'][2][1:])
    assert definition['symbol'] == 'BLACKBULL:XAUUSD' and 'inputs' not in definition
    create = next(r for r in sent if r['m'] == 'create_series')
    assert create['p'][4] == '1'
    assert actual.timestamp.tolist() == [pd.Timestamp('2026-11-10T09:45:00Z'), pd.Timestamp('2026-11-10T09:46:00Z')]


def test_m1_reference_entry_point_rejects_range_intervals():
    with pytest.raises(ValueError, match='minute/hour'):
        ws_fetcher.TradingViewWSFetcher().fetch_latest_time(symbol='XAUUSD', broker='BLACKBULL',
                                                           timeframe='100R', n_bars=2)
