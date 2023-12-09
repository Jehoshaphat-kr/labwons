from labwons.common.metadata import metaData
from labwons.equity._de.data.kr import fetch
from typing import Union
import pandas, numpy


class Ticker(object):

    def __init__(self, ticker:str, **kwargs):
        try:
            self._meta = metaData.loc[ticker].to_dict()
        except KeyError:
            self._meta = {key: ticker if "name" in key.lower() else "" for key in metaData.columns}

        if not ticker in metaData.etfKOR.index:
            data = fetch.stock(ticker)
        else:
            data = fetch.etf(ticker)

        for key, value in kwargs.items():
            if hasattr(data, key):
                setattr(data, key, value)
            else:
                raise AttributeError(f"No such attribute as {key}")

        self.ticker = ticker
        self.data = data
        return

    @property
    def description(self) -> pandas.Series:
        if not hasattr(self, "_describe"):
            data = {}
            for attr in dir(self):
                if attr.startswith("_") or attr == "description":
                    continue
                attribute = self.__getattribute__(attr)
                if isinstance(attribute, (str, int, float)):
                    data[attr] = attribute
            self.__setattr__("_describe", pandas.Series(data))
        return self.__getattribute__("_describe")

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
    def ipo(self) -> Union[str, float]:
        if pandas.isna(self._meta["IPO"]):
            return numpy.nan
        return self._meta['IPO'].strftime("%Y-%m-%d")

    @property
    def currentPrice(self) -> Union[int, float]:
        return self.data.currentPrice

    @property
    def previousClose(self) -> Union[int, float]:
        return self.data.snapShot.previousClose

    @property
    def fiftyTwoWeekHigh(self) -> Union[int, float]:
        return self.data.snapShot.fiftyTwoWeekHigh

    @property
    def fiftyTwoWeekLow(self) -> Union[int, float]:
        return self.data.snapShot.fiftyTwoWeekLow

    @property
    def fiftyTwoWeekHighRatio(self) -> float:
        return round(100 * (self.currentPrice / self.fiftyTwoWeekHigh - 1), 2)

    @property
    def fiftyTwoWeekLowRatio(self) -> float:
        return round(100 * (self.currentPrice / self.fiftyTwoWeekLow - 1), 2)

    @property
    def marketCap(self) -> int:
        return self.data.snapShot.marketCap

    @property
    def sharesOutstanding(self) -> int:
        return self.data.snapShot.sharesOutstanding

    @property
    def floatShares(self) -> int:
        return self.data.snapShot.floatShares

    @property
    def floatSharesRatio(self) -> float:
        try:
            return round(100 * self.floatShares / self.sharesOutstanding, 2)
        except ZeroDivisionError:
            return numpy.nan

    @property
    def foreignRate(self) -> float:
        return self.data.snapShot.foreignRate

    @property
    def beta(self) -> float:
        return self.data.snapShot.beta

    @property
    def volume(self) -> int:
        return self.data.snapShot.volume

    @property
    def averageVolume(self) -> int:
        return int(self.data.price.volume.mean())

    @property
    def averageVolume10days(self) -> int:
        return int(self.data.price.volume.rolling(window=10).mean()[-1])

    @property
    def targetPrice(self) -> Union[int, float]:
        if self.quoteType == "ETF":
            return self.fiftyTwoWeekHigh
        targetPrice = self.data.consensusOutstanding.목표주가
        return self.fiftyTwoWeekHigh if numpy.isnan(targetPrice) else targetPrice

    @property
    def targetPriceRatio(self) -> float:
        return round(100 * (self.currentPrice / self.targetPrice - 1), 2)

    @property
    def numberOfAnalystOpinions(self) -> Union[int, float]:
        try:
            return self.data.consensusOutstanding.추정기관수
        except (ValueError, AttributeError):
            return numpy.nan

    @property
    def dividendRate(self) -> float:
        if self.quoteType == "ETF":
            return numpy.nan
        return self.data.abstract.배당수익률[-2]

    @property
    def fiveYearAverageDividendRate(self) -> float:
        if self.quoteType == "ETF":
            return numpy.nan
        return round(self.data.abstract["배당수익률"].astype(float)[:-1].mean(), 2)

    @property
    def fiveYearAverageDividendYield(self) -> float:
        return self.fiveYearAverageDividendRate

    @property
    def dividendYield(self) -> float:
        return self.data.multiplesTrailing.dividendYield

    @property
    def fiscalPE(self) -> float:
        return round(self.data.currentPrice / self.fiscalEps, 2)

    @property
    def trailingPE(self) -> float:
        return self.data.multiplesTrailing.trailingPE

    @property
    def forwardPE(self) -> float:
        return round(self.currentPrice / self.forwardEps, 2)

    @property
    def estimatePE(self) -> float:
        return self.data.multiplesTrailing.estimatePE

    @property
    def sectorPE(self) -> float:
        return self.data.multiplesOutstanding.sectorPE

    @property
    def fiscalEps(self) -> int:
        try:
            return int(self.previousClose / self.data.multiplesOutstanding.fiscalPE)
        except ValueError:
            return numpy.nan

    @property
    def trailingEps(self) -> int:
        return self.data.multiplesTrailing.trailingEps

    @property
    def forwardEps(self) -> int:
        try:
            return int(self.previousClose / self.data.multiplesOutstanding.forwardPE)
        except ValueError:
            return numpy.nan

    @property
    def estimateEps(self) -> int:
        return self.data.multiplesTrailing.estimateEps

    @property
    def priceToBook(self) -> float:
        return self.data.multiplesTrailing.priceToBook

    @property
    def bookValue(self) -> int:
        return int(self.data.multiplesTrailing.bookValue)

    @property
    def heldPercentInsiders(self) -> float:
        return round(100 - self.data.shareHolders.공시제외주주, 2)

    @property
    def heldPercentInstitutions(self) -> float:
        return self.data.shareInstitutes.상장주식수내비중.sum()

    @property
    def returnOnAssets(self) -> float:
        return self.data.abstract.ROA[-2]

    @property
    def returnOnEquity(self) -> float:
        return self.data.abstract.ROE[-2]

    @property
    def fiscalSps(self) -> int:
        return int(self.data.multiples.SPS[-2])

    @property
    def priceToSales(self) -> float:
        return round(self.currentPrice / self.fiscalSps, 2)

    @property
    def earningsGrowth(self) -> float:
        growth = self.data.growthRate
        return growth.iloc[-2, 1]

    @property
    def revenueGrowth(self) -> float:
        growth = self.data.growthRate
        return growth.iloc[-2, 0]

    @property
    def pegRatio(self) -> float:
        return round(self.trailingPE / self.earningsGrowth, 2)





