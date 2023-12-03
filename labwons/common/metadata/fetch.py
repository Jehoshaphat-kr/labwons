from labwons.common.tools import xml2df
from datetime import datetime
from stocksymbol import StockSymbol
from bs4 import BeautifulSoup
from pykrx.stock import (
    get_nearest_business_day_in_a_week,
    get_market_cap_by_ticker,
    get_market_fundamental,
    get_index_ticker_name,
    get_index_ticker_list
)
import urllib.request as req
import pandas as pd
import requests, time, json


def fetchWiseDate() -> str:
    """
    WISE INDEX latest date
    :return: [str]
    """
    url = 'http://www.wiseindex.com/Index/Index#/G1010.0.Components'
    req = requests.get(url=url)
    if not req.status_code == 200:
        raise ConnectionError('Source Connection Error: Wise Index')

    date = [p.text for p in BeautifulSoup(req.text, 'lxml').find_all('p') if "기준일" in p.text][0]
    return date.replace("기준일 : 20", "").replace('.', '')

def fetchWiseIndustry(date:str, sec_cd:str) -> pd.DataFrame:
    """
    WISE INDEX single industry deposits
    :param date  : [str]
    :param sec_cd: [str]
    :return:
    """
    from labwons.common.config import MAX_TRY_COUNT
    columns = dict(CMP_CD='ticker', CMP_KOR='korName', SEC_NM_KOR='sector', IDX_NM_KOR='industry')
    for try_count in range(MAX_TRY_COUNT):
        req = requests.get(f'http://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt={date}&sec_cd={sec_cd}')
        if req.status_code == 200:
            print(pd.DataFrame(
                data=req.json()['list']
            ))
            return pd.DataFrame(
                data=req.json()['list']
            ).rename(columns=columns)[columns.values()].set_index(keys='ticker')
        time.sleep(5)
    raise ConnectionError(f"Timeout Error: Failed to connect, while fetching: {sec_cd}")

def fetchKrxEnglish(api:str) -> pd.DataFrame:
    """
    Stock Symbol "https://pypi.org/project/stocksymbol/"
    :param api: [str]
    :return:
    """
    kr = pd.DataFrame(data=StockSymbol(api).get_symbol_list(market='kr'))
    kr['ticker'] = kr.symbol.str.split('.').str[0]
    kr['country'] = 'KOR'
    return kr.set_index(keys='ticker')[['shortName', 'longName', 'quoteType', 'country']]

def fetchKrxEtf() -> pd.DataFrame:
    """
    Fetch Korean Stock Exchange(KRX) Listed ETF
    :return:
    """
    url = 'https://finance.naver.com/api/sise/etfItemList.nhn'
    key_prev = ['itemcode', 'itemname', 'nowVal', 'marketSum']
    key_curr = ['ticker', 'name', 'close', 'marketCap']
    df = pd.DataFrame(json.loads(req.urlopen(url).read().decode('cp949'))['result']['etfItemList'])
    df = df[key_prev].rename(columns=dict(zip(key_prev, key_curr)))
    df['marketCap'] = df['marketCap'] * 100000000
    df['exchange'] = 'KOSPI'
    df['quoteType'] = 'ETF'
    df['currency'] = 'KRW'
    df['country'] = 'KOR'
    return df.set_index(keys='ticker').drop_duplicates()

def fetchNyse(api:str) -> pd.DataFrame:
    """
    Fetch NYSE tickers from Stock Symbol
    :return:
    """
    df = pd.DataFrame(StockSymbol(api).get_symbol_list(market='us'))
    df = df.rename(columns=dict(symbol='ticker')).set_index(keys='ticker')
    df['name'] = df['longName']
    df['quoteType'] = 'EQUITY'
    df['currency'] = 'USD'
    df['country'] = 'USA'
    df['benchmarkTicker'] = df['exchange'].apply(lambda x: 'QQQ' if x == 'NASDAQ' else 'SPY')
    df['benchmarkName'] = df['exchange'].apply(lambda x: 'Nasdaq' if x == 'NASDAQ' else 'S&P500')
    return df[[
        'name', 'shortName', 'longName', 'exchange', 'quoteType', 'currency', 'country', 'benchmarkTicker', 'benchmarkName'
    ]]

