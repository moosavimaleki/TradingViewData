from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Tuple
import pandas as pd


@dataclass
class OHLCData:
    timestamp: datetime  # Should always be timezone-aware
    open: float
    high: float
    low: float
    close: float
    volume: float
    bar_index: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'timestamp': self.timestamp.isoformat(),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume
        }
        if self.bar_index is not None:
            result['bar_index'] = self.bar_index
        return result


@dataclass
class Metadata:
    symbol: str
    timeframe: str
    broker: str
    source: str
    collected_at: datetime
    additional_info: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'symbol': self.symbol,
            'timeframe': self.timeframe,
            'broker': self.broker,
            'source': self.source,
            'collected_at': self.collected_at.isoformat()
        }
        if self.additional_info:
            result['additional_info'] = self.additional_info
        return result


class DataSource(ABC):
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.broker_map = {}  # Map of broker names to source-specific names
        self.symbol_map = {}  # Map of standard symbols to source-specific symbols
    
    @abstractmethod
    def fetch_data(
        self, 
        symbol: str, 
        start_date: datetime, 
        end_date: datetime,
        timeframe: str = '1d'
    ) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_available_symbols(self) -> List[str]:
        pass
    
    def map_symbol(self, symbol: str, broker: Optional[str] = None) -> str:
        """
        Map standard symbol to source-specific symbol
        
        Args:
            symbol: Standard symbol (e.g., "XAUUSD")
            broker: Optional broker name
            
        Returns:
            Source-specific symbol
        """
        # First check if we have broker-specific mapping
        if broker:
            broker_key = self._normalize_broker_for_source(broker)
            if broker_key and broker_key != "DEFAULT":
                # For non-default broker, append to symbol if needed
                combined_key = f"{symbol}:{broker_key}"
                if combined_key in self.symbol_map:
                    return self.symbol_map[combined_key]
        
        # Check standard symbol mapping
        if symbol in self.symbol_map:
            return self.symbol_map[symbol]
        
        # Return original symbol if no mapping found
        return symbol
    
    def _normalize_broker_for_source(self, broker: str) -> Optional[str]:
        """
        Normalize broker name for this specific source
        
        Args:
            broker: Broker name
            
        Returns:
            Normalized broker name for this source or None
        """
        if not broker:
            return None
        
        broker_upper = broker.upper()
        
        # Check if broker is in our map
        if broker_upper in self.broker_map:
            return self.broker_map[broker_upper]
        
        # Return "DEFAULT" if broker should use default symbol
        # (i.e., no broker-specific suffix needed)
        return "DEFAULT" if broker_upper in self._get_default_brokers() else broker_upper
    
    def _get_default_brokers(self) -> List[str]:
        """
        Get list of brokers that use default symbols (no suffix needed)
        Override in subclasses as needed
        """
        return []
    
    def create_metadata(
        self, 
        symbol: str, 
        timeframe: str, 
        broker: str = 'unknown'
    ) -> Metadata:
        return Metadata(
            symbol=symbol,
            timeframe=timeframe,
            broker=broker,
            source=self.source_name,
            collected_at=datetime.now(timezone.utc)
        )