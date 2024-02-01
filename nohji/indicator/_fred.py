from datetime import datetime, timedelta
from pandas import DataFrame, Series
from pandas_datareader import get_data_fred

class _fred:
    _base_ = DataFrame([
        # Bond and Interest Rate
        dict(
            symbol='FEDFUNDS',
            name='Federal Funds Effective Rate(M)',
            quoteType='INDICATOR',
            unit='%',
            comment='Federal Funds Effective Rate (Monthly)'
        ),
        dict(
            symbol='DFF',
            name='Federal Funds Effective Rate(D)',
            quoteType='INDICATOR',
            unit='%',
            comment='Federal Funds Effective Rate (Daily)'
        ),
        dict(
            symbol='DGS10',
            name='10-Year Constant Maturity(IB)',
            quoteType='INDICATOR',
            unit='%',
            comment='Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis (Daily)'
        ),
        dict(
            symbol='DGS5',
            name='5-Year Constant Maturity(IB)',
            quoteType='INDICATOR',
            unit='%',
            comment='Market Yield on U.S. Treasury Securities at 5-Year Constant Maturity, Quoted on an Investment Basis (Daily)'
        ),
        dict(
            symbol='DGS2',
            name='2-Year Constant Maturity(IB)',
            quoteType='INDICATOR',
            unit='%',
            comment='Market Yield on U.S. Treasury Securities at 2-Year Constant Maturity, Quoted on an Investment Basis (Daily)'
        ),
        dict(
            symbol='DGS1',
            name='1-Year Constant Maturity(IB)',
            quoteType='INDICATOR',
            unit='%',
            comment='Market Yield on U.S. Treasury Securities at 1-Year Constant Maturity, Quoted on an Investment Basis (Daily)'
        ),
        dict(
            symbol='T10Y2Y',
            name='Treasury Yield Difference(10Y-2Y)',
            quoteType='INDICATOR',
            unit='%',
            comment='10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity (Daily)'
        ),
        dict(
            symbol='T10Y3M',
            name='Treasury Yield Difference(10Y-3M)',
            quoteType='INDICATOR',
            unit='%',
            comment='10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity (Daily)'
        ),
        dict(
            symbol='BAMLH0A0HYM2',
            name='High Yield Spread',
            quoteType='INDICATOR',
            unit='%',
            comment='ICE BofA US High Yield Index Option-Adjusted Spread (Daily)'
        ),
        dict(
            symbol='MORTGAGE30US',
            name='30-Year Fixed Rate Mortgage',
            quoteType='INDICATOR',
            unit='%',
            comment='30-Year Fixed Rate Mortgage Average in the United States (Weekly)'
        ),

        # Monetary
        dict(
            symbol='M2SL',
            name='M2',
            quoteType='INDICATOR',
            unit='USD(xB)',
            comment='M2: Billions of Dollars (Monthly)'
        ),
        dict(
            symbol='M2V',
            name='Velocity of M2 Money Stock',
            quoteType='INDICATOR',
            unit='%',
            comment='Velocity of M2 Money Stock (Seasonally Adjusted, Quarterly)'
        ),

        # Inflation
        dict(
            symbol='CPIAUCSL',
            name='CPI(SA)',
            quoteType='INDICATOR',
            unit='-',
            comment='Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (Seasonally Adjusted, Monthly)'
        ),
        dict(
            symbol='CPIAUCNS',
            name='CPI(Not SA)',
            quoteType='INDICATOR',
            unit='-',
            comment='Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (Not Seasonally Adjusted, Monthly)'
        ),
        dict(
            symbol='CORESTICKM159SFRBATL',
            name='CPI(Sticky Price, YoY)',
            quoteType='INDICATOR',
            unit='%',
            comment='Sticky Price Consumer Price Index less Food and Energy (Monthly)'
        ),
        dict(
            symbol='CPILFESL',
            name='CPI(without Food, Energy)',
            quoteType='INDICATOR',
            unit='-',
            comment='Consumer Price Index for All Urban Consumers: All Items Less Food and Energy in U.S. City Average (Seasonally Adjusted, Monthly)'
        ),
        dict(
            symbol='T10YIE',
            name='10-Year Breakeven Inflation Rate',
            quoteType='INDICATOR',
            unit='%',
            comment='10-Year Breakeven Inflation Rate (Daily, Not Seasonally Adjusted)'
        ),
        dict(
            symbol='T5YIE',
            name='5-Year Breakeven Inflation Rate',
            quoteType='INDICATOR',
            unit='%',
            comment='5-Year Breakeven Inflation Rate (Daily, Not Seasonally Adjusted)'
        ),
        dict(
            symbol='T5YIFR',
            name='5-Year Forward Inflation Expectation Rate',
            quoteType='INDICATOR',
            unit='%',
            comment='5-Year, 5-Year Forward Inflation Expectation Rate (Not Seasonally Adjusted, Daily)'
        ),

        # Labor, GDP, Saving and Others
        dict(
            symbol='UNRATE',
            name='Unemployment Rate',
            quoteType='INDICATOR',
            unit='%',
            comment='Unemployment Rate(Seasonally Adjusted, Monthly)'
        ),
        dict(
            symbol='ICSA',
            name='Initial Claims',
            quoteType='INDICATOR',
            unit='-',
            comment='Initial Claims, individual claims for Unemployment Insurance Program (Seasonally Adjusted, Weekly)'
        ),
        dict(
            symbol='GDP',
            name='Gross Domestic Product',
            quoteType='INDICATOR',
            unit='USD(xB)',
            comment='Gross Domestic Product (Seasonally Adjusted, Quarterly)'
        ),
        dict(
            symbol='GDPC1',
            name='Real Gross Domestic Product',
            quoteType='INDICATOR',
            unit='USD(xB)',
            comment='Real Gross Domestic Product (Seasonally Adjusted, Quarterly)'
        ),
        dict(
            symbol='PSAVERT',
            name='Personal Saving Rate',
            quoteType='INDICATOR',
            unit='%',
            comment='Personal Saving Rate (Monthly)'
        ),
        dict(
            symbol='UMCSENT',
            name='Consumer Sentiment',
            quoteType='INDICATOR',
            unit='-',
            comment='University of Michigan: Consumer Sentiment (Monthly)'
        ),
        dict(
            symbol='VIXCLS',
            name='VIX',
            quoteType='INDICATOR',
            unit='-',
            comment='CBOE Volatility Index: VIX (Daily)'
        ),
    ])

    def __call__(self, symbol:str, period:int=10):
        return self.fetch(symbol, period)

    def __contains__(self, item):
        return item in self._base_["symbol"].values

    def __repr__(self):
        return repr(self._base_)

    def __getitem__(self, item):
        return self._base_[self._base_["symbol"] == item].iloc[0]

    def fetch(self, symbol: str, period:int=10) -> Series:
        name = f"{symbol}({self[symbol]['name']})" if symbol in self else symbol
        fetched = get_data_fred(
            symbols=symbol,
            start=datetime.today() - timedelta(365 * period),
            end=datetime.today()
        )
        return Series(name=name, index=fetched.index, data=fetched[symbol], dtype=float)


# Alias
fred = _fred()


if __name__ == "__main__":
    print(fred("VIXCLS"))