def fetchNyseEtfWikipedia() -> pd.DataFrame:
    """
    Fetch NYSE ETF tickers from Wikipedia
    :return:
    """
    def form(text:str) -> dict:
        io = [n for n, _ in enumerate(text) if _ == '('][-1] if text.count('(') > 1 else text.index('(')
        ic = [n for n, _ in enumerate(text) if _ == ')'][-1] if text.count(')') > 1 else text.index(')')
        dr = text[io + 1: ic].replace(':', '').replace('|', '').replace(' ', '').replace('\xa0', '').lower()
        tn = dr.replace('nysearca', '').replace('nasdaq', '').upper()
        ex = 'NASDAQ' if 'nasdaq' in dr else 'NYSE'
        return dict(ticker=tn, name=tn, exchange=ex, quoteType='ETF', currency='USD', country='USA')

    data = list()
    url = "https://en.wikipedia.org/wiki/List_of_American_exchange-traded_funds"
    src = BeautifulSoup(requests.get(url).text, "html.parser")
    for _1row in src.find_all('li'):
        raw = _1row.text.lower()
        if ('nyse' in raw or 'nasdaq' in raw) and '(' in raw and ')' in raw:
            before = _1row.text
            for _2row in _1row.find_all('li'):
                data.append(form(_2row.text))
                before = before.replace(_2row.text, '')
            data.append(form(before))
    return pd.DataFrame(data=data).set_index(keys='ticker')

def fetchNyseEtfNasdaq() -> pd.DataFrame:
    """
    Fetch NYSE ETF tickers from NASDAQ
    :return:
    """
    data = list()
    url = "https://www.nasdaqtrader.com/trader.aspx?id=etf_definitions"
    src = BeautifulSoup(requests.get(url).text, "html.parser")
    for row in src.find_all('tr')[1:]:
        ticker, comment = (d.text for d in row.find_all('td')[:2])
        data.append(dict(
            ticker=ticker,
            name=ticker,
            exchange='NASDAQ',
            quoteType='ETF',
            currency='USD',
            country='USA',
            benchmarkTicker='QQQ',
            benchmarkName='NASDAQ'
        ))
    return pd.DataFrame(data=data).set_index(keys='ticker')

def fetchNyseEtfCBOE() -> pd.DataFrame:
    """
    Fetch NYSE ETF tickers from CBOE
    :return:
    """
    data = list()
    url = "https://www.cboe.com/us/equities/market_statistics/listed_symbols/xml/"
    src = BeautifulSoup(requests.get(url).text, "lxml")
    for s in src.find_all("symbol"):
        data.append(dict(ticker=s['name'], name=s['name'], exchange='CBOE', quoteType='ETF', currency='USD', country='USA'))
    return pd.DataFrame(data=data).set_index(keys='ticker').drop_duplicates()

def fetchECOS(api) -> pd.DataFrame:
    """
    Fetch ECOS tickers from ECOS
    :return:
    """
    df = xml2df(url=f'http://ecos.bok.or.kr/api/StatisticTableList/{api}/xml/kr/1/10000/')
    df = df[df.SRCH_YN == 'Y'].copy()
    df['STAT_NAME'] = df.STAT_NAME.apply(lambda x: x[x.find(' ') + 1:])
    df = df.rename(columns=dict(STAT_CODE='ticker', STAT_NAME='name', CYCLE='cycle', ORG_NAME='by'))
    df['exchange'] = 'ECOS'
    df['quoteType'] = 'INDEX'
    df['currency'] = '%, 억, -'
    return df[['ticker', 'name', 'exchange', 'quoteType', 'cycle']].set_index(keys='ticker')

