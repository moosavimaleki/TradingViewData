import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Type, Union
import time
import pandas as pd
from pathlib import Path
import re

from .sources.base import DataSource
from .sources.yahoo_finance import YahooFinanceSource
from .sources.faraz import FarazSource
from .sources.tv_fastpass import TvFastpassSource
from .sources.tradingview_ws import TradingViewWebSocketSource
from .storage.manager import StorageManager
from .config.settings import Settings
from .models.market_data import MarketData
from .core.contract_manager import ContractManager

logger = logging.getLogger(__name__)

# Treat TradingView direct WS + fastpass proxy as one logical source on disk.
# We fetch from either endpoint but always persist into the canonical storage namespace.
TV_MIRROR_SOURCES = ("tv_fastpass", "tradingview")
TV_CANONICAL_STORAGE_SOURCE = "tradingview"


class DataCollector:
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.storage_manager = StorageManager(self.settings.get('storage', {}))
        self.sources: Dict[str, DataSource] = {}
        
        self._setup_logging()
        self._initialize_sources()
    
    def _setup_logging(self):
        log_config = self.settings.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        
        handlers = [logging.StreamHandler()]
        
        # Add file handler only if log file is specified and not null
        log_file = log_config.get('file')
        if log_file:
            if not Path(log_file).is_absolute():
                # Use absolute path for logs
                PROJECT_ROOT = Path(__file__).parent.parent.absolute()
                log_file = PROJECT_ROOT / "logs" / "collector.log"
            
            # Create log directory if needed
            log_path = Path(log_file).parent
            log_path.mkdir(parents=True, exist_ok=True)
            handlers.append(logging.FileHandler(log_file))
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
    
    def _initialize_sources(self):
        source_classes = {
            'yahoo_finance': YahooFinanceSource,
            'faraz': FarazSource,
            'tv_fastpass': TvFastpassSource,
            'tradingview': TradingViewWebSocketSource,
        }
        
        for source_name, source_class in source_classes.items():
            if self.settings.is_source_enabled(source_name):
                try:
                    if source_class is TvFastpassSource:
                        self.sources[source_name] = source_class(self.settings.get_source_config(source_name))
                    elif source_class is TradingViewWebSocketSource:
                        self.sources[source_name] = source_class(self.settings.get_source_config(source_name))
                    elif source_class is FarazSource:
                        self.sources[source_name] = source_class(config=self.settings.get_source_config(source_name))
                    else:
                        self.sources[source_name] = source_class()
                    logger.info(f"Initialized source: {source_name}")
                except Exception as e:
                    logger.error(f"Failed to initialize source {source_name}: {e}")
    
    def add_source(self, name: str, source: DataSource):
        self.sources[name] = source
        logger.info(f"Added custom source: {name}")
    
    def set_faraz_cookies(self, cookies: str):
        """Set authentication cookies for Faraz source"""
        if 'faraz' in self.sources:
            self.sources['faraz'].set_cookies(cookies)
            logger.info("Faraz cookies updated")
        else:
            logger.warning("Faraz source not available")
    
    def add_faraz_symbol_mapping(self, internal_symbol: str, faraz_symbol: str, default_broker: str = 'FXCM'):
        """Add new symbol mapping for Faraz source"""
        if 'faraz' in self.sources:
            self.sources['faraz'].add_symbol_mapping(internal_symbol, faraz_symbol, default_broker)
        else:
            logger.warning("Faraz source not available")
    
    def _calculate_overlap_buffer(self, timeframe: str) -> timedelta:
        """محاسبه overlap buffer متناسب با timeframe"""
        # اگر overlap را بر اساس «تعداد کندل» تنظیم کرده باشند، از آن استفاده کن.
        # مثال: overlap_candles=10 و timeframe=1m => 10 دقیقه
        try:
            overlap_candles = int(self.settings.get("collection.overlap_candles", 0) or 0)
        except Exception:
            overlap_candles = 0

        if overlap_candles > 0:
            tf = str(timeframe).strip()
            seconds_per_bar: Optional[int] = None
            m = re.fullmatch(r"([0-9]+)m", tf)
            if m:
                seconds_per_bar = int(m.group(1)) * 60
            m = re.fullmatch(r"([0-9]+)h", tf)
            if seconds_per_bar is None and m:
                seconds_per_bar = int(m.group(1)) * 3600
            if seconds_per_bar is None and tf in ("1d", "1D", "D"):
                seconds_per_bar = 86400
            if seconds_per_bar is None and tf in ("1w", "1W", "W"):
                seconds_per_bar = 7 * 86400
            if seconds_per_bar is None and tf in ("1M", "M"):
                seconds_per_bar = 30 * 86400

            if seconds_per_bar is not None:
                return timedelta(seconds=int(overlap_candles) * int(seconds_per_bar))

        overlap_map = {
            '1s': timedelta(seconds=10),      # 10 ثانیه
            '5s': timedelta(seconds=30),      # 30 ثانیه
            '1m': timedelta(minutes=5),       # 5 دقیقه
            '2m': timedelta(minutes=10),      # 10 دقیقه
            '4m': timedelta(minutes=20),      # 20 دقیقه
            '5m': timedelta(minutes=15),      # 15 دقیقه
            '15m': timedelta(minutes=45),     # 45 دقیقه
            '30m': timedelta(hours=1.5),      # 1.5 ساعت
            '1h': timedelta(hours=3),         # 3 ساعت
            '60m': timedelta(hours=3),        # 3 ساعت
            '4h': timedelta(hours=12),        # 12 ساعت
            '1d': timedelta(days=2),          # 2 روز
            '1D': timedelta(days=2),          # 2 روز
            '1w': timedelta(days=7),          # 1 هفته
            '1W': timedelta(days=7),          # 1 هفته
            '1M': timedelta(days=15),         # 15 روز
        }
        
        return overlap_map.get(timeframe, timedelta(hours=1))  # پیش‌فرض 1 ساعت

    @staticmethod
    def _ensure_utc_datetime(dt: datetime) -> datetime:
        if hasattr(dt, "to_pydatetime"):
            dt = dt.to_pydatetime()
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    def _timeframe_seconds(self, timeframe: str) -> Optional[int]:
        tf = str(timeframe).strip()
        if re.fullmatch(r"[0-9]+[rR]", tf):
            return None
        if re.fullmatch(r"[0-9]+[sS]", tf):
            return int(tf[:-1])
        m = re.fullmatch(r"([0-9]+)[mM]", tf)
        if m:
            return int(m.group(1)) * 60
        m = re.fullmatch(r"([0-9]+)[hH]", tf)
        if m:
            return int(m.group(1)) * 3600
        m = re.fullmatch(r"([0-9]+)[dD]", tf)
        if m:
            return int(m.group(1)) * 86400
        m = re.fullmatch(r"([0-9]+)[wW]", tf)
        if m:
            return int(m.group(1)) * 7 * 86400
        if tf in ("1d", "1D", "D"):
            return 86400
        if tf in ("1w", "1W", "W"):
            return 7 * 86400
        if tf in ("1M", "M"):
            return 30 * 86400
        return None

    def _fetch_data_with_backfill_windows(
        self,
        source_name: str,
        source: DataSource,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        timeframe: str,
    ) -> pd.DataFrame:
        """
        Robust fetch for delayed runs.
        For TradingView time-bars, fetches in bounded windows so max_fetch_bars caps
        don't silently skip older missing intervals.
        """
        if source_name not in TV_MIRROR_SOURCES:
            return source.fetch_data(symbol=symbol, start_date=start_date, end_date=end_date, timeframe=timeframe)

        tf_raw = str(timeframe).strip()
        if re.fullmatch(r"[0-9]+[rR]", tf_raw):
            # Range bars are handled via source-specific latest-bar logic.
            return source.fetch_data(symbol=symbol, start_date=start_date, end_date=end_date, timeframe=timeframe)

        seconds_per_bar = self._timeframe_seconds(tf_raw)
        if not seconds_per_bar:
            return source.fetch_data(symbol=symbol, start_date=start_date, end_date=end_date, timeframe=timeframe)

        max_fetch_bars = int(
            getattr(source, "max_fetch_bars", 0)
            or self.settings.get(f"sources.{source_name}.max_fetch_bars", 12000)
            or 12000
        )
        if max_fetch_bars <= 0:
            max_fetch_bars = 12000

        start_utc = self._ensure_utc_datetime(start_date)
        end_utc = self._ensure_utc_datetime(end_date)
        total_seconds = max(0.0, (end_utc - start_utc).total_seconds())

        conservative_bars = max(200, int(max_fetch_bars * 0.85))
        window_seconds = max(seconds_per_bar, conservative_bars * seconds_per_bar)
        if total_seconds <= window_seconds:
            return source.fetch_data(symbol=symbol, start_date=start_utc, end_date=end_utc, timeframe=timeframe)

        overlap_seconds = int(self._calculate_overlap_buffer(tf_raw).total_seconds())
        overlap_seconds = max(seconds_per_bar, overlap_seconds)
        overlap_seconds = min(overlap_seconds, max(seconds_per_bar, window_seconds // 5))

        frames: List[pd.DataFrame] = []
        cursor_start = start_utc
        max_windows = 5000
        window_count = 0

        while cursor_start < end_utc and window_count < max_windows:
            cursor_end = min(end_utc, cursor_start + timedelta(seconds=window_seconds))
            part = source.fetch_data(
                symbol=symbol,
                start_date=cursor_start,
                end_date=cursor_end,
                timeframe=timeframe,
            )
            if not part.empty:
                frames.append(part)

            next_start = cursor_end - timedelta(seconds=overlap_seconds)
            if next_start <= cursor_start:
                next_start = cursor_start + timedelta(seconds=seconds_per_bar)
            cursor_start = next_start
            window_count += 1

        if window_count >= max_windows:
            logger.warning(
                f"Backfill windows hit safety limit for {symbol} {timeframe} from {source_name}; "
                f"windows={window_count}"
            )

        if not frames:
            return pd.DataFrame()

        merged = pd.concat(frames, ignore_index=True)
        if "timestamp" not in merged.columns:
            return pd.DataFrame()

        merged["timestamp"] = pd.to_datetime(merged["timestamp"], utc=True, format="mixed", errors="coerce")
        merged = merged.dropna(subset=["timestamp"])
        merged = merged.sort_values("timestamp")
        merged = merged.drop_duplicates(subset=["timestamp"], keep="last").reset_index(drop=True)
        merged = merged[(merged["timestamp"] >= pd.Timestamp(start_utc)) & (merged["timestamp"] <= pd.Timestamp(end_utc))]
        return merged.reset_index(drop=True)

    def _drop_unstable_tail_candle(
        self,
        *,
        df: pd.DataFrame,
        timeframe: str,
        end_date: datetime,
        source_name: str,
        symbol: str,
    ) -> tuple[pd.DataFrame, bool]:
        """
        Remove the last in-progress candle before persisting.

        Rules:
        - Range bars (e.g. 100R): always drop the latest bar.
        - Time bars: drop the last bar only if it belongs to the currently open bucket.
        """
        if df.empty or "timestamp" not in df.columns:
            return df, False

        work = df.copy()
        work["timestamp"] = pd.to_datetime(work["timestamp"], utc=True, format="mixed", errors="coerce")
        work = work.dropna(subset=["timestamp"]).sort_values("timestamp")
        work = work.drop_duplicates(subset=["timestamp"], keep="last").reset_index(drop=True)
        if work.empty:
            return work, False

        tf = str(timeframe).strip()

        # Range bars are non-time-based and the latest bar is typically still moving.
        if re.fullmatch(r"[0-9]+[rR]", tf):
            trimmed = work.iloc[:-1].copy() if len(work) > 0 else work
            dropped = len(trimmed) < len(work)
            if dropped:
                logger.info(f"Dropped unstable tail range-bar for {symbol} {timeframe} from {source_name}")
            return trimmed.reset_index(drop=True), dropped

        seconds_per_bar = self._timeframe_seconds(tf)
        if not seconds_per_bar:
            return work, False

        end_utc = self._ensure_utc_datetime(end_date)
        bucket_open_epoch = (int(end_utc.timestamp()) // int(seconds_per_bar)) * int(seconds_per_bar)
        bucket_open = pd.Timestamp(bucket_open_epoch, unit="s", tz="UTC")

        last_ts = pd.Timestamp(work["timestamp"].iloc[-1])
        if last_ts >= bucket_open:
            trimmed = work.iloc[:-1].copy()
            logger.info(
                f"Dropped unstable tail candle for {symbol} {timeframe} from {source_name}; "
                f"last_ts={last_ts.isoformat()}, bucket_open={bucket_open.isoformat()}"
            )
            return trimmed.reset_index(drop=True), True

        return work, False
    
    
    def collect(
        self,
        symbols: List[str],
        sources: Optional[List[str]] = None,
        timeframe: str = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        update_only: bool = False
    ):
        if sources is None:
            sources = list(self.sources.keys())
        
        if timeframe is None:
            timeframe = self.settings.get('collection.default_timeframe', '1d')
        
        if end_date is None:
            end_date = datetime.now(timezone.utc)
        end_date = self._ensure_utc_datetime(end_date)
        
        if start_date is None:
            lookback_days = self.settings.get('collection.default_lookback_days', 30)
            start_date = end_date - timedelta(days=lookback_days)
        start_date = self._ensure_utc_datetime(start_date)
        
        results = {
            'success': [],
            'failed': []
        }
        
        for source_name in sources:
            if source_name not in self.sources:
                logger.warning(f"Source {source_name} not available")
                continue
            
            source = self.sources[source_name]
            storage_source_name = TV_CANONICAL_STORAGE_SOURCE if source_name in TV_MIRROR_SOURCES else source_name
            
            for symbol in symbols:
                try:
                    # Special handling: TradingView range bars (e.g. 100R) are not time-based.
                    # They can also return unreliable *old* history, so we only refresh the tail with overlap.
                    if source_name in ("tv_fastpass", "tradingview") and re.fullmatch(r"[0-9]+[rR]", str(timeframe).strip()):
                        cfg_prefix = f"sources.{source_name}"
                        overlap_bars = int(self.settings.get(f"{cfg_prefix}.range_overlap_bars", 300))
                        initial_fetch_bars = int(self.settings.get(f"{cfg_prefix}.range_initial_fetch_bars", 2000))
                        max_fetch_bars = int(self.settings.get(f"{cfg_prefix}.range_max_fetch_bars", 12000))

                        # Compute cutoff timestamp as the first timestamp inside the last `overlap_bars`.
                        cutoff_ts = None
                        try:
                            tail_result = self.storage_manager.load(
                                symbol=symbol,
                                timeframe=timeframe,
                                source=storage_source_name,
                                broker=None,
                                count=max(1, overlap_bars),
                            )
                            tail_df = tail_result.data if isinstance(tail_result, MarketData) else tail_result
                            if not tail_df.empty and "timestamp" in tail_df.columns:
                                cutoff_ts = tail_df["timestamp"].iloc[0]
                        except Exception:
                            cutoff_ts = None

                        # Initial bootstrap: grab more history.
                        n_bars = max_fetch_bars if cutoff_ts is None else max(1, initial_fetch_bars)
                        df = pd.DataFrame()

                        for _ in range(10):
                            df = source.fetch_latest(symbol=symbol, timeframe=timeframe, n_bars=int(n_bars))
                            if df.empty or cutoff_ts is None:
                                break
                            earliest = df["timestamp"].min()
                            if earliest <= cutoff_ts or n_bars >= max_fetch_bars:
                                break
                            n_bars = min(max_fetch_bars, int(n_bars) * 2)

                        if cutoff_ts is not None and not df.empty:
                            df = df[df["timestamp"] >= cutoff_ts].copy()

                        df, _ = self._drop_unstable_tail_candle(
                            df=df,
                            timeframe=timeframe,
                            end_date=end_date,
                            source_name=source_name,
                            symbol=symbol,
                        )
                        if df.empty:
                            logger.info(f"No stable range-bar data to save for {symbol} from {source_name}")
                            results["success"].append(
                                {
                                    "symbol": symbol,
                                    "source": source_name,
                                    "records": 0,
                                    "status": "no_stable_candle",
                                }
                            )
                            continue

                        cm = ContractManager()
                        actual_symbol, broker = cm.parse_contract_name(symbol)
                        metadata = source.create_metadata(symbol=actual_symbol, timeframe=timeframe, broker=broker)
                        metadata.source = storage_source_name
                        metadata.additional_info = (metadata.additional_info or {}) | {"fetched_from": source_name}
                        self.storage_manager.merge_and_save(df, metadata)

                        results["success"].append({"symbol": symbol, "source": source_name, "records": len(df)})
                        logger.info(
                            f"Successfully collected {len(df)} records for {symbol} from {source_name} "
                            f"(stored_as={metadata.source}, range bars, cutoff={cutoff_ts}, fetched={n_bars})"
                        )
                        time.sleep(1.0)
                        continue

                    # بررسی داده‌های موجود برای intelligent collection
                    last_timestamp = self.storage_manager.get_latest_timestamp(
                        symbol=symbol,
                        timeframe=timeframe,
                        source=storage_source_name
                    )
                    
                    # محاسبه بازه زمانی مطلوب برای دانلود
                    overlap_buffer = self._calculate_overlap_buffer(timeframe)
                    
                    if last_timestamp and not update_only:
                        # اگر داده موجود است، از قبل از آخرین timestamp شروع کن
                        calculated_start = last_timestamp - overlap_buffer
                        actual_start_date = max(start_date, calculated_start)
                        
                        # تبدیل Pandas Timestamp به Python datetime برای سازگاری
                        if hasattr(actual_start_date, 'to_pydatetime'):
                            actual_start_date = actual_start_date.to_pydatetime()
                            # اطمینان از اینکه timezone دارد
                            if actual_start_date.tzinfo is None:
                                actual_start_date = actual_start_date.replace(tzinfo=timezone.utc)
                        
                        
                        # اطمینان از اینکه start_date کمتر از end_date باشد
                        if actual_start_date >= end_date:
                            actual_start_date = end_date - timedelta(hours=1)  # حداقل 1 ساعت قبل
                        
                        logger.info(
                            f"Found existing data for {symbol} until {last_timestamp}, "
                            f"calculated_start: {calculated_start}, "
                            f"overlap_buffer: {overlap_buffer}, "
                            f"will collect from {actual_start_date} with overlap"
                        )
                    elif last_timestamp and update_only:
                        # برای update_only هم overlap داشته باش تا کندل‌های در حال تشکیل در اجرای بعدی اصلاح شوند.
                        calculated_start = last_timestamp - overlap_buffer
                        actual_start_date = max(start_date, calculated_start)
                        actual_start_date = self._ensure_utc_datetime(actual_start_date)
                        
                        if actual_start_date >= end_date:
                            logger.info(
                                f"No new data needed for {symbol} from {source_name} - "
                                f"last data: {last_timestamp}, current time: {end_date}"
                            )
                            results['success'].append({
                                'symbol': symbol,
                                'source': source_name,
                                'records': 0,
                                'status': 'up_to_date'
                            })
                            continue
                    elif not last_timestamp:
                        actual_start_date = start_date
                    else:
                        actual_start_date = start_date

                    
                    # دانلود ساده داده‌ها 
                    data = self._fetch_data_with_backfill_windows(
                        source_name=source_name,
                        source=source,
                        symbol=symbol,
                        start_date=actual_start_date,
                        end_date=end_date,
                        timeframe=timeframe,
                    )
                    data, _ = self._drop_unstable_tail_candle(
                        df=data,
                        timeframe=timeframe,
                        end_date=end_date,
                        source_name=source_name,
                        symbol=symbol,
                    )
                    
                    if data.empty:
                        logger.info(f"No stable data to save for {symbol} from {source_name}")
                        results['success'].append({
                            'symbol': symbol,
                            'source': source_name,
                            'records': 0,
                            'status': 'no_stable_candle'
                        })
                        continue
                    
                    # Extract broker from symbol if using contract notation
                    cm = ContractManager()
                    actual_symbol, broker = cm.parse_contract_name(symbol)
                    
                    # Don't use source_name as broker! Let the source determine the correct broker
                    metadata = source.create_metadata(
                        symbol=actual_symbol,
                        timeframe=timeframe,
                        broker=broker  # Pass None if no broker specified, let source decide
                    )
                    metadata.source = storage_source_name
                    metadata.additional_info = (metadata.additional_info or {}) | {"fetched_from": source_name}
                    
                    # همیشه merge and save استفاده کن برای intelligent merging
                    self.storage_manager.merge_and_save(data, metadata)
                    
                    results['success'].append({
                        'symbol': symbol,
                        'source': source_name,
                        'records': len(data)
                    })
                    
                    logger.info(
                        f"Successfully collected {len(data)} records for {symbol} "
                        f"from {source_name} (stored_as={metadata.source})"
                    )
                    
                except Exception as e:
                    logger.error(f"Error collecting {symbol} from {source_name}: {e}")
                    results['failed'].append({
                        'symbol': symbol,
                        'source': source_name,
                        'error': str(e)
                    })
                
                rate_limit_delay = 1.0
                time.sleep(rate_limit_delay)
        
        return results
    
    def update_all(self):
        available_data = self.storage_manager.get_available_data()
        
        symbols_by_source = {}
        for data in available_data:
            # Unify TradingView mirror sources under the canonical storage namespace.
            source = TV_CANONICAL_STORAGE_SOURCE if data['source'] in TV_MIRROR_SOURCES else data['source']
            symbol = data['symbol']
            broker = data.get('broker')
            if broker:
                symbol = f"{symbol}:{broker}"
            
            if source not in symbols_by_source:
                symbols_by_source[source] = set()
            
            symbols_by_source[source].add(symbol)
        
        all_results = {
            'success': [],
            'failed': []
        }
        
        for source, symbols in symbols_by_source.items():
            fetch_source = source
            if source == TV_CANONICAL_STORAGE_SOURCE and fetch_source not in self.sources:
                # If the canonical storage source isn't enabled as a fetch source, fall back to any mirror endpoint.
                for cand in TV_MIRROR_SOURCES:
                    if cand in self.sources:
                        fetch_source = cand
                        break

            if fetch_source in self.sources:
                results = self.collect(
                    symbols=list(symbols),
                    sources=[fetch_source],
                    update_only=True
                )
                
                all_results['success'].extend(results['success'])
                all_results['failed'].extend(results['failed'])
        
        return all_results
    
    def get_data(
        self,
        symbol: str,
        source: Optional[str] = None,
        broker: Optional[str] = None,
        timeframe: str = '1d',
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Union[pd.DataFrame, MarketData]:
        storage_source = TV_CANONICAL_STORAGE_SOURCE if source in TV_MIRROR_SOURCES else source
        return self.storage_manager.load(
            symbol=symbol,
            timeframe=timeframe,
            source=storage_source,
            broker=broker,
            start_date=start_date,
            end_date=end_date
        )
    
    def load_data(
        self,
        symbol: str,
        source: Optional[str] = None,
        broker: Optional[str] = None,
        timeframe: str = '1d',
        candle_count: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        auto_download: bool = True
    ) -> Dict[str, any]:
        """
        لود داده‌ها با پارامترهای مختلف
        
        Args:
            symbol: نماد مورد نظر
            source: منبع داده (اگر None باشد اولین منبع موجود استفاده می‌شود)
            timeframe: تایم فریم
            candle_count: تعداد کندل (اگر مشخص شود start_date نادیده گرفته می‌شود)
            start_date: تاریخ شروع
            end_date: تاریخ پایان (پیش‌فرض: اکنون)
            auto_download: اگر داده موجود نباشد، دانلود کند
            
        Returns:
            دیکشنری شامل:
            - data: DataFrame حاوی داده‌ها
            - metadata: اطلاعات متا
            - info: اطلاعات اضافی
        """
        if source is None:
            if not self.sources:
                raise ValueError("No data sources available")
            source = list(self.sources.keys())[0]

        # TradingView endpoints are mirrors; unify persistence under one storage source.
        storage_source = TV_CANONICAL_STORAGE_SOURCE if source in TV_MIRROR_SOURCES else source
        
        if end_date is None:
            end_date = datetime.now(timezone.utc)
        
        # ابتدا تلاش برای لود از فایل
        result = self.storage_manager.load(
            symbol=symbol,
            timeframe=timeframe,
            source=storage_source,
            broker=broker,
            start_date=start_date,
            end_date=end_date,
            count=candle_count
        )
        
        # Handle MarketData or DataFrame result
        if isinstance(result, MarketData):
            df = result.data
            metadata_broker = result.broker
        else:
            df = result
            # Parse contract notation if broker not specified
            if not broker and ":" in symbol:
                cm = ContractManager()
                _, parsed_broker = cm.parse_contract_name(symbol)
                metadata_broker = parsed_broker
            else:
                metadata_broker = broker
        
        # اگر داده موجود نیست و auto_download فعال است
        # برای Faraz، فقط داده‌های از قبل دانلود شده را برمی‌گردانیم
        if df.empty and auto_download and source in self.sources and source != 'faraz':
            logger.info(f"No data found for {symbol}, attempting to download...")
            
            # محاسبه start_date بر اساس candle_count
            if candle_count and candle_count > 0:
                # تخمین تاریخ شروع بر اساس تایم فریم
                days_map = {
                    '1m': candle_count / 1440,
                    '5m': candle_count / 288,
                    '15m': candle_count / 96,
                    '30m': candle_count / 48,
                    '1h': candle_count / 24,
                    '60m': candle_count / 24,
                    '1d': candle_count,
                    '1wk': candle_count * 7,
                    '1mo': candle_count * 30
                }
                
                estimated_days = days_map.get(timeframe, candle_count)
                calc_start_date = end_date - timedelta(days=int(estimated_days * 1.2))  # 20% اضافی
            else:
                calc_start_date = start_date or end_date - timedelta(days=365)
            
            # دانلود داده‌ها
            result = self.collect(
                symbols=[symbol],
                sources=[source],
                timeframe=timeframe,
                start_date=calc_start_date,
                end_date=end_date
            )
            
            if result['success']:
                # لود مجدد داده‌ها
                result = self.storage_manager.load(
                    symbol=symbol,
                    timeframe=timeframe,
                    source=storage_source,
                    broker=broker,
                    start_date=start_date,
                    end_date=end_date,
                    count=candle_count
                )
                
                if isinstance(result, MarketData):
                    df = result.data
                    metadata_broker = result.broker
                else:
                    df = result
                    # Parse contract notation if broker not specified
                    if not broker and ":" in symbol:
                        cm = ContractManager()
                        _, parsed_broker = cm.parse_contract_name(symbol)
                        metadata_broker = parsed_broker
                    else:
                        metadata_broker = broker
        elif source == 'faraz' and df.empty:
            logger.warning(f"No pre-downloaded data found for {symbol} from Faraz. For Faraz source, data must be pre-downloaded using collect() method.")
        
        # count already handled in storage_manager.load
        
        # آماده‌سازی metadata
        metadata = {
            'symbol': symbol,
            'source': storage_source,
            'broker': metadata_broker,
            'timeframe': timeframe,
            'total_records': len(df),
            'date_range': {
                'start': df['timestamp'].min().isoformat() if not df.empty else None,
                'end': df['timestamp'].max().isoformat() if not df.empty else None
            }
        }
        
        # اطلاعات اضافی
        info = {
            'data_available': not df.empty,
            'auto_downloaded': df.empty and auto_download,
            'requested_candles': candle_count,
            'actual_candles': len(df)
        }
        
        return {
            'data': df,
            'metadata': metadata,
            'info': info
        }
    
    def load_multiple(
        self,
        symbols: List[str],
        source: Optional[str] = None,
        broker: Optional[str] = None,
        timeframe: str = '1d',
        candle_count: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        auto_download: bool = True
    ) -> Dict[str, Dict[str, any]]:
        """
        لود داده‌ها برای چندین نماد
        
        Returns:
            دیکشنری با کلید symbol و مقدار نتیجه load_data
        """
        results = {}
        
        for symbol in symbols:
            try:
                results[symbol] = self.load_data(
                    symbol=symbol,
                    source=source,
                    broker=broker,
                    timeframe=timeframe,
                    candle_count=candle_count,
                    start_date=start_date,
                    end_date=end_date,
                    auto_download=auto_download
                )
            except Exception as e:
                logger.error(f"Error loading data for {symbol}: {e}")
                results[symbol] = {
                    'data': pd.DataFrame(),
                    'metadata': {'symbol': symbol, 'error': str(e)},
                    'info': {'data_available': False, 'error': str(e)}
                }
        
        return results
    
    def get_latest_data(
        self,
        symbol: str,
        source: Optional[str] = None,
        broker: Optional[str] = None,
        timeframe: str = '1d',
        candle_count: int = 100
    ) -> Dict[str, any]:
        """
        دریافت آخرین داده‌ها برای یک نماد
        """
        return self.load_data(
            symbol=symbol,
            source=source,
            broker=broker,
            timeframe=timeframe,
            candle_count=candle_count,
            auto_download=True
        )
    
    def download_historical(
        self,
        symbol: str,
        timeframe: str = '1d',
        source: Optional[str] = None,
        broker: Optional[str] = None
    ) -> Union[pd.DataFrame, MarketData]:
        """
        Download maximum available historical data for a symbol
        """
        if source is None:
            if not self.sources:
                raise ValueError("No data sources available")
            source = list(self.sources.keys())[0]
        
        # Extract broker from symbol if using contract notation
        cm = ContractManager()
        actual_symbol, parsed_broker = cm.parse_contract_name(symbol)
        if broker is None:
            broker = parsed_broker
        
        # For maximum historical data, use a very old start date
        start_date = datetime(2000, 1, 1, tzinfo=timezone.utc)
        end_date = datetime.now(timezone.utc)
        
        result = self.collect(
            symbols=[actual_symbol],
            sources=[source],
            timeframe=timeframe,
            start_date=start_date,
            end_date=end_date
        )
        
        if result['success']:
            # Load all collected data
            return self.storage_manager.load(
                symbol=actual_symbol,
                timeframe=timeframe,
                source=source,
                broker=broker
            )
        else:
            return MarketData(
                symbol=actual_symbol,
                broker=broker,
                timeframe=timeframe,
                data=pd.DataFrame()
            )
