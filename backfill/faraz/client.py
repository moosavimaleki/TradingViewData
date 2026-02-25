from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional

import pandas as pd
import requests

logger = logging.getLogger("backfill.faraz.client")

TIMEFRAME_TO_RESOLUTION: Dict[str, str] = {
    "1m": "1",
    "3m": "3",
    "5m": "5",
    "15m": "15",
    "30m": "30",
    "45m": "45",
    "1h": "60",
    "2h": "120",
    "4h": "240",
    "1d": "D",
    "1w": "W",
    "1M": "M",
}

SUPPORTED_BROKERS = {"FXCM", "FOREXCOM", "OANDA"}
BROKERLESS_CRYPTO_SYMBOLS = {
    "ADAUSDT",
    "BNBUSDT",
    "DOGEUSDT",
    "LUNAUSDT",
    "MANAUSDT",
    "SHIBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    # Existing brokerless crypto handling kept intact.
    "BTCUSDT",
    "ETHUSDT",
}
SYMBOL_NAME_ALIASES = {
    "DXY": "TVC_DXY",
}
UNSUPPORTED_SYMBOLS = {
    "US500",
}
BROKERLESS_STORAGE_BROKER = "FARAZ"


@dataclass(frozen=True)
class FetchStats:
    pages: int
    rows: int
    first_ts: Optional[float]
    last_ts: Optional[float]


class UnsupportedFarazSymbolError(ValueError):
    pass


def storage_broker_for_symbol(*, symbol: str, requested_broker: str) -> str:
    sym = str(symbol).strip().upper()
    if sym in BROKERLESS_CRYPTO_SYMBOLS:
        return BROKERLESS_STORAGE_BROKER
    return str(requested_broker).strip().upper()


