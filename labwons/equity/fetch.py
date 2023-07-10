from labwons.equity.ticker import _ticker
from pykrx.stock import get_market_ohlcv_by_date
from datetime import datetime, timedelta
from pytz import timezone
import pandas as pd
import yfinance as yf


class _fetch(_ticker):

    def __init__(self, ticker:str, **kwargs):
        super().__init__(ticker=ticker, **kwargs)

        self._period = 20
        self._ddate = datetime.now(timezone('Asia/Seoul')).date()
        self._freq = 'd' if self.market == 'KOR' else '1d'
        return

    @staticmethod
    def fetchKrse(ticker: str = '', startdate: str = '', enddate: str = '', freq: str = '') -> pd.DataFrame:
        ohlcv = get_market_ohlcv_by_date(
            fromdate=startdate,
            todate=enddate,
            ticker=ticker,
            freq=freq
        )
        ohlcv = ohlcv.rename(columns=dict(시가='open', 고가='high', 저가='low', 종가='close', 거래량='volume'))

        trade_stop = ohlcv[ohlcv.open == 0].copy()
        if not trade_stop.empty:
            ohlcv.loc[trade_stop.index, ['open', 'high', 'low']] = trade_stop['close']
        ohlcv.index.name = 'date'
        return ohlcv

    @staticmethod
    def fetchNyse(ticker: str, period: int, freq: str) -> pd.DataFrame:
        columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        ohlcv = yf.Ticker(ticker).history(period=f'{period}y', interval=freq)[columns]
        ohlcv = ohlcv.rename(columns=dict(zip(columns, [n.lower() for n in columns])))
        ohlcv['date'] = pd.to_datetime(ohlcv.index)
        ohlcv['date'] = ohlcv['date'].dt.tz_convert('Asia/Seoul')
        ohlcv.index = ohlcv['date'].dt.date
        return ohlcv.drop(columns=['date'])

    @property
    def enddate(self) -> str:
        return self._ddate.strftime("%Y%m%d")

    @enddate.setter
    def enddate(self, enddate:str or datetime):
        self._ddate = datetime.strptime(enddate, "%Y%m%d") if isinstance(enddate, str) else enddate

    @property
    def startdate(self) -> str:
        return (self._ddate - timedelta(365 * self.period)).strftime("%Y%m%d")

    @property
    def period(self) -> int:
        return self._period

    @period.setter
    def period(self, period:int):
        self._period = period

    @property
    def freq(self) -> str:
        return self._freq

    @freq.setter
    def freq(self, freq:str):
        if (self.market == 'KOR' and not freq in ['d', 'm', 'y']) or \
           (self.market == 'USA' and not freq in ['30m', '60m', '1h', '1d', '5d', '1wk', '1mo', '3mo']):
            raise KeyError(f"Frequency key error for market: {self.market}: {freq}")
        self._freq = freq

    def getOhlcv(self) -> pd.DataFrame:
        attr = f'_fetch_{self.enddate}_{self.period}_{self.freq}'
        if not hasattr(self, attr):
            if self.market == 'KOR':
                self.__setattr__(attr, self.fetchKrse(self.ticker, self.startdate, self.enddate, self.freq))
            elif self.market == 'USA':
                self.__setattr__(attr, self.fetchNyse(self.ticker, self.period, self.freq))
            else:
                raise AttributeError(f"Unknown Market: {self.market}({self.exchange}) is an invalid attribute.")
        return self.__getattribute__(attr)

    # @property
    # def benchmark(self) -> pd.DataFrame:
    #     attr = f'_bench_{self.enddate}_{self.period}_{self.freq}'
    #     if not hasattr(self, attr):
    #         if self.market == 'KOR' and self.benchmarkTicker:
    #             df = self.fetchKrse(self.benchmarkTicker, self.startdate, self.enddate, self.freq)
    #         elif self.market == 'USA' and self.benchmarkTicker:
    #             df = self.fetchNyse(self.benchmarkTicker, self.period, self.freq)
    #         else:
    #             df = pd.DataFrame(columns=['open', 'close', 'high', 'low', 'volume'])
    #
    #         objs = dict()
    #         for col in self.ohlcv.columns:
    #             objs[(col, self.name)] = self.ohlcv[col]
    #             objs[(col, self.benchmarkName)] = df[col]
    #         self.__setattr__(attr, pd.concat(objs=objs, axis=1))
    #     return self.__getattribute__(attr)

    # @property
    # def open(self) -> pd.Series:
    #     _ = self.ohlcv.open
    #     _.name = f"{self.name}(O)"
    #     return _
    #
    # @property
    # def high(self) -> pd.Series:
    #     _ = self.ohlcv.high
    #     _.name = f"{self.name}(H)"
    #     return _
    #
    # @property
    # def low(self) -> pd.Series:
    #     _ = self.ohlcv.low
    #     _.name = f"{self.name}(L)"
    #     return _
    #
    # @property
    # def close(self) -> pd.Series:
    #     _ = self.ohlcv.close
    #     _.name = f"{self.name}(C)"
    #     return _

    # @property
    # def typical(self) -> pd.Series:
    #     _ = (self.ohlcv['high'] + self.ohlcv['low'] + self.ohlcv['close']) / 3
    #     _.name = f"{self.name}(T)"
    #     return _


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)
    API_ECOS = "CEW3KQU603E6GA8VX0O9"

    test = _fetch(ticker='005930')
    # test = _fetch(ticker='TSLA')
    # test = _fetch(ticker='KRE')
    # test = _fetch(ticker='DGS10')
    # test = _fetch(ticker="151Y003", ecoskeys=["예금은행", "전국"])
    # test = _fetch(ticker="121Y002", ecoskeys=["저축성수신"], name='평균수신')
    # test = _fetch(ticker='LORSGPRT', market='KOR')
    print(test.ticker)
    print(test.exchange)
    print(test.ohlcv)
    print(test.benchmark)

    """
    1) BSCICP03: OECD Standardised BCI, Amplitude adjusted(Long term average = 100), sa
    2) CSCICP03: OECD Standardised CCI, Amplitude adjusted(Long term average = 100), sa
    3) LOLITOAA: Amplitude adjusted(CLI)
    4) LOLITONO: Normalised(CLI)
    5) LOLITOTR_STSA: Trend restored(CLI)
    6) LOLITOTR_GYSA: 12 - month rate of change of the trend restored CLI
    7) LORSGPRT: Ratio to trend(GDP)
    8) LORSGPNO: Normalised(GDP)
    9) LORSGPTD: Trend(GDP)
    """
