from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, InstitutionalOwnership, InsiderTrading, CboeVolatilityIndexVix
from surmount.technical_indicators import RSI, EMA, SMA, MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Specify the asset(s) you're interested in; for simplification, we'll just use one.
        self.tickers = ["SPY"]  # The S&P 500 ETF is a common choice for wheeling strategies.
        # Adding VIX to track market volatility; higher VIX might indicate better premiums (simulated environment).
        self.data_list = [CboeVolatilityIndexVix()]

    @property
    def interval(self):
        # Using daily intervals for trend analysis.
        return "1day"
        
    @property
    def assets(self):
        # Our primary asset.
        return self.tickers

    @property
    def data(self):
        # No additional data for now beyond the basics and VIX for context.
        return self.data_list

    def run(self, data):
        vix_data = data[("cboe_volatility_index_vix",)]  # Fetching the VIX data.
        latest_vix = vix_data[-1]['value'] if vix_data and len(vix_data) > 0 else None
        
        allocation_dict = {ticker: 0 for ticker in self.tickers}  # Default to no allocation.
        
        # Basic logic: Higher VIX might be cue for put selling phase (buy signal in our simplified context).
        if latest_vix and latest_vix > 20:  # Arbitrary threshold, typically higher VIX indicates more market fear.
            log("Market volatility high, looking for buying opportunities.")
            for ticker in self.tickers:
                # Simplified indicator (e.g., RSI) might suggest over-sold conditions.
                rsi_data = RSI(ticker, data['ohlcv'], 14)  # Using RSI as an example.
                if rsi_data and rsi_data[-1] < 30:
                    allocation_dict[ticker] = 1.0  # Assuming a strong buy signal based on high volatility and oversold condition.

        # If latest VIX is low, we could look for covered call selling opportunities (sell signal in simplified context),
        # but since we can't model options here directly, we'll assume it's about reducing or clearing positions.
        elif latest_vix and latest_vix < 20:  # Lower VIX might indicate complacency or stability.
            log("Market volatility low, considering position reduction or maintenance.")
            # Could add logic here similar to the buy phase, but inverted for sell signals (e.g., high RSI).
            # For simplicity, we aren't adjusting allocations based on this in our example.
        
        return TargetAllocation(allocation_dict)