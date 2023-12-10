from datetime import datetime, timedelta
from typing import Union, Hashable
from pandas import DataFrame, Series, to_datetime
from pykrx.stock import get_market_ohlcv_by_date
from yfinance import Ticker


def __krse__(ticker:Union[str, Hashable], period:int, freq:str) -> DataFrame:
    columns = {"시가": "open", "고가": "high", "저가": "low", "종가": "close", "거래량": "volume"}
    todate = datetime.today().strftime("%Y%m%d")
    frdate = (datetime.today() - timedelta(365 * period)).strftime("%Y%m%d")
    ohlcv = get_market_ohlcv_by_date(fromdate=frdate, todate=todate, ticker=ticker, freq=freq).rename(columns=columns)
    banned = ohlcv[ohlcv.open == 0].copy()
    if not banned.empty:
        ohlcv.loc[banned.index, ['open', 'high', 'low']] = banned.close
    ohlcv.index.name = 'date'
    return ohlcv


def __nyse__(ticker:Union[str, Hashable], period:int, freq:str) -> DataFrame:
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    ohlcv = Ticker(ticker).history(period=f'{period}y', interval=freq)[columns]
    ohlcv = ohlcv.rename(columns=dict(zip(columns, [n.lower() for n in columns])))
    ohlcv['date'] = to_datetime(ohlcv.index)
    ohlcv['date'] = ohlcv['date'].dt.tz_convert('Asia/Seoul')
    ohlcv.index = ohlcv['date'].dt.date
    return ohlcv.drop(columns=['date'])


def getOhlcv(ticker:Series, period:int, freq:str):
    if ticker.country == "KOR":
        return __krse__(ticker.name, period, freq)
    elif ticker.country == "USA":
        return __nyse__(ticker.name, period, freq)
    else:
        raise KeyError
