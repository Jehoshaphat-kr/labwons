from typing import Union
from datetime import datetime, timedelta
from pykrx.stock import get_market_ohlcv_by_date
from ta import add_all_ta_features
from pandas import DataFrame
from yfinance import Ticker
import pandas


class price(object):

    _ed_:datetime.date = datetime.today().date()
    _pr_:int = 10
    _fq_:str = 'd' # one of ['d', 'm', 'y'] or ['30m', '60m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    def __init__(self, ticker:str, country:str):
        self.ticker, self.country = ticker, country
        self._ed_ = datetime.today().date()
        self._pr_ = 10
        self._fq_ = 'd' if country == "KOR" else '1d'
        return

    def _krse(self) -> DataFrame:
        ohlcv = get_market_ohlcv_by_date(
            fromdate=(self._ed_ - timedelta(365 * self._pr_)).strftime("%Y%m%d"),
            todate=self.enddate,
            ticker=self.ticker,
            freq=self.freq
        )
        ohlcv = ohlcv.rename(columns=dict(시가='open', 고가='high', 저가='low', 종가='close', 거래량='volume'))

        trade_stop = ohlcv[ohlcv["open"] == 0].copy()
        if not trade_stop.empty:
            ohlcv.loc[trade_stop.index, ['open', 'high', 'low']] = trade_stop['close']
        ohlcv.index.name = 'date'
        return ohlcv

    def _nyse(self) -> DataFrame:
        columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        ohlcv = Ticker(self.ticker).history(period=f'{self._pr_}y', interval=self._fq_)[columns]
        ohlcv = ohlcv.rename(columns=dict(zip(columns, [n.lower() for n in columns])))
        ohlcv['date'] = pandas.to_datetime(ohlcv.index)
        ohlcv['date'] = ohlcv['date'].dt.tz_convert('Asia/Seoul')
        ohlcv.index = ohlcv['date'].dt.date
        return ohlcv.drop(columns=['date'])

    def attr(self, key:str):
        return f"_{self.enddate}_{self.period}_{self.freq}_{key}"

    @property
    def enddate(self) -> str:
        return self._ed_.strftime("%Y%m%d")

    @enddate.setter
    def enddate(self, enddate:Union[str, datetime, datetime.date]):
        if isinstance(enddate, str):
            self._ed_ = datetime.strptime(enddate, "%Y%m%d").date()
        elif isinstance(enddate, datetime):
            self._ed_ = enddate.date()
        else:
            self._ed_ = enddate

    @property
    def period(self) -> int:
        return self._pr_

    @period.setter
    def period(self, period:int):
        self._pr_ = period

    @property
    def freq(self) -> str:
        return self._fq_

    @freq.setter
    def freq(self, freq:str):
        if self.country == "KOR":
            discreminator = ['d', 'm', 'y']
        else:
            discreminator = ['30m', '60m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
        if not freq in discreminator:
            raise KeyError
        self._fq_ = freq

    @property
    def price(self) -> DataFrame:
        attr = self.attr("price")
        if not hasattr(self, attr):
            if self.country == "KOR":
                self.__setattr__(attr, self._krse())
            else:
                self.__setattr__(attr, self._nyse())
        return self.__getattribute__(attr)

    @property
    def ta(self) -> DataFrame:
        attr = self.attr("ta")
        if not hasattr(self, attr):
            self.__setattr__(attr, add_all_ta_features(self.price.copy(), 'open', 'high', 'low', 'close', 'volume'))
        return self.__getattribute__(attr)