#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import os
import socket
import ssl
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlparse

import requests
import websockets

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_collector.sources.tv_fastpass_client import fetch_bars_ws, infer_ws_url_and_origin


DEFAULT_DNS_HOSTS = [
    "www.tradingview.com",
    "data.tradingview.com",
    "s.tradingview.com",
    "scanner.tradingview.com",
    "www.google.com",
]

DEFAULT_HTTP_URLS = [
    "https://www.tradingview.com/",
    "https://www.tradingview.com/chart/",
    "https://data.tradingview.com/",
    "https://www.google.com/",
]

DEFAULT_WS_CONTROL_URLS = [
    "wss://echo.websocket.events/",
    "wss://ws.postman-echo.com/raw",
    "wss://ws.ifelse.io",
]

DEFAULT_PUBLIC_IP_URLS = [
    ("ipify", "https://api.ipify.org?format=json"),
    ("ifconfig.me", "https://ifconfig.me/ip"),
    ("ipinfo.io", "https://ipinfo.io/ip"),
]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _log(msg: str) -> None:
    print(f"[tv-diag] {msg}", flush=True)


def _safe_err(exc: Exception) -> Dict[str, str]:
    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": "".join(traceback.format_exception_only(type(exc), exc)).strip(),
    }


def _redact_proxy(proxy: str) -> str:
    try:
        p = urlparse(proxy)
        if not p.username:
            return proxy
        host = p.hostname or ""
        if p.port:
            host = f"{host}:{p.port}"
        return f"{p.scheme}://{p.username}:***@{host}"
    except Exception:
        return proxy


def _run_cmd(cmd: List[str], timeout_sec: float = 20.0) -> Dict[str, Any]:
    started = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": int(proc.returncode),
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "elapsed_sec": round(time.monotonic() - started, 3),
            "cmd": cmd,
        }
    except Exception as exc:
        return {
            "ok": False,
            "returncode": None,
            "error": _safe_err(exc),
            "elapsed_sec": round(time.monotonic() - started, 3),
            "cmd": cmd,
        }


def _discover_public_ip(timeout_sec: float) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for name, url in DEFAULT_PUBLIC_IP_URLS:
        started = time.monotonic()
        item: Dict[str, Any] = {"name": name, "url": url}
        try:
            resp = requests.get(url, timeout=timeout_sec, headers={"User-Agent": "tv-diag/1.0"})
            item["status_code"] = int(resp.status_code)
            text = resp.text.strip()
            if "json" in (resp.headers.get("content-type", "").lower()):
                try:
                    payload = resp.json()
                    item["ip"] = str(payload.get("ip") or payload)
                except Exception:
                    item["ip"] = text
            else:
                item["ip"] = text
            item["ok"] = True
        except Exception as exc:
            item["ok"] = False
            item["error"] = _safe_err(exc)
        item["elapsed_sec"] = round(time.monotonic() - started, 3)
        out.append(item)
    return out


def _dns_tcp_tls_probe(host: str, port: int = 443, timeout_sec: float = 8.0) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "host": host,
        "port": int(port),
        "dns_ok": False,
        "tcp_ok": False,
        "tls_ok": False,
    }

    dns_started = time.monotonic()
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        ips = sorted({info[4][0] for info in infos if info and info[4]})
        result["dns_ok"] = True
        result["ips"] = ips
    except Exception as exc:
        result["dns_error"] = _safe_err(exc)
    result["dns_elapsed_sec"] = round(time.monotonic() - dns_started, 3)

    if not result["dns_ok"]:
        return result

    tcp_started = time.monotonic()
    try:
        with socket.create_connection((host, port), timeout=timeout_sec) as sock:
            result["tcp_ok"] = True
            result["remote_ip"] = sock.getpeername()[0]
            result["local_ip"] = sock.getsockname()[0]
    except Exception as exc:
        result["tcp_error"] = _safe_err(exc)
    result["tcp_elapsed_sec"] = round(time.monotonic() - tcp_started, 3)

    tls_started = time.monotonic()
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout_sec) as raw_sock:
            with ctx.wrap_socket(raw_sock, server_hostname=host) as tls_sock:
                cert = tls_sock.getpeercert()
                san_dns = [name for kind, name in cert.get("subjectAltName", []) if kind == "DNS"]
                result["tls_ok"] = True
                result["tls_version"] = tls_sock.version()
                cipher = tls_sock.cipher() or ("", "", 0)
                result["tls_cipher"] = cipher[0]
                result["tls_san_sample"] = san_dns[:20]
    except Exception as exc:
        result["tls_error"] = _safe_err(exc)
    result["tls_elapsed_sec"] = round(time.monotonic() - tls_started, 3)

    return result


