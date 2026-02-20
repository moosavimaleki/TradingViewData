#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence
from urllib.parse import urlsplit

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_collector.sources.tv_fastpass_client import fetch_bars_ws


DEFAULT_JSON_SOURCES = [
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.json",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.json",
]

DEFAULT_TEXT_SOURCES = [
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
]

_PROBE_SETTINGS: Dict[str, Any] = {}


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Fetch and verify healthy websocket proxies for TradingView.")
    p.add_argument("--count", type=int, default=10, help="Target number of healthy proxies.")
    p.add_argument("--min-count", type=int, default=None, help="Minimum acceptable healthy proxies.")
    p.add_argument("--timeout", type=float, default=8.0, help="Per-proxy websocket timeout (seconds).")
    p.add_argument("--concurrency", type=int, default=64, help="Concurrent proxy checks.")
    p.add_argument("--max-candidates", type=int, default=800, help="Max proxy candidates to test.")
    p.add_argument(
        "--protocols",
        default="http,https,socks4,socks5",
        help="Allowed protocols (comma-separated).",
    )
    p.add_argument(
        "--progress-interval",
        type=float,
        default=5.0,
        help="Print scan progress every N seconds.",
    )
    p.add_argument(
        "--max-runtime",
        type=float,
        default=480.0,
        help="Hard timeout for the whole scan (seconds).",
    )
    p.add_argument(
        "--test-chart-url",
        default=os.getenv("TV_CHART_URL", "https://www.tradingview.com/chart/"),
        help="TradingView chart URL used for proxy validation.",
    )
    p.add_argument(
        "--test-ws-url",
        default=os.getenv("TV_WS_URL", ""),
        help="Optional websocket URL override for proxy validation.",
    )
    p.add_argument(
        "--test-ws-origin",
        default=os.getenv("TV_WS_ORIGIN", ""),
        help="Optional websocket origin override for proxy validation.",
    )
    p.add_argument(
        "--test-symbol",
        default=os.getenv("TV_PROXY_TEST_SYMBOL", "BLACKBULL:XAUUSD"),
        help="Symbol used in TradingView WS probe.",
    )
    p.add_argument(
        "--test-interval",
        default=os.getenv("TV_PROXY_TEST_INTERVAL", "1"),
        help="Interval used in TradingView WS probe (e.g. 1, 5, 1D).",
    )
    p.add_argument(
        "--test-min-bars",
        type=int,
        default=3,
        help="Minimum bars required in probe result to mark proxy healthy.",
    )
    p.add_argument("--out-file", default=".ws_proxies.txt", help="Output file with one proxy per line.")
    p.add_argument("--seed", type=int, default=1337, help="Random seed for deterministic shuffle.")
    return p.parse_args()


def _normalize_allowed_protocols(raw: str) -> set[str]:
    allowed = {x.strip().lower() for x in str(raw).split(",") if x.strip()}
    if not allowed:
        return {"http", "https", "socks4", "socks5"}
    return allowed


def _fetch_text(url: str, timeout: float = 20.0) -> str:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def _fetch_json(url: str, timeout: float = 20.0) -> Any:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _iter_raw_proxies(text: str) -> Iterable[str]:
    for line in text.splitlines():
        val = line.strip()
        if not val or val.startswith("#"):
            continue
        yield val


def _normalize_proxy(p: str) -> str:
    val = p.strip()
    if "://" not in val:
        return f"http://{val}"
    return val


def _is_valid_proxy_url(proxy: str, allowed_protocols: set[str]) -> bool:
    m = re.match(r"^([a-zA-Z0-9]+)://[^\\s]+$", proxy)
    if not m:
        return False
    proto = m.group(1).lower()
    return proto in allowed_protocols


