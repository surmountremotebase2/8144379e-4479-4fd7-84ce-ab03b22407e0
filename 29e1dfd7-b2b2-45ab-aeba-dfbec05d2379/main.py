from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        super().__init__()  # Initialize the parent class
        self.tickers = ["TSLA"]  # Define the ticker for Tesla

    @property
    def assets(self):
        """Assets to include in the strategy."""
        return self.tickers

    @property
    def interval(self):
        """Interval for data fetch."""
        return "1day"  # Using daily data for this strategy

    def run(self, data):
        """
        Define the trading logic to use the MACD for buy/sell signals.
        """
        allocation_dict = {}
        for ticker in self.tickers:
            try:
                # Calculate MACD with default parameters
                macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
                if macd_data is None:
                    continue

                macd_line = macd_data["MACD"]
                signal_line = macd_data["signal"]

                # Check if MACD line crossed above the signal line
                if macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]:
                    allocation_dict[ticker] = 1.0  # Buy signal, allocate 100%
                elif macd_line[-1] < signal_line[-1] and macd_line[-2] >= signal_line[-2]:
                    allocation_dict[ticker] = 0  # Sell signal, allocate 0%
                else:
                    # Hold the current position if no crossover
                    allocation_dict[ticker] = 0  # Default to no allocation if no clear signal
            except Exception as e:
                log(f"Error calculating MACD for {ticker}: {e}")
                allocation_dict[ticker] = 0  # Default to no allocation on error

        return TargetAllocation(allocation_dict)