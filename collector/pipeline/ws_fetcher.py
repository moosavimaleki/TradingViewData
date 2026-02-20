from __future__ import annotations

import asyncio
import json
import random
import re
import string
import time
from typing import Dict, List

import pandas as pd
import websockets
from websockets import exceptions as ws_exceptions

RANGE_TYPE = "BarSetRange@tv-basicstudies-72!"
RANGE_BASE_INTERVAL = "1"
WS_URL = "wss://data.tradingview.com/socket.io/websocket"
WS_ORIGIN = "https://www.tradingview.com"
AUTH_TOKEN = "unauthorized_user_token"


def _ws_frame(message: str) -> str:
    return f"~m~{len(message)}~m~{message}"


def _ws_decode(raw: str) -> List[str]:
    out: List[str] = []
    i = 0
    while i < len(raw):
        if not raw.startswith("~m~", i):
            break
        i += 3
        j = raw.find("~m~", i)
        if j == -1:
            break
        try:
            n = int(raw[i:j])
        except Exception:
            break
        start = j + 3
        end = start + n
        out.append(raw[start:end])
        i = end
    return out


def _random_id(prefix: str) -> str:
    letters = string.ascii_lowercase
    return prefix + "".join(random.choice(letters) for _ in range(12))


class TradingViewWSFetcher:
    def __init__(self, *, timeout_sec: int = 30, page_step: int = 2000) -> None:
        self.timeout_sec = int(timeout_sec)
        self.page_step = int(page_step)

    def fetch_latest_range(self, *, symbol: str, broker: str, timeframe: str, n_bars: int) -> pd.DataFrame:
        if not re.fullmatch(r"[0-9]+[rR]", str(timeframe).strip()):
            raise ValueError(f"timeframe={timeframe!r} is not a range timeframe")
        tv_symbol = f"{broker}:{symbol}"
        return asyncio.run(self._fetch_bars_ws(symbol=tv_symbol, interval=timeframe.upper(), n_bars=int(n_bars)))

    async def _fetch_bars_ws(self, *, symbol: str, interval: str, n_bars: int) -> pd.DataFrame:
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        )
        headers: Dict[str, str] = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.tradingview.com/chart/",
        }

        quote_session = _random_id("qs_")
        chart_session = _random_id("cs_")
        series_id = "s1"
        target_bars = max(1, int(n_bars))
        initial_bars = min(target_bars, 5000)

        bars_by_index: Dict[int, list] = {}
        start = time.time()

        range_match = re.fullmatch(r"([0-9]+)[rR]", str(interval).strip())
        is_range = bool(range_match)
        range_n = int(range_match.group(1)) if range_match else 0

        async def send_msg(ws, method: str, params: list) -> None:
            msg = json.dumps({"m": method, "p": params}, separators=(",", ":"))
            await ws.send(_ws_frame(msg))

        async def handle_payload(ws, payload: str) -> None:
            if payload.startswith("~h~"):
                await ws.send(_ws_frame(payload))
                return

            if "timescale_update" in payload:
                try:
                    message = json.loads(payload)
                    series = message["p"][1][series_id]["s"]
                except Exception:
                    return
                for row in series:
                    bars_by_index[int(row["i"])] = row["v"]
                return

            if is_range and ("\"m\":\"du\"" in payload or "\"m\": \"du\"" in payload or payload.startswith("{\"m\":\"du\"")):
                try:
                    message = json.loads(payload)
                    p = message.get("p")
                    if not (isinstance(p, list) and len(p) >= 2 and isinstance(p[1], dict)):
                        return
                    series = p[1].get(series_id)
                    if not isinstance(series, dict):
                        return
                    ns = series.get("ns")
                    if not isinstance(ns, dict):
                        return
                    d = ns.get("d")
                    idxs = ns.get("indexes")
                    close_time = (series.get("lbs") or {}).get("bar_close_time")
                    if not (isinstance(d, str) and isinstance(idxs, list) and close_time is not None):
                        return
                    dd = json.loads(d)
                    bars = (dd.get("data") or {}).get("bars") or []
                    if not bars:
                        return
                    b0 = bars[0]
                    v = [
                        0.0,
                        float(b0["open"]),
                        float(b0["high"]),
                        float(b0["low"]),
                        float(b0["close"]),
                        float(b0.get("volume", 0.0)),
                    ]
                    for i in idxs:
                        idx = int(i)
                        existing = bars_by_index.get(idx)
                        t = float(existing[0]) if existing else float(close_time)
                        bars_by_index[idx] = [t, v[1], v[2], v[3], v[4], v[5]]
                except Exception:
                    return

        async def recv_for(ws, seconds: int) -> None:
            t0 = time.time()
            while (time.time() - t0) < seconds and (time.time() - start) < self.timeout_sec:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=5)
                except Exception as exc:
                    if isinstance(exc, ws_exceptions.ConnectionClosed):
                        raise RuntimeError(f"websocket closed: {exc}") from exc
                    continue
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8", "replace")
                for payload in _ws_decode(raw) or [raw]:
                    await handle_payload(ws, payload)

        async with websockets.connect(
            WS_URL,
            origin=WS_ORIGIN,
            user_agent_header=user_agent,
            additional_headers=headers,
            ping_interval=None,
            max_size=None,
            open_timeout=max(8, int(self.timeout_sec)),
            close_timeout=5,
        ) as ws:
            await send_msg(ws, "set_auth_token", [AUTH_TOKEN])
            await send_msg(ws, "chart_create_session", [chart_session, ""])
            await send_msg(ws, "quote_create_session", [quote_session])
            await send_msg(
                ws,
                "quote_set_fields",
                [
                    quote_session,
                    "lp",
                    "lp_time",
                    "volume",
                    "currency_code",
                    "description",
                    "exchange",
                    "type",
                ],
            )

            resolved_symbol_id = "symbol_1"
            if is_range:
                resolve_payload = {
                    "inputs": {"phantomBars": False, "range": int(range_n)},
                    "symbol": {"adjustment": "splits", "session": "regular", "symbol": symbol},
                    "type": RANGE_TYPE,
                }
                resolve_string = "=" + json.dumps(resolve_payload, separators=(",", ":"))
                create_interval = RANGE_BASE_INTERVAL
            else:
                resolve_string = f'={{"symbol":"{symbol}","adjustment":"splits","session":"regular"}}'
                create_interval = str(interval)

            await send_msg(ws, "resolve_symbol", [chart_session, resolved_symbol_id, resolve_string])
            await send_msg(ws, "create_series", [chart_session, series_id, series_id, resolved_symbol_id, create_interval, initial_bars, ""])
            await send_msg(ws, "switch_timezone", [chart_session, "exchange"])

            await recv_for(ws, seconds=min(20, self.timeout_sec))

            if self.page_step > 0:
                stagnant_rounds = 0
                for _ in range(100):
                    if len(bars_by_index) >= target_bars:
                        break
                    if (time.time() - start) >= self.timeout_sec:
                        break
                    prev_count = len(bars_by_index)
                    need = target_bars - prev_count
                    req = min(int(self.page_step), need)
                    if req <= 0:
                        break
                    await send_msg(ws, "request_more_data", [chart_session, series_id, req])
                    await recv_for(ws, seconds=12)
                    if len(bars_by_index) <= prev_count:
                        stagnant_rounds += 1
                        if stagnant_rounds >= 3:
                            break
                    else:
                        stagnant_rounds = 0

        if not bars_by_index:
            raise RuntimeError("No bars received from TradingView websocket.")

        rows = []
        for idx in sorted(bars_by_index.keys()):
            v = bars_by_index[idx]
            rows.append(
                {
                    "bar_index": idx,
                    "timestamp": pd.to_datetime(float(v[0]), unit="s", utc=True),
                    "open": float(v[1]),
                    "high": float(v[2]),
                    "low": float(v[3]),
                    "close": float(v[4]),
                    "volume": float(v[5]) if len(v) > 5 else 0.0,
                }
            )
        return pd.DataFrame(rows)