def _http_probe(url: str, timeout_sec: float = 15.0) -> Dict[str, Any]:
    started = time.monotonic()
    out: Dict[str, Any] = {"url": url}
    try:
        resp = requests.get(
            url,
            timeout=timeout_sec,
            allow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
                )
            },
        )
        out["ok"] = True
        out["status_code"] = int(resp.status_code)
        out["final_url"] = resp.url
        out["history_codes"] = [int(r.status_code) for r in resp.history]
        out["content_type"] = resp.headers.get("content-type", "")
        out["server"] = resp.headers.get("server", "")
        out["cf_ray"] = resp.headers.get("cf-ray", "")
        out["body_sample"] = resp.text[:200].replace("\n", "\\n")
    except Exception as exc:
        out["ok"] = False
        out["error"] = _safe_err(exc)
    out["elapsed_sec"] = round(time.monotonic() - started, 3)
    return out


async def _ws_echo_probe(url: str, timeout_sec: float, proxy: str | None = None) -> Dict[str, Any]:
    out: Dict[str, Any] = {"url": url, "proxy": _redact_proxy(proxy) if proxy else ""}
    payload = f"tv-diag-{int(time.time())}"
    started = time.monotonic()
    try:
        async with websockets.connect(
            url,
            open_timeout=timeout_sec,
            close_timeout=min(5, timeout_sec),
            ping_interval=None,
            proxy=proxy or None,
            max_size=None,
        ) as ws:
            out["handshake_ok"] = True
            await ws.send(payload)
            recv_raw = await asyncio.wait_for(ws.recv(), timeout=timeout_sec)
            if isinstance(recv_raw, bytes):
                recv = recv_raw.decode("utf-8", "replace")
            else:
                recv = str(recv_raw)
            out["recv_sample"] = recv[:200]
            out["echo_ok"] = payload in recv
            out["ok"] = bool(out["echo_ok"])
    except Exception as exc:
        out["ok"] = False
        out["handshake_ok"] = False
        out["error"] = _safe_err(exc)
    out["elapsed_sec"] = round(time.monotonic() - started, 3)
    return out


async def _tv_handshake_probe(
    *,
    ws_url: str,
    ws_origin: str,
    chart_url: str,
    timeout_sec: float,
    proxy: str | None = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "ws_url": ws_url,
        "ws_origin": ws_origin,
        "chart_url": chart_url,
        "proxy": _redact_proxy(proxy) if proxy else "",
    }
    started = time.monotonic()
    headers = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": chart_url,
    }
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    )
    try:
        async with websockets.connect(
            ws_url,
            origin=ws_origin,
            user_agent_header=user_agent,
            additional_headers=headers,
            proxy=proxy or None,
            open_timeout=timeout_sec,
            close_timeout=min(5, timeout_sec),
            ping_interval=None,
            max_size=None,
        ):
            out["ok"] = True
    except Exception as exc:
        out["ok"] = False
        out["error"] = _safe_err(exc)
    out["elapsed_sec"] = round(time.monotonic() - started, 3)
    return out


async def _tv_data_probe(
    *,
    chart_url: str,
    ws_url: str,
    ws_origin: str,
    symbol: str,
    interval: str,
    timeout_sec: int,
    n_bars: int,
    proxy: str | None = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "chart_url": chart_url,
        "ws_url": ws_url,
        "ws_origin": ws_origin,
        "symbol": symbol,
        "interval": interval,
        "n_bars": int(n_bars),
        "proxy": _redact_proxy(proxy) if proxy else "",
    }
    started = time.monotonic()
    try:
        df = await fetch_bars_ws(
            chart_url=chart_url,
            ws_url=ws_url,
            ws_origin=ws_origin,
            cookie_string="",
            auth_token="unauthorized_user_token",
            symbol=symbol,
            interval=interval,
            range_type="BarSetRange@tv-basicstudies-72!",
            range_base_interval="1",
            phantom_bars=False,
            n_bars=max(3, int(n_bars)),
            timeout_sec=max(8, int(timeout_sec)),
            page_step=1000,
            ws_proxy=proxy or None,
        )
        out["ok"] = True
        out["bars"] = int(len(df))
        if not df.empty and "timestamp" in df.columns:
            out["first_ts"] = str(df["timestamp"].min())
            out["last_ts"] = str(df["timestamp"].max())
    except Exception as exc:
        out["ok"] = False
        out["error"] = _safe_err(exc)
    out["elapsed_sec"] = round(time.monotonic() - started, 3)
    return out


