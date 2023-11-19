from labwons.common.metadata.metadata import MetaData
from labwons.common.config import PATH
from labwons.equity.source.fnguide.stock import fnguide
from labwons.equity.source.naver.stock import naver
from labwons.common.tools import int2won
from pykrx.stock import get_market_ohlcv_by_date
from typing import Union
from datetime import datetime, timedelta
from pytz import timezone
import pandas as pd
import numpy as np
import os


class krstock(naver, fnguide):

    def __init__(
            self,
            ticker: str,
            period: int = 10,
            enddate: str = "",
            freq: str = "d",
            language: str = "eng"
    ):
        """
        :param ticker   :
        :param language : [str] one of ["eng", "kor"], default "eng"
        :param period   : [int] year
        :param enddate  : [str] format "%Y%m%d"
        :param freq     : [str] one of ['d', 'm', 'y'], default "d"
        """
        super().__init__(ticker=ticker)
        super().__init__(ticker=ticker)
        self.ticker   = ticker
        self.language = language
        if ticker in MetaData.index:
            self._prop = MetaData.loc[ticker].to_dict()
        else:
            self._prop = dict(zip(MetaData.columns, [np.nan] * len(MetaData.columns)))

        self.period = period
        self.enddate = enddate if enddate else datetime.now(timezone('Asia/Seoul')).strftime("%Y%m%d")
        self.freq = freq
        self._attr = lambda x: f"_{x}_{self.period}_{self.enddate}_{self.freq}_"
        return

    def __str__(self) -> str:
        return str(self.describe("series"))

    def describe(self, mode:str="dict") -> Union[dict, pd.DataFrame, pd.Series]:
        data = {
            "ticker": self.ticker,
            "name": self.name,
            "country": self.country,
            "quoteType": self.quoteType,
            "exchange": self.exchange,
            "currency": self.currency,
            "sector": self.sector,
            "benchmark": f"{self.benchmarkName}({self.benchmarkTicker})",
            "currentPrice": f"{self.currentPrice: ,d}",
            "previousPrice": f"{self.previousClose: ,d}",
            "marketCap": int2won(self.marketCap) if self.language == "kor" else self.marketCap,
            "volume": f"{self.volume: ,d}",
            "floatSharesRate": self.floatSharesRate,
            "foreignRate": self.previousForeignRate,
            "fiftyTwoWeekHigh": f"{self.fiftyTwoWeekHigh: ,d}",
            "%fiftyTwoWeekHigh": self.fiftyTwoWeekHighRate,
            "fiftyTwoWeekLow": f"{self.fiftyTwoWeekLow: ,d}",
            "%fiftyTwoWeekLow": self.fiftyTwoWeekLowRate,
            "targetPrice": self.targetPrice,
            "dividendYield": self.dividendYield,
            "beta": self.beta,
            "fiscalPE": self.fiscalPE,
            "trailingPE": self.trailingPE,
            "forwardPE": self.forwardPE,
            "fiscalEps": f"{self.fiscalEps: ,d}",
            "trailingEps": f"{self.trailingEps: ,d}",
            "forwardEps": f"{int(round(self.previousClose / self.forwardPE, 0)): ,d}",
            "priceToBook": self.priceToBook,
            "fiscalPS": self.fiscalPS,
            "pegRatio": self.pegRatio
        }
        if mode.lower() == "series":
            return pd.Series(data=data, name=self.ticker)
        if mode.lower() == "dataframe":
            return pd.DataFrame(data=data, index=[self.ticker])
        return data

    @property
    def name(self) -> str:
        return self._prop["korName"] if self.language == "kor" else self._prop["shortName"]

    @property
    def country(self) -> str:
        return self._prop["country"]

    @property
    def quoteType(self) -> str:
        return "equity"

    @property
    def exchange(self) -> str:
        return self._prop["exchange"]

    @property
    def currency(self) -> str:
        return "원" if self.language == "kor" else "KRW"

    @property
    def sector(self) -> str:
        return self._prop["sector"]

    @property
    def industry(self) -> str:
        return self._prop["industry"]

    @property
    def benchmarkTicker(self) -> str:
        return self._prop["benchmarkTicker"]

    @property
    def benchmarkName(self) -> str:
        return self._prop["benchmarkName"]

    @property
    def path(self) -> str:
        return os.path.join(PATH.BASE, f"{self.ticker}_{self.name}")

    @property
    def pegRatio(self) -> float:
        return round(self.trailingPE / self.trailingEpsGrowth, 2)

    @property
    def ohlcv(self) -> pd.DataFrame:
        if not hasattr(self, self._attr("ohlcv")):
            startdate = (datetime.strptime(self.enddate, "%Y%m%d") - timedelta(365 * self.period)).strftime('%Y%m%d')
            ohlcv = get_market_ohlcv_by_date(fromdate=startdate, todate=self.enddate, ticker=self.ticker, freq=self.freq)
            trade_stop = ohlcv[ohlcv["시가"] == 0].copy()
            if not trade_stop.empty:
                ohlcv.loc[trade_stop.index, ['시가', '고가', '저가']] = trade_stop['종가']
            ohlcv.index.name = '날짜'
            if self.language == "eng":
                ohlcv = ohlcv.rename(columns=dict(시가='open', 고가='high', 저가='low', 종가='close', 거래량='volume'))
            self.__setattr__(self._attr("ohlcv"), ohlcv)
        return self.__getattribute__(self._attr("ohlcv"))


if __name__ == "__main__":
    ticker = '316140'

    stock = krstock(ticker)
    print(stock)
    # print(stock.ticker)