if __name__ == "__main__":
    pandas.set_option('display.expand_frame_repr', False)
    t = Ticker(
        # "005930" # SamsungElec
        # "000660" # SK hynix
        # "207940" # SAMSUNG BIOLOGICS
        # "005380" # HyundaiMtr
        # "005490" # POSCO
        # "035420" # NAVER Corporation
        # "000270" # Kia Corporation
        # "051910" # LG Chem, Ltd.
        # "006400" # Samsung SDI Co., Ltd.
        # "068270" # Celltrion, Inc.
        # "035720" # Kakao Corp.
        # "028260" # Samsung C&T Corporation
        # "105560" # KB Financial Group Inc.
        # "012330" # Mobis
        # "055550" # Shinhan Financial Group Co., Ltd.
        # "066570" # LG Electronics Inc.
        # "032830" # Samsung Life Insurance Co., Ltd.
        # "096770" # SK Innovation Co., Ltd.
        # "003550" # LG Corp.
        # "015760" # Korea Electric Power Corporation
        # "017670" # SK Telecom Co.,Ltd
        # "316140" # Woori Financial Group Inc.

        "359090" # C&R Research
        # "042660"  # Daewoo Shipbuilding & Marine Engineering Co.,Ltd
        # "021080" # Atinum Investment
        # "130500" # GH Advanced Materials Inc.
        # "323280" # SHT-5 SPAC

        # "102780" # KODEX 삼성그룹
    )
    # print(t.name)
    # print(t.description)


    import random
    tickers = random.sample(metaData.equityKOR.index.tolist(), 10)
    for ticker in tickers:
        print(ticker, "...." * 15)
        print(Ticker(ticker).description)