def _normalize_ws_targets(chart_url: str, ws_url: str, ws_origin: str, extra_tv_ws_urls: List[str]) -> List[Dict[str, str]]:
    inferred_url, inferred_origin = infer_ws_url_and_origin(chart_url, ws_url, ws_origin)
    candidates: List[Dict[str, str]] = [
        {
            "name": "inferred",
            "ws_url": inferred_url,
            "ws_origin": inferred_origin,
        },
        {
            "name": "official_data",
            "ws_url": "wss://data.tradingview.com/socket.io/websocket",
            "ws_origin": "https://www.tradingview.com",
        },
    ]

    for raw in extra_tv_ws_urls:
        val = str(raw).strip()
        if not val:
            continue
        candidates.append(
            {
                "name": "extra",
                "ws_url": val,
                "ws_origin": ws_origin.strip() or "https://www.tradingview.com",
            }
        )

    dedup: List[Dict[str, str]] = []
    seen = set()
    for item in candidates:
        key = (item["ws_url"].strip(), item["ws_origin"].strip())
        if key in seen:
            continue
        seen.add(key)
        dedup.append(item)
    return dedup


def _read_lines(path: Path) -> List[str]:
    if not path.exists():
        return []
    out: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        val = line.strip()
        if val:
            out.append(val)
    return out


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Deep diagnostics for TradingView connectivity on GitHub Actions.")
    p.add_argument("--symbol", default=os.getenv("TV_PROXY_TEST_SYMBOL", "BLACKBULL:XAUUSD"))
    p.add_argument("--interval", default=os.getenv("TV_PROXY_TEST_INTERVAL", "1"))
    p.add_argument("--chart-url", default=os.getenv("TV_CHART_URL", "https://www.tradingview.com/chart/"))
    p.add_argument("--ws-url", default=os.getenv("TV_WS_URL", ""))
    p.add_argument("--ws-origin", default=os.getenv("TV_WS_ORIGIN", ""))
    p.add_argument("--dns-timeout", type=float, default=8.0)
    p.add_argument("--http-timeout", type=float, default=15.0)
    p.add_argument("--probe-timeout", type=int, default=16)
    p.add_argument("--probe-bars", type=int, default=5)
    p.add_argument("--proxy-count", type=int, default=10)
    p.add_argument("--proxy-min-count", type=int, default=1)
    p.add_argument("--proxy-timeout", type=float, default=8.0)
    p.add_argument("--proxy-concurrency", type=int, default=64)
    p.add_argument("--proxy-max-candidates", type=int, default=1000)
    p.add_argument("--proxy-max-runtime", type=float, default=500.0)
    p.add_argument("--proxy-test-limit", type=int, default=4)
    p.add_argument("--proxy-out-file", default=".diag_ws_proxies.txt")
    p.add_argument("--out-json", default="tv_diag_report.json")
    p.add_argument("--skip-proxy-discovery", action="store_true")
    p.add_argument("--skip-proxy-tests", action="store_true")
    p.add_argument("--dns-host", action="append", default=[])
    p.add_argument("--http-url", action="append", default=[])
    p.add_argument("--ws-control-url", action="append", default=[])
    p.add_argument("--tv-ws-url", action="append", default=[])
    return p.parse_args()


