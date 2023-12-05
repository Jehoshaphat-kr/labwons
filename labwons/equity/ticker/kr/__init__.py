from labwons.common.metadata import metaData
from labwons.equity.ticker.kr import fetch
from typing import Union
import pandas, numpy


class Ticker(object):

    def __init__(self, ticker:str, **kwargs):
        try:
            self._meta = metaData.loc[ticker].to_dict()
        except KeyError:
            self._meta = {key: ticker if "name" in key.lower() else "" for key in metaData.columns}

        if ticker in metaData.KRETF.index:
            R = fetch.etf(ticker)
        else:
            R = fetch.stock(ticker)

        for key, value in kwargs.items():
            if hasattr(R, key):
                setattr(R, key, value)

        self.ticker = ticker
        self.R = R
        return

    def describe(self) -> pandas.Series:
        data = {}
        for attr in dir(self):
            attribute = self.__getattribute__(attr)
            if callable(attribute) or attr.startswith('_'):
                continue
            if isinstance(attribute, (str, int, float)):
                data[attr] = attribute
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
    def fiftyTwoWeekHighRatio(self) -> float:
        return round(100 * (self.currentPrice / self.fiftyTwoWeekHigh - 1), 2)

    @property
    def fiftyTwoWeekLowRatio(self) -> float:
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
    def floatSharesRatio(self) -> float:
        try:
            return round(100 * self.floatShares / self.sharesOutstanding, 2)
        except ZeroDivisionError:
            return 100.0

    @property
    def foreignRate(self) -> float:
        return self.R.snapShot.foreignRate

    @property
    def beta(self) -> float:
        return self.R.snapShot.beta

    @property
    def volume(self) -> int:
        return self.R.snapShot.volume

    @property
    def averageVolume(self) -> int:
        return int(self.R.price.volume.mean())

    @property
    def averageVolume10days(self) -> int:
        return int(self.R.price.volume.rolling(window=10).mean()[-1])

    @property
    def targetPrice(self) -> Union[int, float]:
        if self.quoteType == "ETF":
            return self.fiftyTwoWeekHigh
        targetPrice = self.R.consensusOutstanding.목표주가
        return self.fiftyTwoWeekHigh if numpy.isnan(targetPrice) else targetPrice

    @property
    def targetPriceRatio(self) -> float:
        return round(100 * (self.currentPrice / self.targetPrice - 1), 2)

    @property
    def numberOfAnalystOpinions(self) -> Union[int, float]:
        try:
            return self.R.consensusOutstanding.추정기관수
        except (ValueError, AttributeError):
            return numpy.nan

    @property
    def dividendYield(self) -> float:
        series = self.R.multiples if self.quoteType == "ETF" else self.R.multiplesOutstanding
        return series["dividendYield"]

    @property
    def fiveYearAverageDividendYield(self) -> float:
        if self.quoteType == "ETF":
            return numpy.nan
        return self.R.abstract["배당수익률"].astype(float)[:-1].mean()




if __name__ == "__main__":

    t = Ticker(
        "005930" # SamsungElec
        # "323280" # SHT-5 SPAC
        # "102780" # KODEX 삼성그룹
    )
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
    # print(t.fiftyTwoWeekHighRatio)
    # print(t.fiftyTwoWeekLowRatio)
    # print(t.floatSharesRatio)
    # print(t.foreignRate)
    # print(t.beta)
    # print(t.targetPrice)
    # print(t.targetPriceRatio)
    # print(t.numberOfAnalystOpinions)
    print(t.dividendYield)
    print(t.fiveYearAverageDividendYield)


    # print(t.describe())
    """
    trailingPE
    forwardPE
    priceToSalesTrailing12Months
    heldPercentInsiders
    heldPercentInstitutions
    shortRatio
    bookValue
    priceToBook
    earningsQuarterlyGrowth
    trailingEps
    forwardEps
    pegRatio
    returnOnAssets
    returnOnEquity
    earningsGrowth
    revenueGrowth
    trailingPegRatio
    """