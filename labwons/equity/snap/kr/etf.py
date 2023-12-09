from labwons.equity.fetch.kr.fetch import etf
from typing import Union
from pandas import Series, isna
from numpy import nan


class snap(object):

    def __init__(self, ticker:str, meta:Series, data:etf):
        self.ticker = ticker
        self._meta = meta
        self._data = data
        return

    def __call__(self) -> Series:
        return self.description

    @property
    def description(self) -> Series:
        if not hasattr(self, "_describe"):
            data = {}
            for attr in dir(self):
                if attr.startswith("_") or attr == "description":
                    continue
                attribute = self.__getattribute__(attr)
                if isinstance(attribute, (str, int, float)):
                    data[attr] = attribute
            self.__setattr__("_describe", Series(data))
        return self.__getattribute__("_describe")

    @property
    def name(self) -> str:
        return self._meta['name']

    @property
    def label(self) -> str:
        return f"{self.name}({self.ticker})"

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
        try:
            comp = self._data.sectorWeights
            return comp[comp[comp.columns[0]] == comp[comp.columns[0]].max()].index[0]
        except (KeyError, ValueError):
            return nan

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
    def ipo(self) -> Union[str, float]:
        if isna(self._meta["IPO"]):
            return nan
        return self._meta['IPO'].strftime("%Y-%m-%d")

    @property
    def currentPrice(self) -> Union[int, float]:
        return self._data.currentPrice

    @property
    def previousClose(self) -> Union[int, float]:
        return self._data.snapShot.previousClose

    @property
    def fiftyTwoWeekHigh(self) -> Union[int, float]:
        return self._data.snapShot.fiftyTwoWeekHigh

    @property
    def fiftyTwoWeekLow(self) -> Union[int, float]:
        return self._data.snapShot.fiftyTwoWeekLow

    @property
    def fiftyTwoWeekHighRatio(self) -> float:
        return round(100 * (self.currentPrice / self.fiftyTwoWeekHigh - 1), 2)

    @property
    def fiftyTwoWeekLowRatio(self) -> float:
        return round(100 * (self.currentPrice / self.fiftyTwoWeekLow - 1), 2)

    @property
    def marketCap(self) -> int:
        return self._data.snapShot.marketCap

    @property
    def sharesOutstanding(self) -> int:
        return self._data.snapShot.sharesOutstanding

    @property
    def floatShares(self) -> int:
        return self._data.snapShot.floatShares

    @property
    def floatSharesRatio(self) -> float:
        try:
            return round(100 * self.floatShares / self.sharesOutstanding, 2)
        except ZeroDivisionError:
            return nan

    @property
    def foreignRate(self) -> float:
        return self._data.snapShot.foreignRate

    @property
    def beta(self) -> float:
        return self._data.snapShot.beta

    @property
    def volume(self) -> int:
        return self._data.snapShot.volume

    @property
    def averageVolume(self) -> int:
        return int(self._data.price.volume.mean())

    @property
    def averageVolume10days(self) -> int:
        return int(self._data.price.volume.rolling(window=10).mean()[-1])

    @property
    def targetPrice(self) -> Union[int, float]:
        return self.fiftyTwoWeekHigh

    @property
    def targetPriceRatio(self) -> float:
        return round(100 * (self.currentPrice / self.targetPrice - 1), 2)

    @property
    def dividendYield(self) -> float:
        return self._data.multiples.dividendYield