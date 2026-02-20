from __future__ import annotations

import asyncio
import json
import logging
import os
import random
import re
import string
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import pandas as pd
import requests
import websockets

logger = logging.getLogger(__name__)


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return str(raw).strip().lower() in {"1", "true", "yes", "on"}


def _ws_debug_enabled() -> bool:
    return _env_bool("TV_WS_DEBUG", False)


def _ws_debug(message: str) -> None:
    if _ws_debug_enabled():
        logger.info(f"[ws-debug] {message}")


def _redact_proxy(proxy: Optional[str]) -> str:
    if not proxy:
        return ""
    parsed = urlparse(proxy)
    if not parsed.username:
        return proxy
    host = parsed.hostname or ""
    if parsed.port:
        host = f"{host}:{parsed.port}"
    return f"{parsed.scheme}://{parsed.username}:***@{host}"


def _should_suppress_ws_loop_exception(context: Dict[str, object]) -> bool:
    exc = context.get("exception")
    msg = str(context.get("message") or "")
    if isinstance(exc, (EOFError, asyncio.InvalidStateError)):
        return True
    if isinstance(exc, AttributeError) and "recv_messages" in str(exc):
        return True
    if "Fatal error: protocol.data_received() call failed." in msg:
        return True
    if "InvalidStateError" in msg:
        return True
    if "SSLCertVerificationError" in msg and "connection_lost" in msg:
        return True
    if "Connection.connection_lost(SSLCertVerifi" in msg:
        return True
    return False


def extract_auth_token_and_build_time(chart_url: str, cookies: Dict[str, str]) -> tuple[str, str | None]:
    """
    Fetch the chart HTML and extract:
    - auth_token (required to send set_auth_token)
    - BUILD_TIME (used by fastpass to build the websocket `date=` query param)
    """
    # Some fastpass proxies sit behind Cloudflare and are UA-sensitive.
    # Use a browser-like UA so `cf_clearance` (if present) can be honored.
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    )
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Referer": chart_url,
    }

    resp = requests.get(chart_url, cookies=cookies, headers=headers, timeout=25)
    resp.raise_for_status()
    html = resp.text

    # Cloudflare challenge pages won't contain auth_token.
    lowered = html.lower()
    if "just a moment" in lowered and "cloudflare" in lowered:
        raise RuntimeError("Cloudflare challenge page received; cookie (cf_clearance) or user-agent likely invalid/expired.")

    m = re.search(r'"auth_token":"([^"]+)"', html)
    if not m:
        raise RuntimeError("auth_token not found in chart page. Cookie may be expired.")
    auth_token = m.group(1)

    m2 = re.search(r'BUILD_TIME\\s*=\\s*"([^"]+)"', html)
    build_time = m2.group(1) if m2 else None

    return auth_token, build_time


def extract_cookie_string(*, cookie_file: str, cookie_string: str) -> str:
    """
    Returns a raw cookie header string.

    Supports two formats in cookie_file:
    - raw "k=v; k2=v2" cookie string
    - a copied curl snippet containing: -b 'k=v; ...'
    """
    if cookie_string.strip():
        return cookie_string.strip()
    content = Path(cookie_file).read_text(encoding="utf-8")
    m = re.search(r"-b '([^']+)'", content)
    if m:
        return m.group(1).strip()
    return content.strip()


