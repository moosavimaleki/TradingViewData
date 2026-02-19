"""
InfluxDB storage backend for market data
"""
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


class InfluxStorage:
    """
    InfluxDB storage backend for time-series market data
    
    Note: This is a placeholder implementation. 
    To use this storage backend, you need to:
    1. Install influxdb-client: pip install influxdb-client
    2. Configure InfluxDB connection in settings.json
    3. Implement the actual InfluxDB operations
    """
    
    def __init__(
        self,
        url: str = "http://localhost:8086",
        token: str = None,
        org: str = "default",
        bucket: str = "market_data"
    ):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        self.client = None
        
        # Try to import and initialize InfluxDB client
        try:
            from influxdb_client import InfluxDBClient
            self.client = InfluxDBClient(url=url, token=token, org=org)
            logger.info(f"Connected to InfluxDB at {url}")
        except ImportError:
            logger.warning("influxdb-client not installed. Install with: pip install influxdb-client")
            raise ImportError("InfluxDB client not available. Install with: pip install influxdb-client")
        except Exception as e:
            logger.error(f"Failed to connect to InfluxDB: {e}")
            raise
    
    def save_data(
        self,
        df: pd.DataFrame,
        metadata: Dict[str, Any],
        symbol: str,
        timeframe: str,
        source: str,
        broker: Optional[str] = None
    ):
        """Save data to InfluxDB"""
        if self.client is None:
            raise RuntimeError("InfluxDB client not initialized")
        
        try:
            from influxdb_client import Point
            from influxdb_client.client.write_api import SYNCHRONOUS
            
            write_api = self.client.write_api(write_options=SYNCHRONOUS)
            
            # Convert DataFrame to InfluxDB points
            points = []
            for _, row in df.iterrows():
                point = Point("market_data") \
                    .tag("symbol", symbol) \
                    .tag("timeframe", timeframe) \
                    .tag("source", source) \
                    .tag("broker", broker or "default") \
                    .field("open", float(row['open'])) \
                    .field("high", float(row['high'])) \
                    .field("low", float(row['low'])) \
                    .field("close", float(row['close'])) \
                    .field("volume", float(row['volume']))
                
                # Ensure timestamp is timezone-aware
                timestamp = row['timestamp']
                if pd.isna(timestamp):
                    continue
                    
                if isinstance(timestamp, pd.Timestamp):
                    if timestamp.tz is None:
                        timestamp = timestamp.tz_localize('UTC')
                    point.time(timestamp.to_pydatetime())
                else:
                    point.time(timestamp)
                
                points.append(point)
            
            # Write points to InfluxDB
            write_api.write(bucket=self.bucket, record=points)
            logger.info(f"Saved {len(points)} data points to InfluxDB for {symbol}")
            
        except Exception as e:
            logger.error(f"Error saving to InfluxDB: {e}")
            raise
    
    def load_data(
        self,
        symbol: str,
        timeframe: str,
        source: str,
        broker: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """Load data from InfluxDB"""
        if self.client is None:
            raise RuntimeError("InfluxDB client not initialized")
        
        try:
            query_api = self.client.query_api()
            
            # Build Flux query
            query = f'''
            from(bucket: "{self.bucket}")
                |> range(start: {self._format_time(start_date)}, stop: {self._format_time(end_date)})
                |> filter(fn: (r) => r._measurement == "market_data")
                |> filter(fn: (r) => r.symbol == "{symbol}")
                |> filter(fn: (r) => r.timeframe == "{timeframe}")
                |> filter(fn: (r) => r.source == "{source}")
            '''
            
            if broker:
                query += f'    |> filter(fn: (r) => r.broker == "{broker}")\n'
            
            query += '    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
            
            # Execute query
            result = query_api.query(query)
            
            # Convert to DataFrame
            data = []
            for table in result:
                for record in table.records:
                    data.append({
                        'timestamp': record.get_time(),
                        'open': record.values.get('open'),
                        'high': record.values.get('high'),
                        'low': record.values.get('low'),
                        'close': record.values.get('close'),
                        'volume': record.values.get('volume')
                    })
            
            if not data:
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Ensure timezone-aware
            if df['timestamp'].dt.tz is None:
                df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')
            
            # Sort by timestamp
            df.sort_values('timestamp', inplace=True)
            df.reset_index(drop=True, inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading from InfluxDB: {e}")
            return pd.DataFrame()
    
    def _format_time(self, dt: Optional[datetime]) -> str:
        """Format datetime for Flux query"""
        if dt is None:
            return "0"  # Beginning of time
        
        # Ensure timezone-aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        return dt.isoformat()
    
    def get_available_data(self) -> List[Dict[str, str]]:
        """Get list of available data in InfluxDB"""
        if self.client is None:
            raise RuntimeError("InfluxDB client not initialized")
        
        try:
            query_api = self.client.query_api()
            
            # Query to get unique combinations
            query = f'''
            from(bucket: "{self.bucket}")
                |> range(start: -365d)
                |> filter(fn: (r) => r._measurement == "market_data")
                |> group(columns: ["symbol", "timeframe", "source", "broker"])
                |> first()
                |> keep(columns: ["symbol", "timeframe", "source", "broker"])
            '''
            
            result = query_api.query(query)
            
            available = []
            for table in result:
                for record in table.records:
                    available.append({
                        'symbol': record.values.get('symbol'),
                        'timeframe': record.values.get('timeframe'),
                        'source': record.values.get('source'),
                        'broker': record.values.get('broker')
                    })
            
            return available
            
        except Exception as e:
            logger.error(f"Error getting available data from InfluxDB: {e}")
            return []
    
    def cleanup_redundant_files(self):
        """InfluxDB doesn't need file cleanup"""
        pass