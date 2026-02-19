"""
Contract naming system similar to TradingView
Manages symbol and broker combinations
"""
from typing import Optional, Dict, Tuple


class ContractManager:
    """Manages contract naming convention similar to TradingView"""
    
    def __init__(self):
        # Standard broker names used across the system
        self.standard_brokers = {
            "FXCM": "FXCM",
            "OANDA": "OANDA", 
            "FOREXCOM": "FOREXCOM",
            "FOREX.COM": "FOREXCOM",
            "BINANCE": "BINANCE",
            "COINBASE": "COINBASE",
            "KRAKEN": "KRAKEN",
            "INTERACTIVE_BROKERS": "IBKR",
            "IB": "IBKR",
            "DUKASCOPY": "DUKASCOPY",
            "SAXO": "SAXO",
            "IG": "IG",
            "PEPPERSTONE": "PEPPERSTONE",
            "XM": "XM",
            "ALPARI": "ALPARI",
            "HOTFOREX": "HOTFOREX",
            "AVATRADE": "AVATRADE",
            "ETORO": "ETORO",
            "PLUS500": "PLUS500",
            "CMC": "CMC",
            "CITYINDEX": "CITYINDEX",
            "GKFX": "GKFX",
            "FXPRO": "FXPRO",
            "ADMIRAL": "ADMIRAL",
            "THINKMARKETS": "THINKMARKETS",
            "FXTM": "FXTM",
            "ROBOFOREX": "ROBOFOREX",
            "EXNESS": "EXNESS",
            "FBS": "FBS",
            "JUSTFOREX": "JUSTFOREX",
            "LITEFOREX": "LITEFOREX",
            "INSTAFOREX": "INSTAFOREX",
            "NORDFX": "NORDFX",
            "FORTRADE": "FORTRADE",
            "SWISSQUOTE": "SWISSQUOTE",
            "BDSWISS": "BDSWISS",
            "FXCHOICE": "FXCHOICE",
            "TRADERSWAY": "TRADERSWAY",
            "HUGOSWAY": "HUGOSWAY",
            "EAGLEFX": "EAGLEFX",
            "COINEXX": "COINEXX",
            "PRIMEXBT": "PRIMEXBT",
            "EVOLVE": "EVOLVE",
            "VANTAGEFX": "VANTAGEFX",
            "ICMARKETS": "ICMARKETS",
            "FPMARKETS": "FPMARKETS",
            "EASYMARKETS": "EASYMARKETS",
            "NAGA": "NAGA",
            "TRADE": "TRADE",
            "LIBERTEX": "LIBERTEX",
            "IFC": "IFC",
            "GRANDCAPITAL": "GRANDCAPITAL",
            "WELTRADE": "WELTRADE",
            "FRESHFOREX": "FRESHFOREX",
            "FIBOGROUP": "FIBOGROUP",
            "MARKETS": "MARKETS",
            "OCTAFX": "OCTAFX",
            "HYCM": "HYCM",
            "MULTIBANK": "MULTIBANK",
            "TICKMILL": "TICKMILL",
            "VANTAGE": "VANTAGE",
            "BLACKBULL": "BLACKBULL",
            "GOLDENBROKERS": "GOLDENBROKERS",
            "AXIMTRADE": "AXIMTRADE",
            "YADIX": "YADIX",
            "ZULUTRADE": "ZULUTRADE",
            "MYFXBOOK": "MYFXBOOK",
            "FARAZ": "FARAZ",
            "IRFARAZ": "FARAZ",
            "MOFID": "MOFID",
            "AGAH": "AGAH",
            "RAHAVARD": "RAHAVARD",
            "SEBA": "SEBA",
            "KIAN": "KIAN",
            "NOVIN": "NOVIN",
            "PASARGAD": "PASARGAD",
            "PARSIAN": "PARSIAN",
            "KARDAN": "KARDAN",
            "HAFEZ": "HAFEZ",
            "ATLAS": "ATLAS",
            "DENA": "DENA",
            "AMIN": "AMIN",
            "MEHR": "MEHR",
            "SAMAN": "SAMAN",
            "SINA": "SINA",
            "SHAHR": "SHAHR",
            "MASKAN": "MASKAN",
            "EGHTESAD": "EGHTESAD",
            "IRAN": "IRAN"
        }
    
    def normalize_broker(self, broker: Optional[str]) -> Optional[str]:
        """Normalize broker name to standard format"""
        if not broker:
            return None
        
        # Convert to uppercase for matching
        broker_upper = broker.upper()
        
        # Direct match
        if broker_upper in self.standard_brokers:
            return self.standard_brokers[broker_upper]
        
        # Try removing common suffixes
        for suffix in [".COM", "_BROKER", "_BROKERS", " BROKER", " BROKERS"]:
            if broker_upper.endswith(suffix):
                cleaned = broker_upper[:-len(suffix)]
                if cleaned in self.standard_brokers:
                    return self.standard_brokers[cleaned]
        
        # If no match found, return original in uppercase
        return broker_upper
    
    def get_contract_name(self, symbol: str, broker: Optional[str] = None) -> str:
        """
        Get contract name in TradingView format
        
        Args:
            symbol: Trading symbol (e.g., "XAUUSD", "EURUSD")
            broker: Optional broker name
            
        Returns:
            Contract name in format "SYMBOL" or "SYMBOL:BROKER"
        """
        # Normalize symbol to uppercase
        symbol = symbol.upper()
        
        # Normalize broker
        normalized_broker = self.normalize_broker(broker)
        
        # If no broker or broker is default, return just symbol
        if not normalized_broker:
            return symbol
        
        # Return in TradingView format
        return f"{symbol}:{normalized_broker}"
    
    def parse_contract_name(self, contract: str) -> Tuple[str, Optional[str]]:
        """
        Parse contract name into symbol and broker
        
        Args:
            contract: Contract name (e.g., "XAUUSD:FXCM" or "XAUUSD")
            
        Returns:
            Tuple of (symbol, broker)
        """
        if ":" in contract:
            parts = contract.split(":", 1)
            return parts[0].upper(), self.normalize_broker(parts[1])
        else:
            return contract.upper(), None
    
    def is_valid_contract(self, contract: str) -> bool:
        """Check if contract name is valid"""
        try:
            symbol, broker = self.parse_contract_name(contract)
            # Basic validation - symbol should have at least 2 characters
            return len(symbol) >= 2
        except:
            return False