from surmount.base_class import Strategy, TargetAllocation
from surmount.data import GDPAllCountries

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming we have a way to invest in Argentina, like a specific ETF or stock representing the country's market
        self.tickers = ["ARGENTINA_ETF"]  # Placeholder for actual investment vehicle
        self.data_list = [GDPAllCountries()]  # Evaluating GDP data for all countries including Argentina

    @property
    def interval(self):
        return "1day"  # Economic data doesn't need frequent updates, daily checks are sufficient

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Initialize allocation with no investment
        argentina_etf_allocation = 0
        gdp_data = data.get(("gdp_by_country",), [])

        # Find Argentina's latest GDP data and decide allocation based on growth or contraction
        for record in gdp_data:
            if record["country"] == "Argentina" and len(gdp_data) > 0:
                # Assuming we have two consecutive values to determine growth
                current_gdp = float(gdp_data[-1]["value"])
                previous_gdp = float(gdp_data[-2]["value"]) if len(gdp_data) > 1 else current_gdp
                gdp_growth = current_gdp - previous_gdp

                # If GDP is growing, invest in Argentina; otherwise, do not invest
                if gdp_growth > 0:
                    argentina_etf_allocation = 1  # Max allocation if growth is positive
                break
        
        return TargetAllocation({self.tickers[0]: argentina_etf_allocation})