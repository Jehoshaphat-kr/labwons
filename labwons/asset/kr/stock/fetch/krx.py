from datetime import datetime, timedelta
from pandas import Series, DataFrame
from pykrx.stock import get_market_cap_by_date, get_market_ohlcv_by_date


def getMarketCap(ticker:str) -> Series:
    """
    :return:
        2019/03     93522
        2019/06     95563
        2019/09     89922
            ...       ...
        2023/03     83071
        2023/06     85838
        2023/09     93241
        2023/11     95497
        Name: 시가총액, dtype: int32
    """

    cap = get_market_cap_by_date(
        fromdate=(datetime.today() - timedelta(365 * 5)).strftime("%Y%m%d"),
        todate=datetime.today().strftime("%Y%m%d"),
        freq='m',
        ticker=ticker
    )
    cap = cap[
        cap.index.astype(str).str.contains('03') | \
        cap.index.astype(str).str.contains('06') | \
        cap.index.astype(str).str.contains('09') | \
        cap.index.astype(str).str.contains('12') | \
        (cap.index == cap.index[-1])
    ]
    cap.index = cap.index.strftime("%Y/%m")
    return Series(index=cap.index, data=cap['시가총액'] / 100000000, dtype=int)

def getOhlcv(ticker:str, period:int=10, freq:str='d') -> DataFrame:
    """
    :param ticker : [str]
    :param period : [int]
    :param freq   : [str]
    :return:
                     시가   고가   저가   종가    거래량
        날짜
        2013-12-13  28200  28220  27800  27800    201065
        2013-12-16  27820  28080  27660  28000    179088
        2013-12-17  28340  28340  27860  27900    155248
        ...           ...    ...    ...    ...       ...
        2023-12-07  71800  71900  71100  71500   8862017
        2023-12-08  72100  72800  71900  72600  10859463
        2023-12-11  72800  73000  72200  73000   9406504
    """
    todate = datetime.today().strftime("%Y%m%d")
    frdate = (datetime.today() - timedelta(365 * period)).strftime("%Y%m%d")
    ohlcv = get_market_ohlcv_by_date(
        fromdate=frdate,
        todate=todate,
        ticker=ticker,
        freq=freq
    )

    trade_stop = ohlcv[ohlcv.시가 == 0].copy()
    if not trade_stop.empty:
        ohlcv.loc[trade_stop.index, ['시가', '고가', '저가']] = trade_stop.종가
    ohlcv.index.name = '날짜'
    # return ohlcv.rename(columns=dict(시가='open', 고가='high', 저가='low', 종가='close', 거래량='volume'))
    return ohlcv