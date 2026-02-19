import requests
import pandas as pd
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
import logging
import time
import json
import os

from .base import DataSource

logger = logging.getLogger(__name__)


class FarazSource(DataSource):
    def __init__(self, cookies: str = None, config: Optional[Dict[str, Any]] = None):
        super().__init__("faraz")
        self.config = config or {}
        self.session = requests.Session()
        self.base_url = self._normalize_base_url(
            str(
                self.config.get("base_url")
                or os.getenv("FARAZ_BASE_URL")
                or "https://ir2.faraz.io/api/customer/trading-view/history"
            ).strip()
        )
        self.timeout_sec = int(self.config.get("timeout_sec", 45))
        self.max_retries = int(self.config.get("max_retries", 3))
        self.retry_sleep_sec = float(self.config.get("retry_sleep_sec", 1.0))
        self.max_pages = int(self.config.get("max_pages", 800))
        self.first_request_countback = int(self.config.get("first_request_countback", 500))
        self.empty_page_max_jumps = int(self.config.get("empty_page_max_jumps", 5))

        # Set default headers
        self.session.headers.update({
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
            'origin': 'https://faraz.io',
            'referer': 'https://faraz.io/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
        })
        
        # Set cookies if provided
        if cookies:
            self.set_cookies(cookies)
        
        # Initialize broker map for Faraz
        self.broker_map = {
            "FXCM": "FXCM",
            "FOREXCOM": "FOREXCOM",
        }
        
        # Symbol mapping from internal names to Faraz names
        self.symbol_map = {
            # Gold mappings (XAUUSD is primary name)
            'XAUUSD': 'FXCM_XAUUSD',
            'XAUUSD:FXCM': 'FXCM_XAUUSD',
            'XAUUSD:FOREXCOM': 'FOREXCOM_XAUUSD',

            # Silver (XAGUSD is primary name)
            'XAGUSD': 'FXCM_XAGUSD',
            'XAGUSD:FXCM': 'FXCM_XAGUSD',
            'XAGUSD:FOREXCOM': 'FOREXCOM_XAGUSD',
            'SILVER': 'FXCM_XAGUSD',  # legacy
            
            # Major forex pairs (standard names)
            'EURUSD': 'FXCM_EURUSD',
            'EURUSD:FXCM': 'FXCM_EURUSD',
            'EURUSD:FOREXCOM': 'FOREXCOM_EURUSD',
            'GBPUSD': 'FXCM_GBPUSD',
            'GBPUSD:FXCM': 'FXCM_GBPUSD',
            'GBPUSD:FOREXCOM': 'FOREXCOM_GBPUSD',
            'USDJPY': 'FXCM_USDJPY',
            'USDJPY:FXCM': 'FXCM_USDJPY',
            'USDJPY:FOREXCOM': 'FOREXCOM_USDJPY',
            'USDCHF': 'FXCM_USDCHF',
            'AUDUSD': 'FXCM_AUDUSD',
            'USDCAD': 'FXCM_USDCAD',
            'NZDUSD': 'FXCM_NZDUSD',
            
            # Legacy forex names
            'EUR/USD': 'FXCM_EURUSD',
            'GBP/USD': 'FXCM_GBPUSD',
            'USD/JPY': 'FXCM_USDJPY',
            
            # Oil (USOIL is primary name)
            'USOIL': 'FXCM_USOIL',
            'OIL': 'FXCM_USOIL',  # legacy
            
            # Crypto on Faraz (if available)
            'BTCUSDT': 'BTCUSDT',  # direct mapping
            'ETHUSDT': 'ETHUSDT',  # direct mapping
        }
        
        # Default broker for each symbol
        self.default_brokers = {
            # Primary names
            'XAUUSD': 'FXCM',
            'XAGUSD': 'FXCM',
            'EURUSD': 'FXCM',
            'GBPUSD': 'FXCM',
            'USDJPY': 'FXCM',
            'USDCHF': 'FXCM',
            'AUDUSD': 'FXCM',
            'USDCAD': 'FXCM',
            'NZDUSD': 'FXCM',
            'USOIL': 'FXCM',
            'BTCUSDT': 'FXCM',
            'ETHUSDT': 'FXCM',
            
            # Legacy names
            'GOLD': 'FXCM',
            'SILVER': 'FXCM',
            'EUR/USD': 'FXCM',
            'GBP/USD': 'FXCM', 
            'USD/JPY': 'FXCM',
            'OIL': 'FXCM',
        }
        
        # Resolution mapping (Faraz uses different resolution format)
        self.timeframe_map = {
            '1s': '1S',
            '1m': '1',
            '2m': '2',
            '4m': '4',
            '5m': '5',
            '15m': '15',
            '30m': '30',
            '1h': '60',
            '60m': '60',
            '1d': 'D',
            '1D': 'D',
            '1w': 'W',
            '1W': 'W',
            '1M': 'M'
        }

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
    
    def set_cookies(self, cookies: str):
        """Set authentication cookies for the session"""
        # Parse cookie string and add to session
        cookie_dict = {}
        for cookie in cookies.split(';'):
            if '=' in cookie:
                key, value = cookie.strip().split('=', 1)
                cookie_dict[key] = value
        
        self.session.cookies.update(cookie_dict)
        logger.info("Faraz cookies updated")
    
    
    def get_default_broker(self, internal_symbol: str) -> str:
        """Get default broker for a symbol"""
        return self.default_brokers.get(internal_symbol, 'FXCM')

    @staticmethod
    def _seconds_per_candle_from_resolution(resolution: str) -> int:
        if resolution == '1S':
            return 1
        if resolution == '1':
            return 60
        if resolution == '2':
            return 120
        if resolution == '4':
            return 240
        if resolution == '5':
            return 300
        if resolution == '15':
            return 900
        if resolution == '30':
            return 1800
        if resolution == '60':
            return 3600
        if resolution == 'D':
            return 86400
        if resolution == 'W':
            return 7 * 86400
        if resolution == 'M':
            return 30 * 86400
        return 3600
    
    def fetch_data_page(
        self, 
        symbol_name: str, 
        resolution: str, 
        to_ts: int,
        countback: int,
        first_request: bool = False
    ) -> Dict:
        """
        Fetch data from Faraz API using countback pagination
        
        Faraz API works with countback but still needs 'from' parameter:
        - Starts from 'to' timestamp and goes back 'countback' candles
        - 'from' can be estimated but actual data depends on countback
        - First request: firstDataRequest=true, countback=500
        - Subsequent requests: firstDataRequest=false, countback up to 40000
        """
        seconds_per_candle = self._seconds_per_candle_from_resolution(resolution)
        safe_countback = max(1, int(countback))
        estimated_from = int(to_ts) - int(safe_countback * seconds_per_candle)
        if estimated_from >= int(to_ts):
            estimated_from = int(to_ts) - seconds_per_candle
        
        params = {
            'symbolName': symbol_name,
            'resolution': resolution,
            'from': estimated_from,
            'to': int(to_ts),
            'countback': min(max(1, int(countback)), 40000),  # Max limit
            'firstDataRequest': 'true' if first_request else 'false',
            'latest': 'false',
            'adjustType': '2',
            'json': 'true'
        }

        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.get(self.base_url, params=params, timeout=float(self.timeout_sec))
                response.raise_for_status()

                logger.info(f"🌐 URL: {response.url}")

                data = response.json()
                result_data = data.get('result', {})
                records_count = len(result_data.get('t', []))
                logger.info(f"📊 Response length: {records_count} records")
                return data

            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt >= self.max_retries:
                    break
                logger.warning(
                    f"Request retry {attempt}/{self.max_retries} failed for {symbol_name}: {e}; "
                    f"sleep={self.retry_sleep_sec}s"
                )
                time.sleep(max(0.0, float(self.retry_sleep_sec)))
            except json.JSONDecodeError as e:
                last_error = e
                break

        if last_error is not None:
            logger.error(f"Request failed for {symbol_name}: {last_error}")
        return {}
    
    def _calculate_countback_for_timeframe(self, timeframe: str) -> int:
        """محاسبه countback مناسب برای هر timeframe"""
        tf = str(timeframe).strip().lower()
        # IMPORTANT:
        # For 1s on Faraz, using a larger logical window in `from/to` is more stable
        # than relying on countback alone (API may return empty on huge jumps).
        if tf == "1s":
            return 1_800_000  # ~20.8 days logical window
        return 40_000
    
    def fetch_data(
        self, 
        symbol: str, 
        start_date: datetime, 
        end_date: datetime,
        timeframe: str = '1d'
    ) -> pd.DataFrame:
        """
        Fetch data from Faraz API using countback pagination
        
        Based on research: date pagination has bugs in Faraz API,
        so we use countback pagination for reliability.
        """
        try:
            mapped_symbol = self.map_symbol(symbol)
            resolution = self.timeframe_map.get(timeframe, 'D')
            
            # Convert datetime to unix timestamps
            end_ts = int(end_date.timestamp())
            start_ts = int(start_date.timestamp())
            
            all_data = {
                'o': [],
                'h': [],
                'l': [],
                'c': [],
                'v': [],
                't': []
            }
            
            current_to = end_ts
            page_count = 0
            max_pages = max(1, int(self.max_pages))
            first_request = True
            prev_min_timestamp: Optional[int] = None
            empty_jumps = 0
            
            logger.info(f"Starting to fetch {symbol} ({mapped_symbol}) from {start_date} to {end_date}")
            
            # Check if time range is valid
            if start_ts >= end_ts:
                logger.warning(f"Invalid time range: start_date ({start_date}) >= end_date ({end_date})")
                return pd.DataFrame()
            
            while page_count < max_pages:
                # تعیین countback بر اساس اولین درخواست یا بعدی
                if first_request:
                    if str(timeframe).strip().lower() == "1s":
                        # برای آپدیت‌های کوتاه، لازم نیست پنجره‌ی 20 روزه بگیریم.
                        # پنجره را تا سقف 1s-max محدود می‌کنیم تا شبکه/CPU سبک‌تر شود.
                        remaining_sec = max(1, int(current_to - start_ts))
                        max_countback = self._calculate_countback_for_timeframe(timeframe)
                        countback = max(1, min(max_countback, remaining_sec + 600))
                    else:
                        countback = max(1, int(self.first_request_countback))
                else:
                    countback = self._calculate_countback_for_timeframe(timeframe)
                
                logger.info(f"📥 Request {page_count + 1}: to={datetime.fromtimestamp(current_to)}, countback={countback}, first={first_request}")
                
                # Fetch page
                page_data = self.fetch_data_page(
                    symbol_name=mapped_symbol,
                    resolution=resolution,
                    to_ts=current_to,
                    countback=countback,
                    first_request=first_request
                )
                
                if not page_data or 'result' not in page_data:
                    logger.warning(f"No data received for page {page_count + 1}")
                    break
                
                result = page_data['result']
                
                # Check if we got any data
                if not result.get('t') or len(result['t']) == 0:
                    # بعضی وقت‌ها API در یک بازه خالی است ولی در بازه‌های قدیمی‌تر دیتا دارد.
                    # چند پرش محدود به عقب می‌زنیم تا اگر جزیره‌ی قدیمی وجود داشت پیدا شود.
                    if (
                        not first_request
                        and current_to > start_ts
                        and empty_jumps < max(0, int(self.empty_page_max_jumps))
                    ):
                        jump_seconds = max(1, int(countback) * int(self._seconds_per_candle_from_resolution(resolution)))
                        next_to = current_to - jump_seconds
                        if next_to <= start_ts:
                            logger.info(f"📭 Empty response and next jump passed start_date; stop for {symbol}")
                            break
                        empty_jumps += 1
                        current_to = next_to
                        page_count += 1
                        logger.info(
                            f"📭 Empty page for {symbol}; jump_back={jump_seconds}s "
                            f"to={datetime.fromtimestamp(current_to)} (empty_jump={empty_jumps}/{self.empty_page_max_jumps})"
                        )
                        time.sleep(0.1)
                        continue

                    logger.info(f"📭 Empty response detected - reached end of data for {symbol}")
                    break
                
                # Add data to beginning of arrays (since we're going backwards in time)
                for key in ['o', 'h', 'l', 'c', 'v', 't']:
                    if key in result:
                        all_data[key] = result[key] + all_data[key]
                
                # Find the minimum timestamp for next iteration
                min_timestamp = min(result['t'])
                received_count = len(result['t'])
                logger.info(f"📊 Received {received_count} records, oldest: {datetime.fromtimestamp(min_timestamp)}")

                # Safety guard: stop if pagination no longer moves backward
                if prev_min_timestamp is not None and min_timestamp >= prev_min_timestamp:
                    logger.warning(
                        f"Pagination stopped because oldest timestamp did not move backward: "
                        f"prev={prev_min_timestamp}, current={min_timestamp}"
                    )
                    break
                prev_min_timestamp = min_timestamp
                empty_jumps = 0
                
                # اگر به start_date رسیدیم، توقف کن
                if min_timestamp <= start_ts:
                    logger.info(f"✅ Reached desired start_date, stopping pagination")
                    break
                
                # Update current_to for next iteration (کمترین timestamp - 1 ثانیه)
                current_to = min_timestamp - 1
                first_request = False
                page_count += 1
                
                # Small delay to be respectful to the API
                time.sleep(0.1)
            
            if not all_data['t']:
                logger.warning(f"No data found for symbol {mapped_symbol} ({symbol})")
                return pd.DataFrame()
            
            # Convert to DataFrame with timezone-aware timestamps
            df = pd.DataFrame({
                'timestamp': [datetime.fromtimestamp(ts, tz=timezone.utc) for ts in all_data['t']],
                'open': all_data['o'],
                'high': all_data['h'], 
                'low': all_data['l'],
                'close': all_data['c'],
                'volume': all_data['v'],
                'bar_index': all_data['t']  # Add bar_index as unix timestamp
            })
            
            # Filter data to requested date range
            df = df[
                (df['timestamp'] >= start_date) & 
                (df['timestamp'] <= end_date)
            ].reset_index(drop=True)
            
            # Sort by timestamp to ensure chronological order
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            logger.info(f"Successfully fetched {len(df)} records for {symbol} from Faraz")
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol} from Faraz: {str(e)}")
            return pd.DataFrame()
    
    def get_available_symbols(self) -> List[str]:
        """Return list of available symbols"""
        return list(self.symbol_map.keys())
    
    def create_metadata(
        self, 
        symbol: str, 
        timeframe: str, 
        broker: str = None
    ):
        """Create metadata for the symbol"""
        if broker is None:
            broker = self.get_default_broker(symbol)
        
        return super().create_metadata(
            symbol=symbol,
            timeframe=timeframe,
            broker=broker
        )
    
    def add_symbol_mapping(self, internal_symbol: str, faraz_symbol: str, default_broker: str = 'FXCM'):
        """Add new symbol mapping with broker support"""
        if default_broker and default_broker != 'DEFAULT':
            # Add broker-specific mapping
            key = f"{internal_symbol}:{default_broker}"
            self.symbol_map[key] = faraz_symbol
        else:
            # Add default mapping
            self.symbol_map[internal_symbol] = faraz_symbol
        
        self.default_brokers[internal_symbol] = default_broker
        logger.info(f"Added symbol mapping: {internal_symbol} -> {faraz_symbol} ({default_broker})")
