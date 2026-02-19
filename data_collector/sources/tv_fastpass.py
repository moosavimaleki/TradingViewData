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
from urllib.parse import urlparse

import pandas as pd

from data_collector.core.contract_manager import ContractManager

from .base import DataSource
from .tv_fastpass_client import (
    cookie_string_to_dict,
    extract_auth_token_and_build_time,
    extract_cookie_string,
    fetch_bars_ws,
)

logger = logging.getLogger(__name__)


class TvFastpassSource(DataSource):
    """
    TradingView "fastpass" websocket source using browser cookies.

    Notes:
    - TradingView WS APIs are *count-based*, not date-range based.
      For time bars we estimate required bars from (end_date-start_date) and then filter.
    - For range bars (e.g. 100R), time-based start/end are not meaningful. Use
      DataCollector range-bar special handling (tail-only update with overlap) or
      call `fetch_latest()` directly.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("tv_fastpass")
        config = config or {}

        project_root = Path(__file__).resolve().parents[2]

        # Secrets: prefer env var over config file.
        self.cookie_string = os.getenv("TV_FASTPASS_COOKIE_STRING", config.get("cookie_string", "")).strip()
        self.cookie_file = os.getenv(
            "TV_FASTPASS_COOKIE_FILE",
            str(config.get("cookie_file") or (project_root / "cookie.md")),
        )

        # Chart / WS endpoints.
        self.chart_url = os.getenv(
            "TV_FASTPASS_CHART_URL",
            str(config.get("chart_url") or "https://tradingview.gettyimages.ir/chart/mx4QWE0a/"),
        )
        self.ws_url = os.getenv("TV_FASTPASS_WS_URL", str(config.get("ws_url") or "")).strip()
        self.ws_origin = os.getenv("TV_FASTPASS_WS_ORIGIN", str(config.get("ws_origin") or "")).strip()

        # Range-bar config (TV internal type).
        self.range_type = str(config.get("range_type") or "BarSetRange@tv-basicstudies-72!")
        self.range_base_interval = str(config.get("range_base_interval") or "1")
        self.phantom_bars = bool(config.get("phantom_bars") or False)

        # Fetch tuning.
        self.timeout_sec = int(config.get("timeout_sec") or 30)
        self.page_step = int(config.get("page_step") or 2000)
        self.max_fetch_bars = int(config.get("max_fetch_bars") or 12000)
        self.default_fetch_bars = int(config.get("default_fetch_bars") or 10000)
        self.auth_token_ttl_sec = int(config.get("auth_token_ttl_sec") or 600)

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

        # Used to detect brokers in either side of "A:B".
        self._known_brokers = set(ContractManager().standard_brokers.values())
        self._auth_token: Optional[str] = None
        self._auth_token_expires_at: float = 0.0
        self._build_time: Optional[str] = None

    def _resolve_symbol_and_broker(self, symbol: str) -> Tuple[str, str]:
        """
        Normalize input into (storage_symbol, storage_broker).

        Accepts:
        - Internal contract: "XAUUSD:BLACKBULL"
        - TradingView format: "BLACKBULL:XAUUSD"
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
                "tv_fastpass requires a broker to build TradingView symbol. "
                "Use contract notation like XAUUSD:BLACKBULL or set sources.tv_fastpass.default_broker."
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
        # Accept raw values like "1D" / "D".
        return tf

    def _read_cookie_string(self) -> str:
        return extract_cookie_string(cookie_file=self.cookie_file, cookie_string=self.cookie_string)

    def _get_auth_token(self, cookie_string: str) -> str:
        now = time.time()
        if self._auth_token and now < self._auth_token_expires_at:
            return self._auth_token
        cookies = cookie_string_to_dict(cookie_string)
        token, build_time = extract_auth_token_and_build_time(self.chart_url, cookies)
        self._auth_token = token
        self._build_time = build_time
        self._auth_token_expires_at = now + max(30, int(self.auth_token_ttl_sec))
        return token

    def _build_fastpass_ws_url(self) -> str:
        """
        Build fastpass WS URL using the same `date=` parameter as the browser.
        Falls back to a UTC timestamp if BUILD_TIME isn't available.
        """
        chart_id_match = re.search(r"/chart/([^/]+)/?", self.chart_url)
        if not chart_id_match:
            raise ValueError(f"Could not extract chart id from chart_url={self.chart_url!r}")
        chart_id = chart_id_match.group(1)

        date_value = (self._build_time or "").strip()
        if not date_value:
            date_value = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%dT%H:%M:%S")

        date_enc = date_value.replace(":", "%3A")
        host = (urlparse(self.chart_url).hostname or "").strip()
        if not host:
            raise ValueError(f"Could not infer host from chart_url={self.chart_url!r}")
        return f"wss://{host}/socket.io/websocket?from=chart%2F{chart_id}%2F&date={date_enc}&type=chart&auth=sessionid"

    def _is_retryable_ws_error(self, exc: Exception) -> bool:
        text = str(exc)
        # Fastpass CDN uses a mix of 426/429 when overloaded/rate-limiting.
        if "HTTP 429" in text or "HTTP 426" in text:
            return True
        if "SSL" in text or "UNEXPECTED_EOF" in text:
            return True
        return False

    def fetch_latest(self, symbol: str, timeframe: str, *, n_bars: int) -> pd.DataFrame:
        """
        Fetch the latest N bars from TradingView WS (both time bars and range bars).
        """
        cookie_string = self._read_cookie_string()
        auth_token = self._get_auth_token(cookie_string)

        tv_symbol, _, _ = self._to_tv_symbol(symbol)
        interval = self._to_tv_interval(timeframe)

        ws_url = self.ws_url
        ws_origin = self.ws_origin
        try:
            host = (urlparse(self.chart_url).hostname or "").lower()
            # Any non-official TradingView domain is treated as a fastpass proxy host.
            if not ws_url.strip() and host and not host.endswith("tradingview.com"):
                ws_url = self._build_fastpass_ws_url()
        except Exception:
            ws_url = self.ws_url

        max_attempts = int(os.getenv("TV_FASTPASS_WS_RETRIES", "10"))
        base_sleep = float(os.getenv("TV_FASTPASS_WS_RETRY_BASE_SLEEP_SEC", "10"))

        last_exc: Exception | None = None
        for attempt in range(1, max_attempts + 1):
            try:
                return asyncio.run(
                    fetch_bars_ws(
                        chart_url=self.chart_url,
                        ws_url=ws_url,
                        ws_origin=ws_origin,
                        cookie_string=cookie_string,
                        auth_token=auth_token,
                        symbol=tv_symbol,
                        interval=interval,
                        range_type=self.range_type,
                        range_base_interval=self.range_base_interval,
                        phantom_bars=self.phantom_bars,
                        n_bars=int(n_bars),
                        timeout_sec=int(self.timeout_sec),
                        page_step=int(self.page_step),
                    )
                )
            except Exception as e:
                last_exc = e
                if attempt >= max_attempts or not self._is_retryable_ws_error(e):
                    raise
                # Exponential backoff with jitter.
                sleep_s = min(120.0, base_sleep * (2 ** (attempt - 1)))
                sleep_s = sleep_s + random.random() * 0.5 * sleep_s
                logger.warning(
                    f"tv_fastpass WS fetch failed (attempt {attempt}/{max_attempts}): {e}. "
                    f"sleeping {sleep_s:.1f}s before retry"
                )
                time.sleep(sleep_s)

        if last_exc is not None:
            raise last_exc
        return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume", "bar_index"])

    def fetch_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        timeframe: str = "1d",
    ) -> pd.DataFrame:
        """
        DataSource interface: tries to approximate a date-range request.

        For range bars (e.g. 100R), date-range is not meaningful; this will return the latest
        `default_fetch_bars` bars (capped by max_fetch_bars) and ignore start/end filtering.
        Prefer DataCollector's range-bar special handling for updates.
        """
        try:
            interval = self._to_tv_interval(timeframe)

            # Range bars: no time-based coverage, just fetch latest N.
            if re.fullmatch(r"[0-9]+R", interval):
                df = self.fetch_latest(symbol, timeframe, n_bars=min(self.default_fetch_bars, self.max_fetch_bars))
                return df

            # Time bars: estimate N needed for the requested window, then filter.
            seconds_per_bar = self._seconds_per_interval(interval)
            if seconds_per_bar is None:
                n_bars = min(self.default_fetch_bars, self.max_fetch_bars)
            else:
                delta_sec = max(0.0, (end_date - start_date).total_seconds())
                est = int(delta_sec / seconds_per_bar) + 500  # safety margin
                n_bars = min(max(est, 1), self.max_fetch_bars)

            df = self.fetch_latest(symbol, timeframe, n_bars=n_bars)

            # Filter by requested range (best effort).
            if not df.empty:
                ts = df["timestamp"]
                # Ensure timezone-aware UTC filtering
                if isinstance(start_date, datetime) and start_date.tzinfo is None:
                    start_date = start_date.replace(tzinfo=timezone.utc)
                if isinstance(end_date, datetime) and end_date.tzinfo is None:
                    end_date = end_date.replace(tzinfo=timezone.utc)
                df = df[(ts >= pd.Timestamp(start_date).tz_convert("UTC")) & (ts <= pd.Timestamp(end_date).tz_convert("UTC"))].copy()

            return df
        except Exception as e:
            logger.error(f"tv_fastpass fetch_data failed for {symbol} tf={timeframe}: {e}")
            return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume", "bar_index"])

    def _seconds_per_interval(self, interval: str) -> Optional[int]:
        raw = interval.strip().upper()
        if raw.isdigit():
            # minutes
            return int(raw) * 60
        if raw in {"D", "1D"}:
            return 86400
        if raw in {"W", "1W"}:
            return 7 * 86400
        if raw in {"M", "1M"}:
            return 30 * 86400
        return None

    def get_available_symbols(self) -> List[str]:
        # TradingView has too many; we don't enumerate.
        return []

    def create_metadata(self, symbol: str, timeframe: str, broker: str = "unknown"):
        # Ensure broker is always populated for consistent storage paths.
        if not broker or broker == "unknown":
            broker = self.default_broker or "unknown"
        else:
            broker = ContractManager().normalize_broker(broker) or broker

        # Keep base behavior but ensure collected_at is UTC.
        md = super().create_metadata(symbol=symbol, timeframe=timeframe, broker=broker)
        md.collected_at = datetime.now(timezone.utc)
        return md
