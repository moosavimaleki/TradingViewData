#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import random
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

import requests
import websockets


DEFAULT_JSON_SOURCES = [
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.json",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.json",
]

DEFAULT_TEXT_SOURCES = [
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt",
]

TEST_WS_URL = "wss://data.tradingview.com/socket.io/websocket"
TEST_ORIGIN = "https://www.tradingview.com"
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
)


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


async def _check_proxy(proxy: str, timeout_sec: float) -> bool:
    try:
        async with asyncio.timeout(timeout_sec):
            async with websockets.connect(
                TEST_WS_URL,
                origin=TEST_ORIGIN,
                user_agent_header=UA,
                proxy=proxy,
                ping_interval=None,
                close_timeout=2,
                max_size=1024 * 1024,
            ):
                return True
    except Exception:
        return False


async def _find_healthy_proxies(
    candidates: Sequence[str],
    target_count: int,
    timeout_sec: float,
    concurrency: int,
) -> List[str]:
    good: List[str] = []
    q: asyncio.Queue[str] = asyncio.Queue()
    lock = asyncio.Lock()

    for c in candidates:
        q.put_nowait(c)

    async def worker() -> None:
        while True:
            if q.empty():
                return
            proxy = await q.get()
            try:
                async with lock:
                    if len(good) >= target_count:
                        return
                ok = await _check_proxy(proxy, timeout_sec)
                if ok:
                    async with lock:
                        if proxy not in good and len(good) < target_count:
                            good.append(proxy)
            finally:
                q.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(max(1, int(concurrency)))]
    await q.join()
    for w in workers:
        w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)
    return good


async def _run_health_scan(
    candidates: Sequence[str],
    target_count: int,
    timeout_sec: float,
    concurrency: int,
) -> List[str]:
    loop = asyncio.get_running_loop()

    def _exception_handler(_loop: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
        exc = context.get("exception")
        msg = str(context.get("message") or "")
        # Suppress noisy known failures from broken public proxies.
        if isinstance(exc, (EOFError, asyncio.InvalidStateError)):
            return
        if "Fatal error: protocol.data_received() call failed." in msg:
            return
        if "InvalidStateError" in msg:
            return
        _loop.default_exception_handler(context)

    loop.set_exception_handler(_exception_handler)
    return await _find_healthy_proxies(candidates, target_count, timeout_sec, concurrency)


def main() -> None:
    args = _parse_args()
    target_count = max(1, int(args.count))
    min_count = target_count if args.min_count is None else max(1, int(args.min_count))
    allowed_protocols = _normalize_allowed_protocols(args.protocols)

    all_candidates: List[str] = []
    errors: List[str] = []
    scored_candidates: List[Dict[str, Any]] = []

    for url in DEFAULT_JSON_SOURCES:
        try:
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
            errors.append(f"{url}: {e}")

    for url in DEFAULT_TEXT_SOURCES:
        try:
            txt = _fetch_text(url)
            all_candidates.extend(_iter_raw_proxies(txt))
        except Exception as e:
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

    if not filtered:
        detail = "; ".join(errors) if errors else "no candidates after filtering"
        raise SystemExit(f"No proxy candidates found ({detail})")

    healthy = asyncio.run(
        _run_health_scan(
            candidates=filtered,
            target_count=target_count,
            timeout_sec=float(args.timeout),
            concurrency=int(args.concurrency),
        )
    )

    out_path = Path(args.out_file).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(healthy) + ("\n" if healthy else ""), encoding="utf-8")

    print(f"candidates_tested={len(filtered)}")
    print(f"healthy_found={len(healthy)}")
    print(f"out_file={out_path}")
    for p in healthy:
        print(f"healthy={p}")

    if len(healthy) < min_count:
        raise SystemExit(
            f"Not enough healthy proxies found (need at least {min_count}, got {len(healthy)})."
        )


if __name__ == "__main__":
    main()