async def _run_async_checks(args: argparse.Namespace, report: Dict[str, Any]) -> None:
    _log("running websocket control probes (no proxy)")
    control_urls = DEFAULT_WS_CONTROL_URLS + list(args.ws_control_url or [])
    control_seen = set()
    ws_controls: List[str] = []
    for url in control_urls:
        val = str(url).strip()
        if not val or val in control_seen:
            continue
        control_seen.add(val)
        ws_controls.append(val)

    for url in ws_controls:
        _log(f"ws control probe: {url}")
        report["ws_control"].append(await _ws_echo_probe(url=url, timeout_sec=float(args.probe_timeout), proxy=None))

    _log("running TradingView direct websocket probes")
    tv_targets = _normalize_ws_targets(
        chart_url=str(args.chart_url).strip(),
        ws_url=str(args.ws_url).strip(),
        ws_origin=str(args.ws_origin).strip(),
        extra_tv_ws_urls=list(args.tv_ws_url or []),
    )

    report["tv_targets"] = tv_targets
    for target in tv_targets:
        ws_url = target["ws_url"]
        ws_origin = target["ws_origin"]
        _log(f"tv handshake probe: ws_url={ws_url} origin={ws_origin}")
        handshake = await _tv_handshake_probe(
            ws_url=ws_url,
            ws_origin=ws_origin,
            chart_url=str(args.chart_url).strip(),
            timeout_sec=float(args.probe_timeout),
            proxy=None,
        )
        handshake["target_name"] = target.get("name", "")
        handshake["check"] = "handshake"
        report["tv_direct"].append(handshake)

        _log(f"tv data probe: ws_url={ws_url} symbol={args.symbol} interval={args.interval}")
        data_probe = await _tv_data_probe(
            chart_url=str(args.chart_url).strip(),
            ws_url=ws_url,
            ws_origin=ws_origin,
            symbol=str(args.symbol).strip(),
            interval=str(args.interval).strip(),
            timeout_sec=int(args.probe_timeout),
            n_bars=int(args.probe_bars),
            proxy=None,
        )
        data_probe["target_name"] = target.get("name", "")
        data_probe["check"] = "data_probe"
        report["tv_direct"].append(data_probe)

    if args.skip_proxy_discovery:
        _log("proxy discovery skipped")
        report["proxy_discovery"] = {"skipped": True, "proxies": []}
    else:
        _log("discovering free proxies with existing selector script")
        proxy_cmd = [
            sys.executable,
            "scripts/select_ws_proxies.py",
            "--count",
            str(max(1, int(args.proxy_count))),
            "--min-count",
            str(max(1, int(args.proxy_min_count))),
            "--timeout",
            str(float(args.proxy_timeout)),
            "--concurrency",
            str(max(1, int(args.proxy_concurrency))),
            "--max-candidates",
            str(max(1, int(args.proxy_max_candidates))),
            "--progress-interval",
            "5",
            "--max-runtime",
            str(float(args.proxy_max_runtime)),
            "--test-symbol",
            str(args.symbol).strip(),
            "--test-interval",
            str(args.interval).strip(),
            "--test-min-bars",
            "3",
            "--out-file",
            str(args.proxy_out_file).strip(),
        ]
        discovery = _run_cmd(proxy_cmd, timeout_sec=float(args.proxy_max_runtime) + 120.0)
        proxy_file = PROJECT_ROOT / str(args.proxy_out_file).strip()
        proxies = _read_lines(proxy_file)
        discovery["proxies"] = proxies
        discovery["proxy_count"] = len(proxies)
        report["proxy_discovery"] = discovery

    if args.skip_proxy_tests:
        _log("proxy tests skipped")
        report["proxy_tests"] = []
        return

    proxies = list((report.get("proxy_discovery") or {}).get("proxies") or [])
    proxy_limit = max(0, int(args.proxy_test_limit))
    if proxy_limit:
        proxies = proxies[:proxy_limit]
    if not proxies:
        _log("no proxies available for detailed tests")
        return

    _log(f"running detailed tests for {len(proxies)} proxies")
    ws_control_target = ws_controls[0] if ws_controls else DEFAULT_WS_CONTROL_URLS[0]
    tv_target = None
    for item in report.get("tv_targets") or []:
        if item.get("ws_url"):
            tv_target = item
            break
    if not tv_target:
        tv_target = {
            "ws_url": "wss://data.tradingview.com/socket.io/websocket",
            "ws_origin": "https://www.tradingview.com",
            "name": "fallback",
        }

    for proxy in proxies:
        masked = _redact_proxy(proxy)
        _log(f"proxy test: {masked}")
        item: Dict[str, Any] = {
            "proxy": masked,
            "raw_proxy": proxy,
        }
        item["control_ws"] = await _ws_echo_probe(
            url=ws_control_target,
            timeout_sec=float(args.probe_timeout),
            proxy=proxy,
        )
        item["tv_handshake"] = await _tv_handshake_probe(
            ws_url=str(tv_target["ws_url"]),
            ws_origin=str(tv_target["ws_origin"]),
            chart_url=str(args.chart_url).strip(),
            timeout_sec=float(args.probe_timeout),
            proxy=proxy,
        )
        item["tv_data_probe"] = await _tv_data_probe(
            chart_url=str(args.chart_url).strip(),
            ws_url=str(tv_target["ws_url"]),
            ws_origin=str(tv_target["ws_origin"]),
            symbol=str(args.symbol).strip(),
            interval=str(args.interval).strip(),
            timeout_sec=int(args.probe_timeout),
            n_bars=int(args.probe_bars),
            proxy=proxy,
        )
        report["proxy_tests"].append(item)


