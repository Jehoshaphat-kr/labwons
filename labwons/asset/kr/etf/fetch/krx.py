from labwons.common.metadata import metaData
from datetime import datetime, timedelta
from pandas import DataFrame
from pykrx.stock import get_etf_portfolio_deposit_file, get_market_ohlcv_by_date


def getComponents(ticker:str) -> DataFrame:
    """
    :return:
                            이름        비중
        티커
        005930          삼성전자  26.469999
        006400           삼성SDI  18.270000
        207940  삼성바이오로직스  10.450000
        028260          삼성물산   8.730000
        000810          삼성화재   6.720000
        009150          삼성전기   6.400000
        032830          삼성생명   5.080000
        010140        삼성중공업   3.960000
        018260    삼성에스디에스   3.640000
        028050    삼성엔지니어링   3.490000
        016360          삼성증권   1.830000
        008770          호텔신라   1.760000
        012750            에스원   1.150000
        030000          제일기획   1.130000
        029780          삼성카드   0.600000
    """
    data = get_etf_portfolio_deposit_file(ticker)
    data['이름'] = metaData[metaData.index.isin(data.index)]['korName']
    return data[['이름', '비중']]

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
