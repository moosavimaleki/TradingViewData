import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
from typing import List, Dict, Optional
import logging

from .base import DataSource

logger = logging.getLogger(__name__)


class YahooFinanceSource(DataSource):
    def __init__(self):
        super().__init__("yahoo_finance")
        
        # Define brokers that use default Yahoo symbols (no special suffix)
        self.default_brokers = [
            "YAHOO", "YF", "YAHOOFINANCE", "YAHOO_FINANCE"
        ]
        
        # Map broker names to Yahoo-specific identifiers if needed
        # Most brokers will use default Yahoo symbols
        self.broker_map = {
            # These brokers use Yahoo's default symbols
            "FXCM": "DEFAULT",
            "OANDA": "DEFAULT",
            "FOREXCOM": "DEFAULT",
            "FOREX.COM": "DEFAULT",
            # Add more as needed
        }
        self.timeframe_map = {
            '1m': '1m',
            '2m': '2m',
            '5m': '5m',
            '15m': '15m',
            '30m': '30m',
            '60m': '60m',
            '1h': '60m',
            '90m': '90m',
            '1d': '1d',
            '5d': '5d',
            '1wk': '1wk',
            '1mo': '1mo',
            '3mo': '3mo'
        }
        
        self.symbol_map = {
            # Crypto (primary names)
            'BTCUSDT': 'BTC-USD',
            'ETHUSDT': 'ETH-USD',
            'BNBUSDT': 'BNB-USD',
            'ADAUSDT': 'ADA-USD',
            'SOLUSDT': 'SOL-USD',
            'DOGEUSDT': 'DOGE-USD',
            
            # Metals (primary names)
            'XAUUSD': 'GC=F',  # Gold futures
            'XAGUSD': 'SI=F',  # Silver futures
            
            # Oil (primary name)
            'USOIL': 'CL=F',   # WTI Crude Oil futures
            
            # Forex (primary names) - Yahoo uses =X format
            'EURUSD': 'EURUSD=X',
            'GBPUSD': 'GBPUSD=X', 
            'USDJPY': 'USDJPY=X',
            'USDCHF': 'USDCHF=X',
            'AUDUSD': 'AUDUSD=X',
            'USDCAD': 'USDCAD=X',
            'NZDUSD': 'NZDUSD=X',
            
            # Stock indices
            'SPX': '^GSPC',    # S&P 500
            'NDX': '^IXIC',    # NASDAQ
            'DJI': '^DJI',     # Dow Jones
            'VIX': '^VIX',     # Volatility Index
            
            # Legacy mappings for backwards compatibility
            'GOLD': 'GC=F',
            'SILVER': 'SI=F',
            'OIL': 'CL=F',
            'EUR/USD': 'EURUSD=X',
            'GBP/USD': 'GBPUSD=X',
            'USD/JPY': 'USDJPY=X',
            'SP500': '^GSPC',
            'NASDAQ': '^IXIC'
        }
    
    def _get_default_brokers(self) -> List[str]:
        """Get list of brokers that use default Yahoo symbols"""
        return self.default_brokers
    
    def fetch_data(
        self, 
        symbol: str, 
        start_date: datetime, 
        end_date: datetime,
        timeframe: str = '1d'
    ) -> pd.DataFrame:
        try:
            # Extract broker from symbol if contains colon
            if ":" in symbol:
                symbol_part, broker_part = symbol.split(":", 1)
                mapped_symbol = self.map_symbol(symbol_part, broker_part)
            else:
                mapped_symbol = self.map_symbol(symbol)
            interval = self.timeframe_map.get(timeframe, '1d')
            
            ticker = yf.Ticker(mapped_symbol)
            
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval
            )
            
            if df.empty:
                logger.warning(f"No data found for symbol {mapped_symbol} ({symbol})")
                return pd.DataFrame()
            
            df.reset_index(inplace=True)
            
            df.columns = [col.lower() for col in df.columns]
            
            if 'date' in df.columns:
                df.rename(columns={'date': 'timestamp'}, inplace=True)
            elif 'datetime' in df.columns:
                df.rename(columns={'datetime': 'timestamp'}, inplace=True)
            
            required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
            for col in required_columns:
                if col not in df.columns:
                    if col == 'volume' and 'volume' not in df.columns:
                        df['volume'] = 0
                    else:
                        logger.error(f"Missing required column: {col}")
                        return pd.DataFrame()
            
            # Ensure timestamp is timezone-aware (Yahoo usually returns timezone-aware data)
            if df['timestamp'].dt.tz is None:
                # If naive, assume UTC
                df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC')
            else:
                # Convert to UTC if not already
                df['timestamp'] = df['timestamp'].dt.tz_convert('UTC')
            
            # Add bar_index from timestamp
            df['bar_index'] = df['timestamp'].apply(lambda x: int(x.timestamp()))
            
            return df[required_columns + ['bar_index']]
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            # Return empty DataFrame with correct columns and types
            return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'bar_index'])
    
    def get_available_symbols(self) -> List[str]:
        return list(self.symbol_map.keys())
    
    def add_symbol_mapping(self, internal_symbol: str, yahoo_symbol: str):
        self.symbol_map[internal_symbol] = yahoo_symbol