class FarazClient:
    def __init__(
        self,
        *,
        cookie_string: str,
        base_url: str = "https://ir2.faraz.io/api/customer/trading-view/history",
        timeout_sec: int = 45,
        max_retries: int = 3,
        retry_sleep_sec: float = 1.0,
        page_countback: int = 40_000,
        first_page_countback: int = 500,
        max_pages: int = 800,
    ) -> None:
        if not cookie_string.strip():
            raise ValueError("cookie_string is empty. Set FARAZ_COOKIE_STRING or FARAZ_COOKIES.")

        self.base_url = self._normalize_base_url(base_url)
        self.timeout_sec = int(timeout_sec)
        self.max_retries = int(max_retries)
        self.retry_sleep_sec = float(retry_sleep_sec)
        self.page_countback = int(page_countback)
        self.first_page_countback = int(first_page_countback)
        self.max_pages = int(max_pages)

        self.session = requests.Session()
        self.session.headers.update(
            {
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9,fa;q=0.8",
                "origin": "https://faraz.io",
                "referer": "https://faraz.io/",
                "user-agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
                ),
            }
        )
        self._set_cookies(cookie_string)

    @staticmethod
    def _normalize_base_url(raw_url: str) -> str:
        url = str(raw_url or "").strip()
        if not url:
            return "https://ir2.faraz.io/api/customer/trading-view/history"
        if url.endswith("/api/customer/trading-view/history"):
            return url
        if url.startswith("http://") or url.startswith("https://"):
            return url.rstrip("/") + "/api/customer/trading-view/history"
        return "https://" + url.strip("/").rstrip("/") + "/api/customer/trading-view/history"

    def _set_cookies(self, cookie_string: str) -> None:
        for part in cookie_string.split(";"):
            if "=" not in part:
                continue
            key, value = part.strip().split("=", 1)
            if key:
                self.session.cookies.set(key, value)

    def _map_symbol_name(self, *, symbol: str, broker: str) -> str:
        sym = str(symbol).strip().upper()
        bro = str(broker).strip().upper()
        if bro not in SUPPORTED_BROKERS:
            raise ValueError(f"Unsupported Faraz broker: {broker}")
        if sym in UNSUPPORTED_SYMBOLS:
            raise UnsupportedFarazSymbolError(f"Faraz symbol is not available: {sym}")
        alias = SYMBOL_NAME_ALIASES.get(sym)
        if alias:
            return alias

        # Some crypto symbols are exposed directly on Faraz without broker prefix.
        if sym in BROKERLESS_CRYPTO_SYMBOLS:
            return sym
        return f"{bro}_{sym}"

    def _fetch_page(
        self,
        *,
        symbol_name: str,
        resolution: str,
        from_ts: int,
        to_ts: int,
        countback: int,
        first_data_request: bool,
    ) -> dict:
        params = {
            "symbolName": symbol_name,
            "resolution": resolution,
            "from": int(from_ts),
            "to": int(to_ts),
            "countback": min(max(1, int(countback)), 40_000),
            "firstDataRequest": "true" if first_data_request else "false",
            "latest": "false",
            "adjustType": "2",
            "json": "true",
        }

        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.get(self.base_url, params=params, timeout=float(self.timeout_sec))
                response.raise_for_status()
                return response.json()
            except Exception as exc:  # pragma: no cover
                last_error = exc
                if attempt >= self.max_retries:
                    break
                time.sleep(max(0.0, self.retry_sleep_sec))

        if last_error is not None:
            raise RuntimeError(f"Faraz request failed: {type(last_error).__name__}: {last_error}") from last_error
        raise RuntimeError("Faraz request failed with unknown error")

    def fetch_history(
        self,
        *,
        symbol: str,
        broker: str,
        timeframe: str,
        start_dt: datetime,
        end_dt: datetime,
    ) -> tuple[pd.DataFrame, FetchStats]:
        tf = str(timeframe).strip()
        if tf not in TIMEFRAME_TO_RESOLUTION:
            raise ValueError(f"timeframe={timeframe!r} is not supported by Faraz")

        start_utc = start_dt.astimezone(timezone.utc)
        end_utc = end_dt.astimezone(timezone.utc)
        if start_utc >= end_utc:
            raise ValueError("start_dt must be less than end_dt")

        resolution = TIMEFRAME_TO_RESOLUTION[tf]
        symbol_name = self._map_symbol_name(symbol=symbol, broker=broker)

        start_ts = int(start_utc.timestamp())
        current_to = int(end_utc.timestamp())
        first_request = True
        pages = 0
        previous_min_ts: Optional[int] = None

        chunks = []
        while pages < self.max_pages:
            countback = self.first_page_countback if first_request else self.page_countback
            logger.debug(
                "Faraz page request symbol=%s broker=%s tf=%s page=%s to=%s countback=%s first=%s",
                symbol,
                broker,
                tf,
                pages + 1,
                current_to,
                countback,
                first_request,
            )
            payload = self._fetch_page(
                symbol_name=symbol_name,
                resolution=resolution,
                from_ts=start_ts,
                to_ts=current_to,
                countback=countback,
                first_data_request=first_request,
            )
            result = payload.get("result") or {}
            times = list(result.get("t") or [])
            if not times:
                logger.debug("Faraz page empty symbol=%s broker=%s tf=%s page=%s", symbol, broker, tf, pages + 1)
                break

            df = pd.DataFrame(
                {
                    "ts": pd.to_numeric(pd.Series(times), errors="coerce"),
                    "open": pd.to_numeric(pd.Series(result.get("o") or []), errors="coerce"),
                    "high": pd.to_numeric(pd.Series(result.get("h") or []), errors="coerce"),
                    "low": pd.to_numeric(pd.Series(result.get("l") or []), errors="coerce"),
                    "close": pd.to_numeric(pd.Series(result.get("c") or []), errors="coerce"),
                    "volume": pd.to_numeric(pd.Series(result.get("v") or []), errors="coerce").fillna(0.0),
                }
            )
            df = df.dropna(subset=["ts", "open", "high", "low", "close"])
            if df.empty:
                logger.debug(
                    "Faraz page parsed empty symbol=%s broker=%s tf=%s page=%s",
                    symbol,
                    broker,
                    tf,
                    pages + 1,
                )
                break
            chunks.append(df)
            pages += 1
            logger.debug(
                "Faraz page ok symbol=%s broker=%s tf=%s page=%s rows=%s ts_min=%s ts_max=%s",
                symbol,
                broker,
                tf,
                pages,
                len(df),
                int(df["ts"].min()),
                int(df["ts"].max()),
            )

            min_ts = int(df["ts"].min())
            if previous_min_ts is not None and min_ts >= previous_min_ts:
                break
            previous_min_ts = min_ts
            if min_ts <= start_ts:
                break

            current_to = min_ts - 1
            first_request = False
            time.sleep(0.1)

        if not chunks:
            empty = pd.DataFrame(columns=["ts", "open", "high", "low", "close", "volume"])
            return empty, FetchStats(pages=pages, rows=0, first_ts=None, last_ts=None)

        full = pd.concat(chunks, ignore_index=True, sort=False)
        full = full.dropna(subset=["ts", "open", "high", "low", "close"])
        full = full.sort_values("ts")
        full = full.drop_duplicates(subset=["ts"], keep="last").reset_index(drop=True)
        full = full[(full["ts"] >= float(start_ts)) & (full["ts"] <= float(int(end_utc.timestamp())))]
        full["ts"] = full["ts"].astype("float64")
        for col in ("open", "high", "low", "close", "volume"):
            full[col] = full[col].astype("float64")

        if full.empty:
            return full, FetchStats(pages=pages, rows=0, first_ts=None, last_ts=None)
        return full, FetchStats(
            pages=pages,
            rows=int(len(full)),
            first_ts=float(full["ts"].iloc[0]),
            last_ts=float(full["ts"].iloc[-1]),
        )
