"""
Market data model with broker information
"""
from dataclasses import dataclass
from typing import Optional
import pandas as pd
from datetime import datetime, timezone


@dataclass
class MarketData:
    """Container for market data with broker information"""
    
    symbol: str
    broker: Optional[str]
    data: pd.DataFrame
    timeframe: str = "1d"
    metadata: dict = None
    
    def __post_init__(self):
        """Validate and process data after initialization"""
        if self.metadata is None:
            self.metadata = {}
        
        # Ensure all timestamps are timezone-aware
        if 'timestamp' in self.data.columns:
            if self.data['timestamp'].dt.tz is None:
                # Convert naive timestamps to UTC
                self.data['timestamp'] = pd.to_datetime(self.data['timestamp']).dt.tz_localize('UTC')
            else:
                # Convert to UTC if in different timezone
                self.data['timestamp'] = self.data['timestamp'].dt.tz_convert('UTC')
        
        # Add broker to metadata
        self.metadata['broker'] = self.broker
        self.metadata['symbol'] = self.symbol
        self.metadata['timeframe'] = self.timeframe
        self.metadata['data_points'] = len(self.data)
        
        if 'timestamp' in self.data.columns:
            self.metadata['start_date'] = self.data['timestamp'].min().isoformat()
            self.metadata['end_date'] = self.data['timestamp'].max().isoformat()
    
    @property
    def contract_name(self):
        """Get contract name in TradingView format"""
        from data_collector.core.contract_manager import ContractManager
        cm = ContractManager()
        return cm.get_contract_name(self.symbol, self.broker)
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            'symbol': self.symbol,
            'broker': self.broker,
            'timeframe': self.timeframe,
            'metadata': self.metadata,
            'data': self.data.to_dict('records')
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create MarketData from dictionary"""
        df = pd.DataFrame(data['data'])
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return cls(
            symbol=data['symbol'],
            broker=data.get('broker'),
            timeframe=data.get('timeframe', '1d'),
            metadata=data.get('metadata', {}),
            data=df
        )