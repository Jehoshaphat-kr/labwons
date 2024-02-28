from nohji.deprecated.labwons.equity.fetch.kr.fetch import stock
from typing import Union
from pandas import Series, isna
from numpy import nan, isnan


class snap(object):

    def __init__(self, ticker:str, meta:Series, data:stock):
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
        targetPrice = self._data.consensusOutstanding.목표주가
        return self.fiftyTwoWeekHigh if isnan(targetPrice) else targetPrice

    @property
    def targetPriceRatio(self) -> float:
        return round(100 * (self.currentPrice / self.targetPrice - 1), 2)

    @property
    def numberOfAnalystOpinions(self) -> Union[int, float]:
        try:
            return self._data.consensusOutstanding.추정기관수
        except (ValueError, AttributeError):
            return nan

    @property
    def dividendRate(self) -> float:
        return self._data.abstract.배당수익률[-2]

    @property
    def fiveYearAverageDividendRate(self) -> float:
        return round(self._data.abstract["배당수익률"].astype(float)[:-1].mean(), 2)

    @property
    def fiveYearAverageDividendYield(self) -> float:
        return self.fiveYearAverageDividendRate

    @property
    def dividendYield(self) -> float:
        return self._data.multiplesTrailing.dividendYield

    @property
    def fiscalPE(self) -> float:
        return round(self._data.currentPrice / self.fiscalEps, 2)

    @property
    def trailingPE(self) -> float:
        return self._data.multiplesTrailing.trailingPE

    @property
    def forwardPE(self) -> float:
        return round(self.currentPrice / self.forwardEps, 2)

    @property
    def estimatePE(self) -> float:
        return self._data.multiplesTrailing.estimatePE

    @property
    def sectorPE(self) -> float:
        return self._data.multiplesOutstanding.sectorPE

    @property
    def fiscalEps(self) -> int:
        try:
            return int(self.previousClose / self._data.multiplesOutstanding.fiscalPE)
        except ValueError:
            return nan

    @property
    def trailingEps(self) -> int:
        return self._data.multiplesTrailing.trailingEps

    @property
    def forwardEps(self) -> int:
        try:
            return int(self.previousClose / self._data.multiplesOutstanding.forwardPE)
        except ValueError:
            return nan

    @property
    def estimateEps(self) -> int:
        return self._data.multiplesTrailing.estimateEps

    @property
    def priceToBook(self) -> float:
        return self._data.multiplesTrailing.priceToBook

    @property
    def bookValue(self) -> int:
        return int(self._data.multiplesTrailing.bookValue)

    @property
    def heldPercentInsiders(self) -> float:
        return round(100 - self._data.shareHolders.공시제외주주, 2)

    @property
    def heldPercentInstitutions(self) -> float:
        return self._data.shareInstitutes.상장주식수내비중.sum()

    @property
    def returnOnAssets(self) -> float:
        return self._data.abstract.ROA[-2]

    @property
    def returnOnEquity(self) -> float:
        return self._data.abstract.ROE[-2]

    @property
    def fiscalSps(self) -> int:
        return int(self._data.multiples.SPS[-2])

    @property
    def priceToSales(self) -> float:
        return round(self.currentPrice / self.fiscalSps, 2)

    @property
    def earningsGrowth(self) -> float:
        growth = self._data.growthRate
        return growth.iloc[-2, 1]

    @property
    def revenueGrowth(self) -> float:
        growth = self._data.growthRate
        return growth.iloc[-2, 0]

    @property
    def pegRatio(self) -> float:
        return round(self.trailingPE / self.earningsGrowth, 2)
