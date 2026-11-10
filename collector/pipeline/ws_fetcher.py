from __future__ import annotations

import asyncio
import json
import random
import re
import string
import time
from contextlib import nullcontext
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
    def __init__(self, *, timeout_sec: int = 30, page_step: int = 2000, raw_archive=None) -> None:
        self.timeout_sec = int(timeout_sec)
        self.page_step = int(page_step)
        self.raw_archive = raw_archive

    def fetch_latest_range(self, *, symbol: str, broker: str, timeframe: str, n_bars: int) -> pd.DataFrame:
        if not re.fullmatch(r"[0-9]+[rR]", str(timeframe).strip()):
            raise ValueError(f"timeframe={timeframe!r} is not a range timeframe")
        return self._fetch_with_archive(symbol=symbol, broker=broker, interval=timeframe.upper(), n_bars=n_bars)

    def fetch_latest_time(self, *, symbol: str, broker: str, timeframe: str, n_bars: int) -> pd.DataFrame:
        """Fetch regular time bars with the same paginated websocket path.

        Unlike ``TvDatafeed.get_hist`` this can request more than 5000 bars by
        paging the chart series. Timestamps are epoch UTC and therefore do not
        inherit tvDatafeed's host-timezone parsing quirk.
        """
        if not str(timeframe).isdigit():
            raise ValueError(f"timeframe={timeframe!r} must be a minute/hour interval")
        return self._fetch_with_archive(symbol=symbol, broker=broker, interval=str(timeframe), n_bars=n_bars)

    def _fetch_with_archive(self, *, symbol: str, broker: str, interval: str, n_bars: int):
        capture = self.raw_archive.request(
            source="tradingview", symbol=symbol, broker=broker,
            timeframe=interval, requested_bars=n_bars,
        ) if self.raw_archive else nullcontext()
        with capture as raw_request:
            frame = asyncio.run(self._fetch_bars_ws(
                symbol=f"{broker}:{symbol}", interval=interval, n_bars=int(n_bars), raw_request=raw_request,
            ))
            if raw_request is not None:
                raw_request.frame(frame)
            return frame

    async def _fetch_bars_ws(self, *, symbol: str, interval: str, n_bars: int, raw_request=None) -> pd.DataFrame:
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
        series_completed = False
        start = time.time()

        range_match = re.fullmatch(r"([0-9]+)[rR]", str(interval).strip())
        is_range = bool(range_match)
        range_n = int(range_match.group(1)) if range_match else 0

        async def send_msg(ws, method: str, params: list) -> None:
            msg = json.dumps({"m": method, "p": params}, separators=(",", ":"))
            await ws.send(_ws_frame(msg))

        async def handle_payload(ws, payload: str) -> None:
            nonlocal series_completed
            if payload.startswith("~h~"):
                await ws.send(_ws_frame(payload))
                return

            try:
                message = json.loads(payload)
            except (TypeError, ValueError) as exc:
                raise RuntimeError("Invalid TradingView websocket JSON") from exc
            if not isinstance(message, dict):
                return
            method = message.get("m")
            p = message.get("p")
            if method in {"series_error", "symbol_error", "critical_error", "protocol_error"}:
                raise RuntimeError(f"TradingView {method}: {p}")
            if not isinstance(p, list) or len(p) < 2 or p[0] != chart_session:
                return
            if method == "series_completed" and p[1] == series_id:
                series_completed = True
                return
            if method not in {"timescale_update", "du"} or not isinstance(p[1], dict):
                return
            series = p[1].get(series_id)
            if not isinstance(series, dict):
                return
            if "s" in series:
                try:
                    for row in series["s"]:
                        values = row["v"]
                        if len(values) < 5:
                            raise ValueError("missing candle values")
                        bars_by_index[int(row["i"])] = values
                except (KeyError, TypeError, ValueError) as exc:
                    raise RuntimeError("Invalid TradingView series bars") from exc

            if is_range and method == "du" and "ns" in series:
                try:
                    ns = series["ns"]
                    idxs = ns["indexes"]
                    # A valid metadata-only update has d="" and no bar data.
                    # Any regular s rows above have already been applied.
                    if idxs == "nochange":
                        return
                    bars = json.loads(ns["d"])["data"]["bars"]
                    if not isinstance(idxs, list) or not isinstance(bars, list) or len(bars) != len(idxs):
                        raise ValueError("bar and index counts differ")
                    close_time = (series.get("lbs") or {}).get("bar_close_time")
                    for index, bar in zip(idxs, bars, strict=True):
                        idx = int(index)
                        existing = bars_by_index.get(idx)
                        if existing is not None:
                            timestamp = existing[0]
                        elif len(bars) == 1 and close_time is not None:
                            timestamp = close_time
                        else:
                            raise ValueError("missing per-bar timestamp")
                        bars_by_index[idx] = [
                            float(timestamp), float(bar["open"]), float(bar["high"]),
                            float(bar["low"]), float(bar["close"]), float(bar.get("volume", 0.0)),
                        ]
                except (KeyError, TypeError, ValueError) as exc:
                    raise RuntimeError(f"Invalid range delta: {exc}") from exc

        async def recv_for(ws, seconds: int) -> None:
            t0 = time.time()
            while (time.time() - t0) < seconds and (time.time() - start) < self.timeout_sec:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=5)
                except Exception as exc:
                    if isinstance(exc, ws_exceptions.ConnectionClosed):
                        raise RuntimeError(f"websocket closed: {exc}") from exc
                    continue
                if raw_request is not None:
                    raw_request.message(raw)
                if isinstance(raw, bytes):
                    raw = raw.decode("utf-8", "replace")
                for payload in _ws_decode(raw) or [raw]:
                    await handle_payload(ws, payload)
                if series_completed:
                    return

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
            if not series_completed:
                raise RuntimeError("TradingView snapshot did not complete before timeout")

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
                    series_completed = False
                    await send_msg(ws, "request_more_data", [chart_session, series_id, req])
                    await recv_for(ws, seconds=12)
                    if not series_completed:
                        raise RuntimeError("TradingView history page did not complete before timeout")
                    if len(bars_by_index) <= prev_count:
                        stagnant_rounds += 1
                        if stagnant_rounds >= 3:
                            break
                    else:
                        stagnant_rounds = 0

        if not bars_by_index:
            raise RuntimeError("No bars received from TradingView websocket.")
        indexes = sorted(bars_by_index)
        if is_range and any(right != left + 1 for left, right in zip(indexes, indexes[1:])):
            raise RuntimeError("TradingView range snapshot has gaps in bar indexes")

        rows = []
        for idx in indexes:
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
