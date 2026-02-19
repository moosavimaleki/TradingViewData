from typing import Dict, List, Optional, Any, Union
import pandas as pd
from datetime import datetime, timezone
import logging

from .file_storage import FileStorage
from ..sources.base import Metadata
from ..models.market_data import MarketData
from ..core.contract_manager import ContractManager

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self, storage_config: Optional[Dict[str, Any]] = None):
        if storage_config is None:
            storage_config = {}
        
        self.storage_type = storage_config.get('type', 'file')
        
        if self.storage_type == 'file':
            self.storage = FileStorage(
                base_path=storage_config.get('base_path'),  # None if not specified, FileStorage will use absolute default
                max_file_size_mb=storage_config.get('max_file_size_mb', 100),
                compression=storage_config.get('compression', True),
                chunk_size=storage_config.get('chunk_size', 10000),
                merge_tail_chunks=storage_config.get('merge_tail_chunks', 2),
            )
        elif self.storage_type == 'influxdb':
            try:
                from .influx_storage import InfluxStorage
                self.storage = InfluxStorage(
                    url=storage_config.get('url', 'http://localhost:8086'),
                    token=storage_config.get('token'),
                    org=storage_config.get('org', 'default'),
                    bucket=storage_config.get('bucket', 'market_data')
                )
                logger.info("Using InfluxDB storage backend")
            except ImportError as e:
                logger.error(f"InfluxDB storage not available: {e}")
                logger.info("Falling back to file storage")
                self.storage_type = 'file'
                self.storage = FileStorage()
            except Exception as e:
                logger.error(f"Failed to initialize InfluxDB storage: {e}")
                logger.info("Falling back to file storage")
                self.storage_type = 'file'
                self.storage = FileStorage()
        else:
            raise ValueError(f"Unsupported storage type: {self.storage_type}")
    
    def save(
        self,
        data: Union[pd.DataFrame, MarketData],
        metadata: Optional[Metadata] = None
    ):
        # Handle MarketData object
        if isinstance(data, MarketData):
            df = data.data
            if metadata is None:
                # Create metadata from MarketData
                metadata = Metadata(
                    symbol=data.symbol,
                    timeframe=data.timeframe,
                    broker=data.broker or "unknown",
                    source=data.metadata.get('source', 'yahoo_finance'),
                    collected_at=datetime.now(timezone.utc),
                    additional_info=data.metadata
                )
        else:
            df = data
            if metadata is None:
                raise ValueError("Metadata required when saving DataFrame directly")
        
        if df.empty:
            logger.warning(f"No data to save for {metadata.symbol}")
            return
        
        # Include broker in storage key
        self.storage.save_data(
            df=df,
            metadata=metadata.to_dict(),
            symbol=metadata.symbol,
            timeframe=metadata.timeframe,
            source=metadata.source,
            broker=metadata.broker
        )
    
    def load(
        self,
        symbol: str,
        timeframe: str = "1d",
        source: Optional[str] = None,
        broker: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None
    ) -> Union[pd.DataFrame, MarketData]:
        # Handle contract notation (SYMBOL:BROKER)
        cm = ContractManager()
        if ":" in symbol:
            symbol, parsed_broker = cm.parse_contract_name(symbol)
            if broker is None:
                broker = parsed_broker
        
        # If source is not specified, try to find any available source
        if source is None:
            available = self.get_available_data()
            for item in available:
                if item['symbol'] == symbol and item['timeframe'] == timeframe:
                    if broker is None or item.get('broker') == broker:
                        source = item['source']
                        break
            
            if source is None:
                # Default to a common source
                source = 'yahoo_finance'
        
        df = self.storage.load_data(
            symbol=symbol,
            timeframe=timeframe,
            source=source,
            broker=broker,
            start_date=start_date,
            end_date=end_date,
            count=count,
        )
        
        if df.empty:
            return df
        
        # Return as MarketData object
        return MarketData(
            symbol=symbol,
            broker=broker,
            timeframe=timeframe,
            data=df
        )
    
    def merge_and_save(
        self,
        new_data: Union[pd.DataFrame, MarketData],
        metadata: Optional[Metadata] = None
    ):
        # Handle MarketData object
        if isinstance(new_data, MarketData):
            df = new_data.data
            if metadata is None:
                metadata = Metadata(
                    symbol=new_data.symbol,
                    timeframe=new_data.timeframe,
                    broker=new_data.broker or "unknown",
                    source=new_data.metadata.get('source', 'yahoo_finance'),
                    collected_at=datetime.now(timezone.utc),
                    additional_info=new_data.metadata
                )
        else:
            df = new_data
            if metadata is None:
                raise ValueError("Metadata required when saving DataFrame directly")
        
        # Don't reload all existing data, just save the new data
        # The file storage will handle merging at the file level
        self.storage.save_data(
            df=df,
            metadata=metadata.to_dict(),
            symbol=metadata.symbol,
            timeframe=metadata.timeframe,
            source=metadata.source,
            broker=metadata.broker
        )
    
    def get_available_data(self) -> List[Dict[str, str]]:
        return self.storage.get_available_data()
    
    def get_latest_timestamp(
        self,
        symbol: str,
        timeframe: str,
        source: Optional[str] = None,
        broker: Optional[str] = None
    ) -> Optional[datetime]:
        if source and hasattr(self.storage, "get_latest_timestamp"):
            try:
                latest = self.storage.get_latest_timestamp(
                    symbol=symbol,
                    timeframe=timeframe,
                    source=source,
                    broker=broker,
                )
                if latest is not None:
                    return latest
            except Exception as e:
                logger.warning(f"Fast latest timestamp lookup failed for {symbol}: {e}")

        result = self.load(
            symbol=symbol,
            timeframe=timeframe,
            source=source,
            broker=broker
        )
        
        if isinstance(result, MarketData):
            if result.data.empty:
                return None
            return result.data['timestamp'].max()
        else:
            if result.empty:
                return None
            return result['timestamp'].max()