def fetchKrxIndex() -> pd.DataFrame:
    """
    :return:
                      KOSPI                                KOSDAQ               KRX                      테마
        지수         지수명   지수                         지수명  지수      지수명  지수              지수명
    0   1001         코스피   2001                         코스닥  5042     KRX 100  1163    코스피 고배당 50
    1   1002  코스피 대형주   2002                  코스닥 대형주  5043  KRX 자동차  1164  코스피 배당성장 50
    ...  ...            ...    ...                            ...   ...        ...    ...                 ...
    48   NaN            NaN   2217            코스닥 150 헬스케어   NaN        NaN    NaN                 NaN
    49   NaN            NaN   2218  코스닥 150 커뮤니케이션서비스   NaN        NaN    NaN                 NaN
    """
    objs = dict()
    for market in ('KOSPI', 'KOSDAQ', 'KRX', '테마'):
        indices = get_index_ticker_list(market=market)
        names = [get_index_ticker_name(i) for i in indices]
        objs[market] = pd.DataFrame(data={'지수': indices, '지수명': names})
    return pd.concat(objs=objs, axis=1)

def fetchKrseMarketCapMultipleIpo() -> pd.DataFrame:
    """
    Fetch KRX Market Cap, Volume, ..., Multiples and IPO
    :return:
             close        marketCap    volume    ...     BPS     PER   PBR      EPS   DIV      DPS         IPO
    005930   72000  429824343600000  13194571  ...   57822.0    8.94  1.25   8057.0  2.01   1444.0  1975-06-11
    373220  607000  142038000000000    192569  ...   80052.0  183.61  7.58   3306.0  0.00      0.0  2022-01-27
    000660  119500   86996282617500   6221769  ...   92004.0   36.86  1.30   3242.0  1.00   1200.0  1996-12-26
    ...        ...              ...       ...  ...       ...     ...   ...      ...   ...      ...         ...
    245450    1599       2526356040         1  ...       NaN     NaN   NaN      NaN   NaN      NaN  2016-06-24
    288490      56       2136232000    264148  ...       NaN     NaN   NaN      NaN   NaN      NaN         NaT
    000547   12140       1864704000      8664  ...       NaN     NaN   NaN      NaN   NaN      NaN         NaT
    """
    date = get_nearest_business_day_in_a_week(datetime.today().strftime("%Y%m%d"))
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
    kwargs = dict(date=date, market="ALL", alternative=True)

    caps_cols = dict(종가='close', 시가총액='marketCap', 거래량='volume')
    caps = get_market_cap_by_ticker(**kwargs).rename(columns=caps_cols).drop_duplicates()[caps_cols.values()]

    muls = get_market_fundamental(**kwargs).drop_duplicates()

    ipo = pd.read_html(io=url, header=0)[0][['종목코드', '상장일']]
    ipo = ipo.rename(columns=dict(종목코드='ticker', 상장일='IPO')).set_index(keys='ticker')
    ipo.index = ipo.index.astype(str).str.zfill(6)
    ipo.IPO = pd.to_datetime(ipo.IPO)
    ipo = ipo[ipo.IPO <= datetime.strptime(date, "%Y%m%d")].drop_duplicates()
    return pd.concat([caps, muls, ipo], axis=1)

def getEcosContains(api:str, ticker:str) -> pd.DataFrame:
    """
    ECOS ticker specific data contains
    :param api   : [str]
    :param ticker: [str]
    :return:
    """
    columns = dict(
        ITEM_NAME='이름',
        ITEM_CODE='코드',
        CYCLE='주기',
        START_TIME='시점',
        END_TIME='종점',
        DATA_CNT='개수'
    )
    url = f"http://ecos.bok.or.kr/api/StatisticItemList/{api}/xml/kr/1/10000/{ticker}"
    return xml2df(url=url)[columns.keys()].rename(columns=columns)


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)

    print(fetchWiseDate())
    # print(fetchWiseIndustry('231201', 'WI100'))
    # print(fetchKrxEnglish("95012214-44b0-4664-813f-a7ef5ad3b0b4"))
    # df = fetchNyse("95012214-44b0-4664-813f-a7ef5ad3b0b4")
    # df = fetchNyseEtfWikipedia()
    # print(df.loc['QQQ'])
    #
    # df = fetchNyseEtfNasdaq()
    # print(df.loc['QQQ'])

