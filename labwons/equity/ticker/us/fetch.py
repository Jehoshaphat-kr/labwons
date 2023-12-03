from typing import Union
from datetime import datetime
import yfinance, requests, warnings, pandas


class equity(object):

    _ed_:datetime.date = datetime.today().date()
    _pr_:int = 10
    _fq_:str = '1d'
    def __init__(self, ticker):
        self.ticker = ticker
        self._yahoo = yfinance.Ticker(ticker)
        return

    @property
    def enddate(self) -> str:
        return self._ed_.strftime("%Y%m%d")

    @enddate.setter
    def enddate(self, enddate: Union[str, datetime, datetime.date]):
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
    def period(self, period: int):
        self._pr_ = period

    @property
    def freq(self) -> str:
        return self._fq_

    @freq.setter
    def freq(self, freq: str):
        if not freq in ['30m', '60m', '1h', '1d', '5d', '1wk', '1mo', '3mo']:
            raise KeyError
        self._fq_ = freq

    @property
    def price(self) -> pandas.DataFrame:
        attr = f"_{self.enddate}_{self.period}_{self.freq}_"
        if not hasattr(self, attr):
            columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            ohlcv = self._yahoo.history(period=f'{self._pr_}y', interval=self._fq_)[columns]
            ohlcv = ohlcv.rename(columns=dict(zip(columns, [n.lower() for n in columns])))
            ohlcv['date'] = pandas.to_datetime(ohlcv.index)
            ohlcv['date'] = ohlcv['date'].dt.tz_convert('Asia/Seoul')
            ohlcv.index = ohlcv['date'].dt.date
            self.__setattr__(attr, ohlcv.drop(columns=['date']))
        return self.__getattribute__(attr)

    @property
    def info(self) -> dict:
        try:
            info = self._yahoo.info  # [dict]
            for k, v in info.values():
                print(k, v)
            return info
        except requests.exceptions.HTTPError:
            warnings.warn("Warning: Server Blocked", Warning)
        return {}



if __name__ == "__main__":
    myEquity = equity('AAPL')
    print(myEquity.price)