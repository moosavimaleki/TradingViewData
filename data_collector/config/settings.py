import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()

class Settings:
    def __init__(self, config_file: Optional[str] = None):
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = str(PROJECT_ROOT / "data_collector" / "config" / "settings.json")
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        config_path = Path(self.config_file)
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                return self._get_default_config()
        else:
            config = self._get_default_config()
            self._save_config(config)
            return config
    
    def _save_config(self, config: Dict[str, Any]):
        config_path = Path(self.config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"Saved config to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "sources": {
                "yahoo_finance": {
                    "enabled": False,
                    "rate_limit": {
                        "requests_per_minute": 60,
                        "requests_per_hour": 2000
                    }
                },
                "faraz": {
                    "enabled": False,
                    "rate_limit": {
                        "requests_per_minute": 120,
                        "requests_per_hour": 2000
                    }
                },
                "binance": {
                    "enabled": False,
                    "api_key": "",
                    "api_secret": "",
                    "testnet": False
                },
                "metatrader": {
                    "enabled": False,
                    "terminal_path": "",
                    "account": ""
                },
                "tv_fastpass": {
                    "enabled": False,
                    "cookie_file": str(PROJECT_ROOT / "cookie.md"),
                    "cookie_string": "",
                    "chart_url": "https://tradingview.gettyimages.ir/chart/mx4QWE0a/",
                    "ws_url": "",
                    "ws_origin": "",
                    "ws_proxy": "",
                    "default_broker": "BLACKBULL",
                    "range_type": "BarSetRange@tv-basicstudies-72!",
                    "range_base_interval": "1",
                    "phantom_bars": False,
                    "timeout_sec": 60,
                    "page_step": 2000,
                    "max_fetch_bars": 12000,
                    "default_fetch_bars": 10000,
                    "range_overlap_bars": 300,
                    "range_initial_fetch_bars": 2000,
                    "range_max_fetch_bars": 12000
                },
                "tradingview": {
                    "enabled": False,
                    "chart_url": "https://www.tradingview.com/chart/",
                    "ws_url": "",
                    "ws_origin": "",
                    "ws_proxy": "",
                    "auth_token": "unauthorized_user_token",
                    "default_broker": "OANDA",
                    "range_type": "BarSetRange@tv-basicstudies-72!",
                    "range_base_interval": "1",
                    "phantom_bars": False,
                    "timeout_sec": 60,
                    "page_step": 2000,
                    "max_fetch_bars": 12000,
                    "default_fetch_bars": 10000,
                    "max_retries": 6,
                    "retry_base_sleep_sec": 2,
                    "range_overlap_bars": 300,
                    "range_initial_fetch_bars": 2000,
                    "range_max_fetch_bars": 12000
                }
            },
            "storage": {
                "type": "file",
                "base_path": str(PROJECT_ROOT / "data"),
                "max_file_size_mb": 100,
                "compression": True,
                "chunk_size": 10000,
                "merge_tail_chunks": 2,
                "retention_days": 365
            },
            "collection": {
                "default_timeframe": "1d",
                "default_lookback_days": 30,
                "auto_update": False,
                "update_interval_minutes": 60
            },
            "logging": {
                "level": "INFO",
                "file": str(PROJECT_ROOT / "logs" / "collector.log"),
                "max_size_mb": 50,
                "backup_count": 5
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self._save_config(self.config)
    
    def get_source_config(self, source_name: str) -> Dict[str, Any]:
        return self.get(f"sources.{source_name}", {})
    
    def is_source_enabled(self, source_name: str) -> bool:
        return self.get(f"sources.{source_name}.enabled", False)