def _build_summary(report: Dict[str, Any]) -> Dict[str, Any]:
    public_ip_ok = sum(1 for x in report.get("public_ip", []) if x.get("ok"))
    dns_ok = sum(1 for x in report.get("dns_tcp_tls", []) if x.get("dns_ok"))
    tls_ok = sum(1 for x in report.get("dns_tcp_tls", []) if x.get("tls_ok"))
    http_ok = sum(1 for x in report.get("http", []) if x.get("ok"))
    ws_control_ok = sum(1 for x in report.get("ws_control", []) if x.get("ok"))
    tv_direct_ok = sum(1 for x in report.get("tv_direct", []) if x.get("ok"))
    proxy_tests = report.get("proxy_tests", [])
    proxy_control_ok = sum(1 for x in proxy_tests if (x.get("control_ws") or {}).get("ok"))
    proxy_tv_handshake_ok = sum(1 for x in proxy_tests if (x.get("tv_handshake") or {}).get("ok"))
    proxy_tv_data_ok = sum(1 for x in proxy_tests if (x.get("tv_data_probe") or {}).get("ok"))
    return {
        "public_ip_ok": public_ip_ok,
        "dns_ok": dns_ok,
        "tls_ok": tls_ok,
        "http_ok": http_ok,
        "ws_control_ok": ws_control_ok,
        "tv_direct_ok": tv_direct_ok,
        "proxy_tested": len(proxy_tests),
        "proxy_control_ws_ok": proxy_control_ok,
        "proxy_tv_handshake_ok": proxy_tv_handshake_ok,
        "proxy_tv_data_ok": proxy_tv_data_ok,
    }


def main() -> None:
    args = _parse_args()
    report: Dict[str, Any] = {
        "started_at": _utc_now_iso(),
        "args": vars(args),
        "env": {
            "github_actions": os.getenv("GITHUB_ACTIONS", ""),
            "runner_os": os.getenv("RUNNER_OS", ""),
            "runner_arch": os.getenv("RUNNER_ARCH", ""),
            "python": sys.version,
        },
        "public_ip": [],
        "dns_tcp_tls": [],
        "http": [],
        "ws_control": [],
        "tv_targets": [],
        "tv_direct": [],
        "proxy_discovery": {},
        "proxy_tests": [],
    }

    _log("collecting public IP details")
    report["public_ip"] = _discover_public_ip(timeout_sec=10.0)

    dns_hosts = list(DEFAULT_DNS_HOSTS)
    chart_host = (urlparse(str(args.chart_url).strip()).hostname or "").strip()
    ws_host = (urlparse(str(args.ws_url).strip()).hostname or "").strip()
    if chart_host:
        dns_hosts.append(chart_host)
    if ws_host:
        dns_hosts.append(ws_host)
    dns_hosts.extend(list(args.dns_host or []))
    seen_hosts = set()
    normalized_hosts: List[str] = []
    for host in dns_hosts:
        val = str(host).strip()
        if not val or val in seen_hosts:
            continue
        seen_hosts.add(val)
        normalized_hosts.append(val)

    _log(f"dns/tcp/tls probes for {len(normalized_hosts)} hosts")
    for host in normalized_hosts:
        _log(f"dns/tcp/tls probe: {host}")
        report["dns_tcp_tls"].append(_dns_tcp_tls_probe(host=host, timeout_sec=float(args.dns_timeout)))

    http_urls = list(DEFAULT_HTTP_URLS)
    http_urls.extend(list(args.http_url or []))
    seen_http = set()
    normalized_http: List[str] = []
    for url in http_urls:
        val = str(url).strip()
        if not val or val in seen_http:
            continue
        seen_http.add(val)
        normalized_http.append(val)

    _log(f"http probes for {len(normalized_http)} urls")
    for url in normalized_http:
        _log(f"http probe: {url}")
        report["http"].append(_http_probe(url=url, timeout_sec=float(args.http_timeout)))

    asyncio.run(_run_async_checks(args, report))

    report["finished_at"] = _utc_now_iso()
    report["summary"] = _build_summary(report)

    out_path = Path(str(args.out_json)).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    _log(f"summary: {json.dumps(report['summary'], ensure_ascii=False)}")
    _log(f"report written: {out_path}")


if __name__ == "__main__":
    main()
