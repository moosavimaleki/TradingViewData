from __future__ import annotations

import asyncio
import logging
import os
import re
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from data_collector.core.contract_manager import ContractManager

from .base import DataSource
from .tv_fastpass_client import fetch_bars_ws

logger = logging.getLogger(__name__)


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return int(default)
    text = str(raw).strip()
    if text == "":
        return int(default)
    try:
        return int(text)
    except Exception:
        return int(default)


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return float(default)
    text = str(raw).strip()
    if text == "":
        return float(default)
    try:
        return float(text)
    except Exception:
        return float(default)


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return bool(default)
    text = str(raw).strip().lower()
    if text == "":
        return bool(default)
    return text in {"1", "true", "yes", "on"}


class TradingViewWebSocketSource(DataSource):
    """
    Direct TradingView websocket source (wss://data.tradingview.com/socket.io/websocket).

    Default auth token is TradingView's public guest token: "unauthorized_user_token".
    This is usually enough to fetch recent data; limits may apply compared to logged-in sessions.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("tradingview")
        config = config or {}

        project_root = Path(__file__).resolve().parents[2]

        self.chart_url = os.getenv("TV_CHART_URL", str(config.get("chart_url") or "https://www.tradingview.com/chart/"))
        self.ws_url = os.getenv("TV_WS_URL", str(config.get("ws_url") or "")).strip()
        self.ws_origin = os.getenv("TV_WS_ORIGIN", str(config.get("ws_origin") or "")).strip()
        self.ws_proxy = os.getenv("TV_WS_PROXY", str(config.get("ws_proxy") or "")).strip()
        self.ws_proxy_pool = self._parse_proxy_pool(self.ws_proxy)
        self.ws_direct_fallback = _env_bool(
            "TV_WS_DIRECT_FALLBACK",
            str(config.get("ws_direct_fallback", "1")).strip().lower() in {"1", "true", "yes", "on"},
        )
        self.ws_direct_first = _env_bool(
            "TV_WS_DIRECT_FIRST",
            str(config.get("ws_direct_first", "1")).strip().lower() in {"1", "true", "yes", "on"},
        )

        # Direct TradingView source always uses guest auth.
        self.auth_token = "unauthorized_user_token"

        # Range-bar config (TV internal type).
        self.range_type = str(config.get("range_type") or "BarSetRange@tv-basicstudies-72!")
        self.range_base_interval = str(config.get("range_base_interval") or "1")
        self.phantom_bars = bool(config.get("phantom_bars") or False)

        # Fetch tuning.
        self.timeout_sec = _env_int("TV_WS_TIMEOUT_SEC", int(config.get("timeout_sec") or 60))
        self.page_step = _env_int("TV_WS_PAGE_STEP", int(config.get("page_step") or 2000))
        self.max_fetch_bars = _env_int("TV_WS_MAX_FETCH_BARS", int(config.get("max_fetch_bars") or 12000))
        self.default_fetch_bars = _env_int(
            "TV_WS_DEFAULT_FETCH_BARS", int(config.get("default_fetch_bars") or 10000)
        )
        self.max_retries = _env_int("TV_WS_RETRIES", int(config.get("max_retries") or 6))
        self.retry_base_sleep_sec = _env_float(
            "TV_WS_RETRY_BASE_SLEEP_SEC", float(config.get("retry_base_sleep_sec") or 2.0)
        )
        self.retry_max_sleep_sec = _env_float(
            "TV_WS_RETRY_MAX_SLEEP_SEC", float(config.get("retry_max_sleep_sec") or 20.0)
        )
        self.max_proxy_attempts = _env_int(
            "TV_WS_MAX_PROXY_ATTEMPTS", int(config.get("max_proxy_attempts") or 0)
        )

        # Contract defaults for symbol-only input.
        self.default_broker = str(config.get("default_broker") or "").strip().upper()

        # Timeframe mapping (DataCollector uses 1m/1h; TV WS uses minutes and D/W/M).
        self.timeframe_map = {
            "1m": "1",
            "2m": "2",
            "3m": "3",
            "4m": "4",
            "5m": "5",
            "15m": "15",
            "30m": "30",
            "45m": "45",
            "1h": "60",
            "60m": "60",
            "2h": "120",
            "4h": "240",
            "1d": "1D",
            "1D": "1D",
            "D": "1D",
            "1w": "1W",
            "1W": "1W",
            "W": "1W",
            "1M": "1M",
            "M": "1M",
        }

        self._known_brokers = set(ContractManager().standard_brokers.values())

    @staticmethod
    def _ws_debug_enabled() -> bool:
        return str(os.getenv("TV_WS_DEBUG", "0")).strip().lower() in {"1", "true", "yes", "on"}

    @staticmethod
    def _parse_proxy_pool(raw: str) -> List[str]:
        if not raw:
            return []
        tokens = re.split(r"[\n,;]+", raw)
        out: List[str] = []
        seen = set()
        for t in tokens:
            val = t.strip()
            if not val:
                continue
            if "://" not in val:
                val = f"http://{val}"
            if val in seen:
                continue
            seen.add(val)
            out.append(val)
        return out

    def _proxy_for_attempt(self, attempt: int) -> Optional[str]:
        plan = self._attempt_plan()
        idx = max(0, int(attempt) - 1) % len(plan)
        return plan[idx]

    def _attempt_plan(self) -> List[Optional[str]]:
        proxies: List[Optional[str]] = list(self.ws_proxy_pool)
        if self.max_proxy_attempts > 0:
            proxies = proxies[: max(1, int(self.max_proxy_attempts))]

        plan: List[Optional[str]] = []

        # Prefer direct first so good GitHub runner egress doesn't wait behind flaky proxies.
        if self.ws_direct_first and (self.ws_direct_fallback or not proxies):
            plan.append(None)

        plan.extend(proxies)

        # Keep direct as fallback if enabled and not already present.
        if (self.ws_direct_fallback or not proxies) and None not in plan:
            plan.append(None)

        if not plan:
            plan = [None]
        return plan

    def _resolve_symbol_and_broker(self, symbol: str) -> Tuple[str, str]:
        """
        Normalize input into (storage_symbol, storage_broker).

        Accepts:
        - Internal contract: "XAUUSD:OANDA"
        - TradingView format: "OANDA:XAUUSD"
        - Bare symbol: "XAUUSD" (uses default_broker)
        """
        cm = ContractManager()
        raw = symbol.strip()

        if ":" in raw:
            left, right = raw.split(":", 1)
            left_u = left.strip().upper()
            right_u = right.strip().upper()

            left_norm = cm.normalize_broker(left_u) or left_u
            right_norm = cm.normalize_broker(right_u) or right_u

            # If right side is a known broker, treat as internal format SYMBOL:BROKER
            if right_norm in self._known_brokers:
                return left_u, right_norm

            # If left side is a known broker, treat as TV format BROKER:SYMBOL
            if left_norm in self._known_brokers:
                return right_u, left_norm

            # Default to SYMBOL:BROKER
            return left_u, right_norm

        sym = raw.upper()
        if not self.default_broker:
            raise ValueError(
                "tradingview source requires a broker/exchange to build TradingView symbol. "
                "Use contract notation like XAUUSD:OANDA or set sources.tradingview.default_broker."
            )
        return sym, self.default_broker

    def _to_tv_symbol(self, symbol: str) -> Tuple[str, str, str]:
        storage_symbol, storage_broker = self._resolve_symbol_and_broker(symbol)
        tv_symbol = f"{storage_broker}:{storage_symbol}"
        return tv_symbol, storage_symbol, storage_broker

    def _to_tv_interval(self, timeframe: str) -> str:
        tf = str(timeframe).strip()
        if re.fullmatch(r"[0-9]+[rR]", tf):
            return tf.upper()
        if tf.isdigit():
            return tf
        mapped = self.timeframe_map.get(tf)
        if mapped:
            return mapped
        return tf

    def fetch_latest(self, symbol: str, timeframe: str, *, n_bars: int) -> pd.DataFrame:
        tv_symbol, _, _ = self._to_tv_symbol(symbol)
        interval = self._to_tv_interval(timeframe)
        attempt_plan = self._attempt_plan()
        planned_variants = len(attempt_plan)
        max_attempts = max(1, int(self.max_retries), planned_variants)
        last_exc: Exception | None = None
        debug_enabled = self._ws_debug_enabled()

        if debug_enabled:
            logger.info(
                "[ws-debug] tradingview fetch_latest start "
                f"symbol={symbol} tv_symbol={tv_symbol} timeframe={timeframe} interval={interval} "
                f"n_bars={int(n_bars)} attempts={max_attempts} proxies={len(self.ws_proxy_pool)} "
                f"direct_fallback={self.ws_direct_fallback} direct_first={self.ws_direct_first} "
                f"max_proxy_attempts={self.max_proxy_attempts} auth_mode=guest"
            )

        for attempt in range(1, max_attempts + 1):
            try:
                ws_proxy = self._proxy_for_attempt(attempt)
                if debug_enabled:
                    logger.info(
                        "[ws-debug] tradingview attempt "
                        f"{attempt}/{max_attempts} ws_url={self.ws_url or '(auto)'} "
                        f"ws_origin={self.ws_origin or '(auto)'} proxy={ws_proxy or '(direct)'}"
                    )
                return asyncio.run(
                    fetch_bars_ws(
                        chart_url=self.chart_url,
                        ws_url=self.ws_url,
                        ws_origin=self.ws_origin,
                        cookie_string="",  # guest token by default
                        auth_token=self.auth_token,
                        symbol=tv_symbol,
                        interval=interval,
                        range_type=self.range_type,
                        range_base_interval=self.range_base_interval,
                        phantom_bars=self.phantom_bars,
                        n_bars=int(n_bars),
                        timeout_sec=int(self.timeout_sec),
                        page_step=int(self.page_step),
                        ws_proxy=ws_proxy,
                    )
                )
            except Exception as e:
                last_exc = e
                if debug_enabled:
                    logger.info(
                        f"[ws-debug] tradingview attempt failed {attempt}/{max_attempts} "
                        f"err_type={type(e).__name__} err={e}"
                    )
                if attempt >= max_attempts or not self._is_retryable_ws_error(e):
                    raise
                backoff = min(
                    max(1.0, float(self.retry_max_sleep_sec)),
                    float(self.retry_base_sleep_sec) * (2 ** (attempt - 1)),
                )
                jitter = random.random() * 0.5 * backoff
                sleep_s = backoff + jitter
                ws_proxy = self._proxy_for_attempt(attempt)
                proxy_hint = ""
                if ws_proxy:
                    safe_proxy = re.sub(r"://[^@]+@", "://***:***@", ws_proxy)
                    proxy_hint = f" proxy={safe_proxy}"
                logger.warning(
                    f"tradingview fetch_latest retry {attempt}/{max_attempts} for {symbol} {timeframe}: {e}; "
                    f"sleep={sleep_s:.1f}s{proxy_hint} "
                    f"ws_url={self.ws_url or 'auto:data.tradingview.com/socket.io/websocket'} "
                    f"ws_origin={self.ws_origin or 'auto:https://www.tradingview.com'}"
                )
                time.sleep(sleep_s)

        if last_exc:
            raise last_exc
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume", "bar_index"])

    @staticmethod
    def _is_retryable_ws_error(exc: Exception) -> bool:
        text = str(exc)
        retry_signals = (
            "received 1000 (OK); then sent 1000 (OK)",  # graceful close by server
            "ConnectionClosed",
            "timed out",
            "Timeout",
            "HTTP 429",
            "HTTP 426",
            "UNEXPECTED_EOF",
            "SSL",
            "reset by peer",
            "ServerDisconnectedError",
        )
        return any(sig in text for sig in retry_signals)

    def fetch_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        timeframe: str = "1d",
    ) -> pd.DataFrame:
        """
        DataSource interface: best-effort date-range for time bars; range bars return latest N.
        """
        try:
            interval = self._to_tv_interval(timeframe)

            # Range bars: not time-based.
            if re.fullmatch(r"[0-9]+R", interval):
                return self.fetch_latest(symbol, timeframe, n_bars=min(self.default_fetch_bars, self.max_fetch_bars))

            seconds_per_bar = self._seconds_per_interval(interval)
            if seconds_per_bar is None:
                n_bars = min(self.default_fetch_bars, self.max_fetch_bars)
            else:
                delta_sec = max(0.0, (end_date - start_date).total_seconds())
                est = int(delta_sec / seconds_per_bar) + 500
                n_bars = min(max(est, 1), self.max_fetch_bars)

            df = self.fetch_latest(symbol, timeframe, n_bars=n_bars)
            if not df.empty:
                if start_date.tzinfo is None:
                    start_date = start_date.replace(tzinfo=timezone.utc)
                if end_date.tzinfo is None:
                    end_date = end_date.replace(tzinfo=timezone.utc)
                ts = df["timestamp"]
                df = df[(ts >= pd.Timestamp(start_date).tz_convert("UTC")) & (ts <= pd.Timestamp(end_date).tz_convert("UTC"))].copy()
            return df
        except Exception as e:
            logger.error(f"tradingview fetch_data failed for {symbol} tf={timeframe}: {e}")
            return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume", "bar_index"])

    def _seconds_per_interval(self, interval: str) -> Optional[int]:
        raw = interval.strip().upper()
        if raw.isdigit():
            return int(raw) * 60
        if raw in {"D", "1D"}:
            return 86400
        if raw in {"W", "1W"}:
            return 7 * 86400
        if raw in {"M", "1M"}:
            return 30 * 86400
        return None

    def get_available_symbols(self) -> List[str]:
        return []

    def create_metadata(self, symbol: str, timeframe: str, broker: str = "unknown"):
        # Ensure broker is always populated for consistent storage paths.
        if not broker or broker == "unknown":
            broker = self.default_broker or "unknown"
        else:
            broker = ContractManager().normalize_broker(broker) or broker
        md = super().create_metadata(symbol=symbol, timeframe=timeframe, broker=broker)
        md.collected_at = datetime.now(timezone.utc)
        return md