def cookie_string_to_dict(cookie_string: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for part in cookie_string.split(";"):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        out[key.strip()] = value
    return out


def extract_auth_token(chart_url: str, cookies: Dict[str, str]) -> str:
    token, _build_time = extract_auth_token_and_build_time(chart_url, cookies)
    return token


def ws_frame(message: str) -> str:
    return f"~m~{len(message)}~m~{message}"


def ws_decode(raw: str) -> List[str]:
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


def random_id(prefix: str) -> str:
    letters = string.ascii_lowercase
    return prefix + "".join(random.choice(letters) for _ in range(12))


def _extract_chart_id(chart_url: str) -> str:
    m = re.search(r"/chart/([^/]+)/?", chart_url)
    if not m:
        raise ValueError(f"Could not extract chart id from chart_url={chart_url!r}")
    return m.group(1)


def _build_fastpass_ws_url(chart_url: str) -> str:
    # Mirrors the browser WS URL observed on fastpass:
    # wss://tradingview.fastpass-panel.ir/socket.io/websocket?from=chart%2F<id>%2F&date=<iso>&type=chart&auth=sessionid
    chart_id = _extract_chart_id(chart_url)
    host = urlparse(chart_url).hostname or ""
    if not host:
        raise ValueError(f"Could not infer host from chart_url={chart_url!r}")
    iso = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%dT%H:%M:%SZ")
    iso_enc = iso.replace(":", "%3A")
    return (
        f"wss://{host}/socket.io/websocket"
        f"?from=chart%2F{chart_id}%2F&date={iso_enc}&type=chart&auth=sessionid"
    )


def infer_ws_url_and_origin(chart_url: str, ws_url: str, ws_origin: str) -> tuple[str, str]:
    if ws_url.strip():
        final_ws_url = ws_url.strip()
    else:
        host = urlparse(chart_url).hostname or ""
        # If chart is hosted on a non-official TradingView domain (e.g. fastpass proxies),
        # use that host for the websocket endpoint.
        if host and not host.endswith("tradingview.com"):
            final_ws_url = _build_fastpass_ws_url(chart_url)
        else:
            final_ws_url = "wss://data.tradingview.com/socket.io/websocket"

    if ws_origin.strip():
        origin = ws_origin.strip()
    else:
        ws_host = urlparse(final_ws_url).hostname or ""
        if ws_host and not ws_host.endswith("tradingview.com"):
            origin = f"https://{ws_host}"
        else:
            origin = "https://www.tradingview.com"

    return final_ws_url, origin


@dataclass(frozen=True)
class FetchConfig:
    chart_url: str
    ws_url: str = ""
    ws_origin: str = ""
    range_type: str = "BarSetRange@tv-basicstudies-72!"
    range_base_interval: str = "1"
    phantom_bars: bool = False
    timeout_sec: int = 30
    page_step: int = 2000


async def fetch_bars_ws(
    *,
    chart_url: str,
    ws_url: str,
    ws_origin: str,
    cookie_string: str,
    auth_token: str,
    symbol: str,
    interval: str,
    range_type: str,
    range_base_interval: str,
    phantom_bars: bool,
    n_bars: int,
    timeout_sec: int,
    page_step: int,
    ws_proxy: Optional[str] = None,
) -> pd.DataFrame:
    ws_url_final, ws_origin_final = infer_ws_url_and_origin(chart_url, ws_url, ws_origin)
    debug_enabled = _ws_debug_enabled()
    loop = asyncio.get_running_loop()
    prev_exc_handler = loop.get_exception_handler()

    def _loop_exc_handler(lp: asyncio.AbstractEventLoop, context: Dict[str, object]) -> None:
        if _should_suppress_ws_loop_exception(context):
            return
        if prev_exc_handler is not None:
            prev_exc_handler(lp, context)
        else:
            lp.default_exception_handler(context)

    loop.set_exception_handler(_loop_exc_handler)

    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    )

    headers: Dict[str, str] = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": chart_url,
    }
    if cookie_string.strip():
        headers["Cookie"] = cookie_string.strip()

    quote_session = random_id("qs_")
    chart_session = random_id("cs_")
    series_id = "s1"

    async def send_msg(ws, method: str, params: list) -> None:
        msg = json.dumps({"m": method, "p": params}, separators=(",", ":"))
        await ws.send(ws_frame(msg))

    target_bars = max(1, int(n_bars))
    initial_bars = min(target_bars, 5000)
    bars_by_index: Dict[int, list] = {}
    errors: List[str] = []
    start = time.time()

    interval_raw = str(interval).strip()
    range_match = re.fullmatch(r"([0-9]+)[rR]", interval_raw)
    is_range_bars = bool(range_match)
    range_n = int(range_match.group(1)) if range_match else 0
    create_interval = ""

    if debug_enabled:
        _ws_debug(
            "start "
            f"ws_url={ws_url_final} origin={ws_origin_final} chart_url={chart_url} "
            f"symbol={symbol} interval={interval_raw} target_bars={target_bars} "
            f"timeout={timeout_sec}s page_step={page_step} proxy={_redact_proxy(ws_proxy)}"
        )

    debug_payload_seen = 0
    debug_last_status_log = time.monotonic()

    def _maybe_log_status(reason: str) -> None:
        nonlocal debug_last_status_log
        if not debug_enabled:
            return
        now = time.monotonic()
        if (now - debug_last_status_log) >= 3.0:
            _ws_debug(
                f"{reason} bars_collected={len(bars_by_index)} "
                f"errors={len(errors)} elapsed={now - start:.1f}s"
            )
            debug_last_status_log = now

    async def handle_payload(ws, payload: str) -> None:
        nonlocal debug_payload_seen
        if debug_enabled:
            debug_payload_seen += 1
            if debug_payload_seen <= 8 or debug_payload_seen % 50 == 0:
                sample = payload[:180].replace("\n", "\\n")
                _ws_debug(f"recv_payload#{debug_payload_seen} sample={sample}")

        if payload.startswith("~h~"):
            # TradingView-style heartbeat: echo back the framed heartbeat payload.
            await ws.send(ws_frame(payload))
            _maybe_log_status("heartbeat_echo")
            return

        if "timescale_update" in payload:
            try:
                message = json.loads(payload)
                series = message["p"][1][series_id]["s"]
            except Exception:
                return
            for row in series:
                bars_by_index[int(row["i"])] = row["v"]
            _maybe_log_status("timescale_update")
            return

        if is_range_bars and ("\"m\":\"du\"" in payload or "\"m\": \"du\"" in payload or payload.startswith("{\"m\":\"du\"")):
            # Range bars often send incremental updates via `du` with ns: { d: \"{...}\", indexes: [...] }.
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
                    # Prefer keeping the original bar time (often sub-second) from timescale_update.
                    # If we don't have it yet, fall back to bar_close_time seconds.
                    t = float(existing[0]) if existing else float(close_time)
                    v2 = [t, v[1], v[2], v[3], v[4], v[5]]
                    bars_by_index[idx] = v2
                _maybe_log_status("range_du_update")
            except Exception:
                return

        if "critical_error" in payload or "symbol_error" in payload:
            errors.append(payload[:400])
            if debug_enabled:
                _ws_debug(f"error_payload sample={payload[:220]}")

    async def recv_for(ws, seconds: int) -> None:
        t0 = time.time()
        while (time.time() - t0) < seconds and (time.time() - start) < timeout_sec:
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=5)
            except Exception as e:
                if debug_enabled:
                    _ws_debug(f"recv_wait error={type(e).__name__}: {e}")
                continue
            if isinstance(raw, bytes):
                raw = raw.decode("utf-8", "replace")
            for payload in ws_decode(raw) or [raw]:
                await handle_payload(ws, payload)

    try:
        async with websockets.connect(
            ws_url_final,
            origin=ws_origin_final,
            user_agent_header=user_agent,
            additional_headers=headers,
            proxy=(ws_proxy or None),
            ping_interval=None,
            max_size=None,
        ) as ws:
            if debug_enabled:
                _ws_debug("websocket_handshake_ok")
            await send_msg(ws, "set_auth_token", [auth_token])
            await send_msg(ws, "chart_create_session", [chart_session, ""])
            await send_msg(ws, "quote_create_session", [quote_session])
            await send_msg(
                ws,
                "quote_set_fields",
                [
                    quote_session,
                    "ch",
                    "chp",
                    "current_session",
                    "description",
                    "exchange",
                    "is_tradable",
                    "lp",
                    "lp_time",
                    "minmov",
                    "minmove2",
                    "original_name",
                    "pricescale",
                    "pro_name",
                    "short_name",
                    "type",
                    "update_mode",
                    "volume",
                    "currency_code",
                ],
            )
            resolved_symbol_id = "symbol_1"
            if is_range_bars:
                resolve_payload = {
                    "inputs": {"phantomBars": bool(phantom_bars), "range": int(range_n)},
                    "symbol": {"adjustment": "splits", "session": "regular", "symbol": symbol},
                    "type": range_type,
                }
                resolve_string = "=" + json.dumps(resolve_payload, separators=(",", ":"))
                create_interval = str(range_base_interval)
            else:
                resolve_string = f'={{"symbol":"{symbol}","adjustment":"splits","session":"regular"}}'
                create_interval = str(interval_raw)

            await send_msg(ws, "resolve_symbol", [chart_session, resolved_symbol_id, resolve_string])
            await send_msg(ws, "create_series", [chart_session, series_id, series_id, resolved_symbol_id, create_interval, initial_bars, ""])
            await send_msg(ws, "switch_timezone", [chart_session, "exchange"])

            # Consume initial batch.
            await recv_for(ws, seconds=min(20, timeout_sec))

            # Backfill older bars in pages.
            if page_step > 0:
                stagnant_rounds = 0
                for _ in range(100):
                    if len(bars_by_index) >= target_bars:
                        if debug_enabled:
                            _ws_debug("target_bars_reached_in_backfill")
                        break
                    if (time.time() - start) >= timeout_sec:
                        if debug_enabled:
                            _ws_debug("timeout_reached_during_backfill")
                        break
                    prev_count = len(bars_by_index)
                    need = target_bars - prev_count
                    req = min(int(page_step), need)
                    if req <= 0:
                        break
                    if debug_enabled:
                        _ws_debug(f"request_more_data req={req} prev_count={prev_count}")
                    await send_msg(ws, "request_more_data", [chart_session, series_id, req])
                    await recv_for(ws, seconds=18)
                    if len(bars_by_index) <= prev_count:
                        stagnant_rounds += 1
                        if debug_enabled:
                            _ws_debug(f"backfill_stagnant_round={stagnant_rounds} bars={len(bars_by_index)}")
                        if stagnant_rounds >= 3:
                            break
                    else:
                        stagnant_rounds = 0
    finally:
        loop.set_exception_handler(prev_exc_handler)

    if not bars_by_index:
        error_text = errors[0] if errors else "No explicit error payload."
        if debug_enabled:
            _ws_debug(f"no_bars_received error_text={error_text}")
        raise RuntimeError(f"No bars received from websocket. sample_error={error_text}")

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

    if debug_enabled:
        first_idx = rows[0]["bar_index"] if rows else None
        last_idx = rows[-1]["bar_index"] if rows else None
        _ws_debug(
            f"done bars={len(rows)} first_idx={first_idx} last_idx={last_idx} "
            f"elapsed={time.time() - start:.1f}s"
        )

    return pd.DataFrame(rows)
