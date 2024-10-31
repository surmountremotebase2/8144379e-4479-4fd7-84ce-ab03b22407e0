from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.data import CboeVolatilityIndexVix
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY"]
        # VIX data to gauge market volatility
        self.data_list = [CboeVolatilityIndexVix()]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Default to no allocation
        spy_allocation = 0
        
        # Ensure we have enough data for analysis
        if len(data["ohlcv"]) < 35:  # Considering MACD calculation needs
            return TargetAllocation({"SPY": spy_allocation})
        
        # Calculate MACD for SPY
        macd_data = MACD("SPY", data["ohlcv"], 12, 26)
        
        # VIX value as a sentiment indicator
        vix_value = data[("cboe_volatility_index_vix",)][-1]['value']
        
        # Check for market conditions
        # Lower VIX and positive MACD signal suggests a bullish market sentiment
        if vix_value < 20 and macd_data["MACD"][-1] > macd_data["signal"][-1]:
            spy_allocation = 1
        # Higher VIX and negative MACD signal suggests bearish or volatile conditions, stay out
        elif vix_value > 20 or macd_data["MACD"][-1] < macd_data["signal"][-1]:
            spy_allocation = 0
        
        # Log the decision for review
        log(f"Allocating {spy_allocation * 100}% to SPY based on VIX and MACD analysis.")
        
        # Return the target allocation
        return TargetAllocation({"SPY": spy_allocation})