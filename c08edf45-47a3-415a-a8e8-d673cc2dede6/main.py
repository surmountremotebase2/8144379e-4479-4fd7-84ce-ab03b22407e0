from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import Asset  # Assuming Asset can fetch price data for simplicity; adjust based on actual Surmount data handling

class TradingStrategy(Strategy):
    def __init__(self):
        # Assume an initial set of tickers identified as penny stocks; in practice, this list should be dynamically generated
        self.tickers = ["PLUG", "FCEL", "BLNK"]  # Example penny stocks, replace with real penny stock tickers
        # Not adding any specific data fetchers, as SMA calculation is handled through technical indicators provided by Surmount

    @property
    def interval(self):
        return "1day"  # Daily interval chosen for simplicity; adjust based on strategy refinement needs

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        allocation_dict = {}

        for ticker in self.tickers:
            sma_last_10 = SMA(ticker, data, 10)  # Calculate 10-day Simple Moving Average
            current_price = data["ohlcv"][-1][ticker]['close']  # Assume last entry is the latest

            if sma_last_10 and len(sma_last_10) > 0:
                sma_current = sma_last_10[-1]  # Latest SMA value

                # Implement strategy logic: buy if current price is significantly lower than the SMA, suggesting a potential rebound
                if current_price < sma_current * 0.9:  # Current price is at least 10% lower than the SMA of the last 10 days
                    allocation_dict[ticker] = 1 / len(self.tickers)  # Evenly distribute allocation among selected penny stocks
                else:
                    allocation_dict[ticker] = 0  # Do not invest if the condition is not met
            else:
                # No SMA data available for decision making
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)