def _dedupe_keep_order(items: Sequence[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def _protocol_rank(proto: str) -> int:
    # Prefer SOCKS, then HTTPS, then HTTP
    p = str(proto or "").lower()
    if p == "socks5":
        return 4
    if p == "socks4":
        return 3
    if p == "https":
        return 2
    if p == "http":
        return 1
    return 0


def _redact_proxy(proxy: str) -> str:
    try:
        parts = urlsplit(proxy)
        if not parts.username:
            return proxy
        host = parts.hostname or ""
        if parts.port:
            host = f"{host}:{parts.port}"
        return f"{parts.scheme}://{parts.username}:***@{host}"
    except Exception:
        return proxy


async def _check_proxy(proxy: str, timeout_sec: float) -> bool:
    try:
        async with asyncio.timeout(timeout_sec + 8):
            df = await fetch_bars_ws(
                chart_url=_PROBE_SETTINGS["chart_url"],
                ws_url=_PROBE_SETTINGS["ws_url"],
                ws_origin=_PROBE_SETTINGS["ws_origin"],
                cookie_string="",
                auth_token="unauthorized_user_token",
                symbol=_PROBE_SETTINGS["symbol"],
                interval=_PROBE_SETTINGS["interval"],
                range_type="BarSetRange@tv-basicstudies-72!",
                range_base_interval="1",
                phantom_bars=False,
                n_bars=max(5, int(_PROBE_SETTINGS["min_bars"]) + 2),
                timeout_sec=max(8, int(timeout_sec)),
                page_step=1000,
                ws_proxy=proxy,
            )
        return len(df) >= int(_PROBE_SETTINGS["min_bars"])
    except Exception:
        return False


async def _find_healthy_proxies(
    candidates: Sequence[str],
    target_count: int,
    timeout_sec: float,
    concurrency: int,
    progress_interval_sec: float,
) -> List[str]:
    good: List[str] = []
    total = len(candidates)
    tested = 0
    failed = 0
    started = time.monotonic()
    last_log = started

    sem = asyncio.Semaphore(max(1, int(concurrency)))

    async def probe(proxy: str) -> tuple[str, bool]:
        async with sem:
            ok = await _check_proxy(proxy, timeout_sec)
        return proxy, ok

    tasks = [asyncio.create_task(probe(proxy)) for proxy in candidates]

    try:
        for fut in asyncio.as_completed(tasks):
            proxy, ok = await fut
            tested += 1
            if ok and proxy not in good:
                good.append(proxy)
                print(
                    f"[proxy-scan] healthy={len(good)}/{target_count} "
                    f"proxy={_redact_proxy(proxy)}",
                    flush=True,
                )
            if not ok:
                failed += 1

            now = time.monotonic()
            if (now - last_log) >= max(1.0, float(progress_interval_sec)):
                elapsed = now - started
                print(
                    f"[proxy-scan] progress tested={tested}/{total} healthy={len(good)} "
                    f"failed={failed} elapsed={elapsed:.1f}s",
                    flush=True,
                )
                last_log = now

            if len(good) >= target_count:
                print(
                    f"[proxy-scan] target reached: {len(good)}/{target_count}. "
                    "canceling remaining checks.",
                    flush=True,
                )
                break
    finally:
        for t in tasks:
            if not t.done():
                t.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    elapsed = time.monotonic() - started
    print(
        f"[proxy-scan] finished tested={tested}/{total} healthy={len(good)} "
        f"failed={failed} elapsed={elapsed:.1f}s",
        flush=True,
    )
    return good[:target_count]


async def _run_health_scan(
    candidates: Sequence[str],
    target_count: int,
    timeout_sec: float,
    concurrency: int,
    progress_interval_sec: float,
) -> List[str]:
    loop = asyncio.get_running_loop()
    prev_handler = loop.get_exception_handler()

    def _exception_handler(_loop: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
        exc = context.get("exception")
        msg = str(context.get("message") or "")
        # Suppress noisy known failures from broken public proxies.
        if isinstance(exc, (EOFError, asyncio.InvalidStateError)):
            return
        if isinstance(exc, AttributeError) and "recv_messages" in str(exc):
            return
        if "Fatal error: protocol.data_received() call failed." in msg:
            return
        if "InvalidStateError" in msg:
            return
        if "SSLCertVerificationError" in msg and "connection_lost" in msg:
            return
        if "Connection.connection_lost(SSLCertVerifi" in msg:
            return
        _loop.default_exception_handler(context)

    loop.set_exception_handler(_exception_handler)
    try:
        return await _find_healthy_proxies(
            candidates,
            target_count,
            timeout_sec,
            concurrency,
            progress_interval_sec,
        )
    finally:
        loop.set_exception_handler(prev_handler)


def main() -> None:
    args = _parse_args()
    target_count = max(1, int(args.count))
    min_count = target_count if args.min_count is None else max(1, int(args.min_count))
    allowed_protocols = _normalize_allowed_protocols(args.protocols)
    global _PROBE_SETTINGS
    _PROBE_SETTINGS = {
        "chart_url": str(args.test_chart_url).strip(),
        "ws_url": str(args.test_ws_url).strip(),
        "ws_origin": str(args.test_ws_origin).strip(),
        "symbol": str(args.test_symbol).strip(),
        "interval": str(args.test_interval).strip(),
        "min_bars": max(1, int(args.test_min_bars)),
    }

    print(
        f"[proxy-scan] start count={target_count} min_count={min_count} timeout={args.timeout}s "
        f"concurrency={args.concurrency} max_candidates={args.max_candidates} "
        f"max_runtime={args.max_runtime}s protocols={sorted(allowed_protocols)} "
        f"probe_symbol={_PROBE_SETTINGS['symbol']} probe_interval={_PROBE_SETTINGS['interval']} "
        f"probe_min_bars={_PROBE_SETTINGS['min_bars']}",
        flush=True,
    )

    all_candidates: List[str] = []
    errors: List[str] = []
    scored_candidates: List[Dict[str, Any]] = []

    for url in DEFAULT_JSON_SOURCES:
        try:
            print(f"[proxy-scan] fetching json source: {url}", flush=True)
            payload = _fetch_json(url)
            if isinstance(payload, list):
                for item in payload:
                    if not isinstance(item, dict):
                        continue
                    proxy = _normalize_proxy(str(item.get("proxy", "")).strip())
                    proto = str(item.get("protocol", "")).lower()
                    if not proxy or not _is_valid_proxy_url(proxy, allowed_protocols):
                        continue
                    score = int(item.get("score", 0) or 0)
                    scored_candidates.append(
                        {
                            "proxy": proxy,
                            "protocol": proto,
                            "score": score,
                            "rank": _protocol_rank(proto),
                        }
                    )
        except Exception as e:
            print(f"[proxy-scan] warning source failed: {url} err={e}", flush=True)
            errors.append(f"{url}: {e}")

    for url in DEFAULT_TEXT_SOURCES:
        try:
            print(f"[proxy-scan] fetching text source: {url}", flush=True)
            txt = _fetch_text(url)
            all_candidates.extend(_iter_raw_proxies(txt))
        except Exception as e:
            print(f"[proxy-scan] warning source failed: {url} err={e}", flush=True)
            errors.append(f"{url}: {e}")

    if scored_candidates:
        scored_candidates = sorted(
            scored_candidates,
            key=lambda x: (int(x.get("rank", 0)), int(x.get("score", 0))),
            reverse=True,
        )
        filtered = _dedupe_keep_order([str(x["proxy"]) for x in scored_candidates])
    else:
        normalized = [_normalize_proxy(x) for x in all_candidates]
        filtered = [x for x in normalized if _is_valid_proxy_url(x, allowed_protocols)]
        filtered = _dedupe_keep_order(filtered)

    rnd = random.Random(int(args.seed))
    rnd.shuffle(filtered)
    if args.max_candidates and int(args.max_candidates) > 0:
        filtered = filtered[: int(args.max_candidates)]

    print(f"[proxy-scan] candidates_after_filter={len(filtered)}", flush=True)

    if not filtered:
        detail = "; ".join(errors) if errors else "no candidates after filtering"
        raise SystemExit(f"No proxy candidates found ({detail})")

    try:
        healthy = asyncio.run(
            asyncio.wait_for(
                _run_health_scan(
                    candidates=filtered,
                    target_count=target_count,
                    timeout_sec=float(args.timeout),
                    concurrency=int(args.concurrency),
                    progress_interval_sec=float(args.progress_interval),
                ),
                timeout=float(args.max_runtime),
            )
        )
    except TimeoutError:
        raise SystemExit(
            f"Proxy scan timed out after {float(args.max_runtime):.1f}s. "
            "Try lowering --count or raising --max-runtime."
        )

    out_path = Path(args.out_file).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(healthy) + ("\n" if healthy else ""), encoding="utf-8")

    print(f"candidates_tested={len(filtered)}", flush=True)
    print(f"healthy_found={len(healthy)}", flush=True)
    print(f"out_file={out_path}", flush=True)
    for p in healthy:
        print(f"healthy={p}", flush=True)

    if len(healthy) < min_count:
        raise SystemExit(
            f"Not enough healthy proxies found (need at least {min_count}, got {len(healthy)})."
        )


if __name__ == "__main__":
    main()
