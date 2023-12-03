from labwons.common.metadata import metaData
from typing import Union
import pandas


class Ticker(object):

    def __init__(self, ticker:str, **kwargs):
        try:
            self._meta = metaData.loc[ticker].to_dict()
        except KeyError:
            self._meta = {key: ticker if "name" in key.lower() else "" for key in metaData.columns}

        if ticker.isdigit():
            if ticker in metaData.KRETF.index:
                from labwons.equity.ticker.kr.fetch import etf
                _r = etf(ticker)
            else:
                from labwons.equity.ticker.kr.fetch import stock
                _r = stock(ticker)
        else:
            from labwons.equity.ticker.us.fetch import equity
            _r = equity(ticker)

        if "enddate" in kwargs:
            _r.enddate = kwargs["enddate"]
        if "period" in kwargs:
            _r.period = kwargs["period"]
        if "freq" in kwargs:
            _r.freq = kwargs["freq"]

        self.ticker = ticker
        self.R = _r
        return

    def describe(self) -> pandas.Series:
        data = {}
        for attr in dir(self):
            if attr.startswith('_'):
                continue
            if attr == "R":
                continue
            if callable(self.__getattribute__(attr)):
                continue
            data[attr] = self.__getattribute__(attr)
        return pandas.Series(data)

    @property
    def name(self) -> str:
        return self._meta['name']

    @property
    def quoteType(self) -> str:
        return self._meta['quoteType']

    @property
    def country(self) -> str:
        return self._meta['country']

    @property
    def exchange(self) -> str:
        return self._meta['exchange']

    @property
    def currency(self) -> str:
        return self._meta['currency']

    @property
    def shortName(self) -> str:
        return self._meta['shortName']

    @property
    def longName(self) -> str:
        return self._meta['longName']

    @property
    def korName(self) -> str:
        return self._meta['korName']

    @property
    def sector(self) -> str:
        return self._meta['sector']

    @property
    def industry(self) -> str:
        return self._meta['industry']

    @property
    def benchmarkTicker(self) -> str:
        return self._meta['benchmarkTicker']

    @property
    def benchmarkName(self) -> str:
        return self._meta['benchmarkName']

    @property
    def currentPrice(self) -> Union[int, float]:
        return self.R.currentPrice

    @property
    def previousClose(self) -> Union[int, float]:
        return self.R.snapShot.previousClose

    @property
    def fiftyTwoWeekHigh(self) -> Union[int, float]:
        return self.R.snapShot.fiftyTwoWeekHigh

    @property
    def fiftyTwoWeekLow(self) -> Union[int, float]:
        return self.R.snapShot.fiftyTwoWeekLow

    @property
    def pctFiftyTwoWeekHigh(self) -> float:
        return round(100 * (self.currentPrice / self.fiftyTwoWeekHigh - 1), 2)

    @property
    def pctFiftyTwoWeekLow(self) -> float:
        return round(100 * (self.currentPrice / self.fiftyTwoWeekLow - 1), 2)

    @property
    def marketCap(self) -> int:
        return self.R.snapShot.marketCap

    @property
    def sharesOutstanding(self) -> int:
        return self.R.snapShot.sharesOutstanding

    @property
    def floatShares(self) -> int:
        return self.R.snapShot.floatShares

    @property
    def pctFloatShares(self) -> float:
        return round(100 * self.floatShares / self.sharesOutstanding, 2)

    @property
    def foreignRate(self) -> float:
        return self.R.snapShot.foreignRate

    @property
    def beta(self) -> float:
        return self.R.snapShot.beta

if __name__ == "__main__":

    t = Ticker("005930")
    # print(t.R.price)
    # print(t.name)
    # print(t.quoteType)
    # print(t.country)
    # print(t.exchange)
    # print(t.currency)
    # print(t.shortName)
    # print(t.longName)
    # print(t.korName)
    # print(t.sector)
    # print(t.industry)
    # print(t.benchmarkTicker)
    # print(t.benchmarkName)
    # print(t.currentPrice)
    # print(t.previousClose)
    # print(t.marketCap)
    # print(t.fiftyTwoWeekHigh)
    # print(t.fiftyTwoWeekLow)
    # print(t.pctFiftyTwoWeekHigh)
    # print(t.pctFiftyTwoWeekLow)
    # print(t.pctFloatShares)
    # print(t.foreignRate)
    # print(t.beta)

    print(t.describe())
