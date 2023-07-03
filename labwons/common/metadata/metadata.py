from labwons.common.config import OECD, FRED
# from labwons.common.base import xml2df
from stocksymbol import StockSymbol
from pykrx.stock import (
    get_market_cap_by_ticker,
    get_market_fundamental,
    get_etf_ticker_name,
    get_nearest_business_day_in_a_week,
    get_index_ticker_list,
    get_index_ticker_name,
    get_index_portfolio_deposit_file,
)
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests, json
import urllib.request as req


class krse(pd.DataFrame):
    def __init__(self, api:str):
        """
        Korean Stock Exchange(KRSE) Listed Company
        :param api: [str] Stock Symbol api key(https://pypi.org/project/stocksymbol/)
        """

        """
        WISE WI26 Industry-Configured by ticker
        [DataFrame *index]   : 'ticker'
        [DataFrame *columns] : ['korName', 'sector']
        """
        from labwons.common.config import WI26
        from labwons.common.metadata.basis import fetchWiseDate, fetchWiseIndustry
        meta = pd.DataFrame(data=WI26).set_index(keys='id')
        date = fetchWiseDate()
        data = pd.concat(objs=[fetchWiseIndustry(date, cd) for cd in meta.index], axis=0)


        """
        Stock Symbol API: Get English Name of Listed Companies
        [DataFrame *index]   : 'ticker' 
        [DataFrame *columns] : ['shortName', 'longName', 'quoteType', 'market']
        """
        from labwons.common.metadata.basis import fetchKrxEnglish
        data = data.join(fetchKrxEnglish(api), how='left')


        """
        Post Process
        1) Join English Name: ['name', 'korName', 'shortName', 'longName']
        2) Set Representative Name: ['name'] ('shortName' is prior to 'korName')
        3) Set Exchange: KOSPI / KOSDAQ
        """
        from pykrx.stock import get_index_portfolio_deposit_file
        ks = get_index_portfolio_deposit_file('1001', alternative=True)
        kq = get_index_portfolio_deposit_file('2001', alternative=True)

        fdef = lambda x: x['korName'] if pd.isna(x['shortName']) else x['shortName']
        data['name'] = data[['shortName', 'korName']].apply(fdef, axis=1)
        data['exchange'] = ['KOSPI' if t in ks else 'KOSDAQ' if t in kq else 'Unknown' for t in data.index]

        super().__init__(index=data.index, columns=data.columns, data=data.values)
        return


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)

    _api = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
    _krx = krse(_api)
    print(_krx)


# class _metadata(pd.DataFrame):
#     _meta = {
#         'oecd': pd.DataFrame(),
#         'ecos': pd.DataFrame(),
#         'nyse': pd.DataFrame(),
#         'krse': pd.DataFrame(),
#         'ketf': pd.DataFrame(),
#         'uetf': pd.DataFrame(),
#         'fred': pd.DataFrame()
#     }
#     _date = str()
#     _kicm = pd.DataFrame()
#     def __init__(self):
#         src = pd.read_csv(
#             'https://raw.githubusercontent.com/Jehoshaphat-kr/snowball/master/snowball/tickers/metadata.csv',
#             # r'./metadata.csv',
#             index_col='ticker',
#             encoding='utf-8'
#         )
#         super().__init__(index=src.index, columns=src.columns, data=src.values)
#         return
#
#     @property
#     def tdate(self) -> str:
#         if not self._date:
#             self._date = get_nearest_business_day_in_a_week()
#         return self._date
#
#     @tdate.setter
#     def tdate(self, tdate:str):
#         self._date = tdate
#         return
#
#     @property
#     def oecd(self) -> pd.DataFrame:
#         return self[self['exchange'] == 'OECD']
#
#     @property
#     def fred(self) -> pd.DataFrame:
#         return self[self['exchange'] == 'FRED']
#
#     @property
#     def ecos(self) -> pd.DataFrame:
#         return self[self['exchange'] == 'ECOS']
#
#     @property
#     def krse(self) -> pd.DataFrame:
#         return self[(self['quoteType'] == 'EQUITY') & (self['country'] == 'KOR')]
#
#     @property
#     def nyse(self) -> pd.DataFrame:
#         return self[(self['quoteType'] == 'EQUITY') & (self['country'] == 'USA')]
#
#     @property
#     def ketf(self) -> pd.DataFrame:
#         return self[(self['quoteType'] == 'ETF') & (self['country'] == 'KOR')]
#
#     @property
#     def uetf(self) -> pd.DataFrame:
#         return self[(self['quoteType'] == 'ETF') & (self['country'] == 'USA')]
#
#     @staticmethod
#     def getOecd() -> pd.DataFrame:
#         """
#         OECD ticker list
#         :return:
#                             name exchange  quoteType                                        comment
#         ticker
#         BSCICP03             BCI     OECD  INDEX  OECD Standard BCI, Amplitude adjusted (Long te...
#         CSCICP03             CCI     OECD  INDEX  OECD Standard CCI, Amplitude adjusted (Long te...
#         LOLITOAA         CLI(AA)     OECD  INDEX                           Amplitude adjusted (CLI)
#         LOLITONO       CLI(Norm)     OECD  INDEX                                   Normalised (CLI)
#         LOLITOTR_STSA    CLI(TR)     OECD  INDEX                               Trend restored (CLI)
#         LOLITOTR_GYSA   CLI(%TR)     OECD  INDEX  12-month rate of change of the trend restored CLI
#         LORSGPNO       GDP(Norm)     OECD  INDEX                               Ratio to trend (GDP)
#         LORSGPTD          GDP(T)     OECD  INDEX                                   Normalised (GDP)
#         LORSGPRT         GDP(%T)     OECD  INDEX                                        Trend (GDP)
#         """
#         return pd.DataFrame(data=COD_OECD).set_index(keys='ticker')
#
#     @staticmethod
#     def getEcos() -> pd.DataFrame:
#         """
#         Fetch ECOS tickers from ECOS api
#         :return:
#                                                   name exchange  quoteType cycle
#         ticker
#         102Y004  본원통화 구성내역(평잔, 계절조정계열)     ECOS  INDEX     M
#         102Y002        본원통화 구성내역(평잔, 원계열)     ECOS  INDEX     M
#         102Y003  본원통화 구성내역(말잔, 계절조정계열)     ECOS  INDEX     M
#         ...                                        ...      ...    ...   ...
#         251Y003                                   총량     ECOS  INDEX     A
#         251Y002                         한국/북한 배율     ECOS  INDEX     A
#         251Y001           북한의 경제활동별 국내총생산     ECOS  INDEX     A
#         """
#         df = xml2df(url=f'http://ecos.bok.or.kr/api/StatisticTableList/{API_ECOS}/xml/kr/1/10000/')
#         df = df[df.SRCH_YN == 'Y'].copy()
#         df['STAT_NAME'] = df.STAT_NAME.apply(lambda x: x[x.find(' ') + 1:])
#         df = df.rename(columns=dict(STAT_CODE='ticker', STAT_NAME='name', CYCLE='cycle', ORG_NAME='by'))
#         df['exchange'] = 'ECOS'
#         df['quoteType'] = 'INDEX'
#         df['unit'] = '%, 억, -'
#         return df[['ticker', 'name', 'exchange', 'quoteType', 'cycle']].set_index(keys='ticker')
#
#     @staticmethod
#     def getFred() -> pd.DataFrame:
#         """
#         Fetch FRED representatives tickers
#         :return:
#                                              name exchange  quoteType  unit                                    comment
#         ticker
#         FEDFUNDS  Federal Funds Effective Rate(M)     FRED      INDEX     %     Federal Funds Effective Rate (Monthly)
#         DFF       Federal Funds Effective Rate(D)     FRED      INDEX     %       Federal Funds Effective Rate (Daily)
#         ...                                  ...       ...        ...   ...                                        ...
#         PSAVERT              Personal Saving Rate     FRED      INDEX     %             Personal Saving Rate (Monthly)
#         UMCSENT                Consumer Sentiment     FRED      INDEX     -  University of Michigan: Consumer Senti...
#         VIXCLS                                VIX     FRED      INDEX     -         CBOE Volatility Index: VIX (Daily)
#         """
#         return pd.DataFrame(data=COD_FRED).set_index(keys='ticker')
#
#     @staticmethod
#     def getKrse() -> pd.DataFrame:
#         """
#         Fetch <WI26 Category> from WISE INDEX
#         :return:
#                               name     shortName               longName             korName exchange    quoteType unit          sector
#         ticker
#         000020        DongwhaPharm  DongwhaPharm  Dongwha Pharm.Co.,Ltd            동화약품    KOSPI      KRSTOCK  KRW        건강관리
#         000040           KR MOTORS     KR MOTORS     KR Motors Co., Ltd            KR모터스    KOSPI      KRSTOCK  KRW  경기관련소비재
#         000050           Kyungbang     Kyungbang      Kyungbang Co.,Ltd                경방    KOSPI      KRSTOCK  KRW  경기관련소비재
#         ...                    ...           ...                    ...                 ...      ...          ...  ...             ...
#         453340        현대그린푸드           NaN                    NaN        현대그린푸드    KOSPI      KRSTOCK  KRW  경기관련소비재
#         456040                 OCI           NaN                    NaN                 OCI    KOSPI      KRSTOCK  KRW            소재
#         457190  이수스페셜티케미컬           NaN                    NaN  이수스페셜티케미컬    KOSPI      KRSTOCK  KRW            소재
#         """
#         src = requests.get(url='http://www.wiseindex.com/Index/Index#/G1010.0.Components').text
#         tic = src.find("기준일")
#         wdate = src[tic + 6: tic + src[tic:].find("</p>")].replace('.', '')
#
#         data, cols = list(), dict(CMP_CD='ticker', CMP_KOR='korName', SEC_NM_KOR='sector')
#         for c, l in COD_WI26.items():
#             try_counter = 0
#             while try_counter < 5:
#                 r = requests.get(f'http://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt={wdate}&sec_cd={c}')
#                 if not r.status_code == 200:
#                     try_counter += 1
#                     continue
#                 data += r.json()['list']
#                 break
#             if try_counter == 5:
#                 raise ConnectionError(f'Timeout Error: Failed to connect, while fetching {c}/{l}')
#         df = pd.DataFrame(data=data).rename(columns=cols).set_index(keys='ticker').drop_duplicates()
#
#         kr = pd.DataFrame(data=StockSymbol(API_SYMS).get_symbol_list(market='kr'))
#         kr['ticker'] = kr.symbol.str.split('.').str[0]
#         df = df.join(kr.set_index(keys='ticker'), how='left')
#         df['name'] = df.apply(lambda x: x['korName'] if pd.isna(x['shortName']) else x['shortName'], axis=1)
#
#         ks = get_index_portfolio_deposit_file('1001', alternative=True)
#         kq = get_index_portfolio_deposit_file('2001', alternative=True)
#         df['exchange'] = ['KOSPI' if t in ks else 'KOSDAQ' if t in kq else 'Unknown' for t in df.index]
#         df['quoteType'] = 'EQUITY'
#         df['unit'] = 'KRW'
#         df['country'] = 'KOR'
#         df['benchmarkTicker'] = df['IDX_CD'].apply(lambda x: CODE_BENCHMARK[x])
#         df['benchmarkName'] = df['benchmarkTicker'].apply(lambda x: get_etf_ticker_name(x))
#         return df[[
#             'name', 'shortName', 'longName', 'korName', 'exchange', 'quoteType', 'unit', 'sector', 'country',
#             'benchmarkTicker', 'benchmarkName'
#         ]]
#
#     @staticmethod
#     def getKrEtf() -> pd.DataFrame:
#         """
#         Fetch KRX ETF List from Naver
#         :return:
#                                         name   close      marketCap exchange  quoteType
#         ticker
#         069500                     KODEX 200   34725  6068200000000    KOSPI      KRETF
#         357870     TIGER CD금리투자KIS(합성)   52505  4539200000000    KOSPI      KRETF
#         423160    KODEX KOFR금리액티브(합성)  103275  3591700000000    KOSPI      KRETF
#         ...                              ...     ...            ...      ...        ...
#         315480  KBSTAR 200커뮤니케이션서비스   11475     1400000000    KOSPI      KRETF
#         287330          KBSTAR 200생활소비재    5935     1300000000    KOSPI      KRETF
#         287320              KBSTAR 200산업재   12180     1200000000    KOSPI      KRETF
#         """
#         url = 'https://finance.naver.com/api/sise/etfItemList.nhn'
#         key_prev = ['itemcode', 'itemname', 'nowVal', 'marketSum']
#         key_curr = ['ticker', 'name', 'close', 'marketCap']
#         df = pd.DataFrame(json.loads(req.urlopen(url).read().decode('cp949'))['result']['etfItemList'])
#         df = df[key_prev].rename(columns=dict(zip(key_prev, key_curr)))
#         df['marketCap'] = df['marketCap'] * 100000000
#         df['exchange'] = 'KOSPI'
#         df['quoteType'] = 'ETF'
#         df['unit'] = 'KRW'
#         df['country'] = 'KOR'
#         return df.set_index(keys='ticker').drop_duplicates()
#
#     @staticmethod
#     def getNyse() -> pd.DataFrame:
#         """
#         Fetch NYSE tickers from Stock Symbol
#         :return:
#                                      name  shortName                   longName exchange quoteType unit
#         ticker
#         AAPL                   Apple Inc.      apple                 Apple Inc.   NASDAQ   USSTOCK  USD
#         MSFT        Microsoft Corporation  microsoft      Microsoft Corporation   NASDAQ   USSTOCK  USD
#         GOOG                Alphabet Inc.   alphabet              Alphabet Inc.   NASDAQ   USSTOCK  USD
#         ...                           ...        ...                        ...      ...       ...  ...
#         FLCX               flooidCX Corp.                        flooidCX Corp.      OTC   USSTOCK  USD
#         BLEG          BRANDED LEGACY INC.                   BRANDED LEGACY INC.      OTC   USSTOCK  USD
#         RRIF    Rainforest Resources Inc.             Rainforest Resources Inc.      OTC   USSTOCK  USD
#         """
#         df = pd.DataFrame(StockSymbol(API_SYMS).get_symbol_list(market='us'))
#         df['name'] = df['longName']
#         df = df.rename(columns=dict(symbol='ticker')).set_index(keys='ticker')
#         df['quoteType'] = 'EQUITY'
#         df['unit'] = 'USD'
#         df['country'] = 'USA'
#         df['benchmarkTicker'] = df['exchange'].apply(lambda x: 'QQQ' if x == 'NASDAQ' else 'SPY')
#         df['benchmarkName'] = df['exchange'].apply(lambda x: 'Nasdaq' if x == 'NASDAQ' else 'S&P500')
#         return df[[
#             'name', 'shortName', 'longName', 'exchange', 'quoteType', 'unit', 'country', 'benchmarkTicker', 'benchmarkName'
#         ]]
#
#     @staticmethod
#     def getUsEtf() -> pd.DataFrame:
#         """
#         Fetch US ETF List from different sources
#         :return:
#                 name exchange  quoteType                               comment
#         ticker
#         ITOT    ITOT     NYSE      USETF   iShares Core S&P Total US Stock Mkt
#         ACWI    ACWI     NYSE      USETF               iShares MSCI ACWI Index
#         IWV      IWV     NYSE      USETF            iShares Russell 3000 Index
#         ...      ...      ...        ...                                   ...
#         XTJL    XTJL     NYSE      USETF                                   NaN
#         XTOC    XTOC     NYSE      USETF                                   NaN
#         YSEP    YSEP     NYSE      USETF                                   NaN
#         """
#         def cut(text: str) -> dict:
#             io = [n for n, _ in enumerate(text) if _ == '('][-1] if text.count('(') > 1 else text.index('(')
#             ic = [n for n, _ in enumerate(text) if _ == ')'][-1] if text.count(')') > 1 else text.index(')')
#             dr = text[io + 1: ic].replace(':', '').replace('|', '').replace(' ', '').replace('\xa0', '').lower()
#             tn = dr.replace('nysearca', '').replace('nasdaq', '').upper()
#             ex = 'NASDAQ' if 'nasdaq' in dr else 'NYSE'
#             return dict(ticker=tn, name=tn, exchange=ex, quoteType='ETF', unit='USD', country='USA')
#
#         data = list()
#
#         # Get from Wikipedia
#         url = "https://en.wikipedia.org/wiki/List_of_American_exchange-traded_funds"
#         src = BeautifulSoup(requests.get(url).text, "html.parser")
#         for _1row in src.find_all('li'):
#             raw = _1row.text.lower()
#             if ('nyse' in raw or 'nasdaq' in raw) and '(' in raw and ')' in raw:
#                 before = _1row.text
#                 for _2row in _1row.find_all('li'):
#                     data.append(cut(_2row.text))
#                     before = before.replace(_2row.text, '')
#                 data.append(cut(before))
#
#         # Get from NASDAQ
#         url = "https://www.nasdaqtrader.com/trader.aspx?id=etf_definitions"
#         src = BeautifulSoup(requests.get(url).text, "html.parser")
#         for row in src.find_all('tr')[1:]:
#             ticker, comment = (d.text for d in row.find_all('td')[:2])
#             data.append(dict(ticker=ticker, name=ticker, exchange='NASDAQ', quoteType='ETF', unit='USD', country='USA'))
#
#         # Get from CBOE
#         url = "https://www.cboe.com/us/equities/market_statistics/listed_symbols/xml/"
#         src = BeautifulSoup(requests.get(url).text, "lxml")
#         for s in src.find_all("symbol"):
#             data.append(dict(ticker=s['name'], name=s['name'], exchange='CBOE', quoteType='ETF', unit='USD', country='USA'))
#         return pd.DataFrame(data=data).set_index(keys='ticker').drop_duplicates()
#
#     @staticmethod
#     def getKrxIndex() -> pd.DataFrame:
#         """
#         :return:
#                           KOSPI                                KOSDAQ               KRX                      테마
#             지수         지수명   지수                         지수명  지수      지수명  지수              지수명
#         0   1001         코스피   2001                         코스닥  5042     KRX 100  1163    코스피 고배당 50
#         1   1002  코스피 대형주   2002                  코스닥 대형주  5043  KRX 자동차  1164  코스피 배당성장 50
#         ...  ...            ...    ...                            ...   ...        ...    ...                 ...
#         48   NaN            NaN   2217            코스닥 150 헬스케어   NaN        NaN    NaN                 NaN
#         49   NaN            NaN   2218  코스닥 150 커뮤니케이션서비스   NaN        NaN    NaN                 NaN
#         """
#         objs = dict()
#         for market in ('KOSPI', 'KOSDAQ', 'KRX', '테마'):
#             indices = get_index_ticker_list(market=market)
#             names = [get_index_ticker_name(i) for i in indices]
#             objs[market] = pd.DataFrame(data={'지수': indices, '지수명': names})
#         return pd.concat(objs=objs, axis=1)
#
#     @staticmethod
#     def econtains(ticker:str) -> pd.DataFrame:
#         """
#         ECOS ticker specific data contains
#         :param ticker: [str]
#         :return:
#         """
#         api = API_ECOS if API_ECOS else "CEW3KQU603E6GA8VX0O9"
#         columns = dict(
#             ITEM_NAME='이름',
#             ITEM_CODE='코드',
#             CYCLE='주기',
#             START_TIME='시점',
#             END_TIME='종점',
#             DATA_CNT='개수'
#         )
#         url = f"http://ecos.bok.or.kr/api/StatisticItemList/{api}/xml/kr/1/10000/{ticker}"
#         return xml2df(url=url)[columns.keys()].rename(columns=columns)
#
#     def getKrseMarketCapMultipleIpo(self) -> pd.DataFrame:
#         """
#         Fetch KRX Market Cap, Volume, ..., Multiples and IPO
#         :return:
#                  close        marketCap    volume    ...     BPS     PER   PBR      EPS   DIV      DPS         IPO
#         005930   72000  429824343600000  13194571  ...   57822.0    8.94  1.25   8057.0  2.01   1444.0  1975-06-11
#         373220  607000  142038000000000    192569  ...   80052.0  183.61  7.58   3306.0  0.00      0.0  2022-01-27
#         000660  119500   86996282617500   6221769  ...   92004.0   36.86  1.30   3242.0  1.00   1200.0  1996-12-26
#         ...        ...              ...       ...  ...       ...     ...   ...      ...   ...      ...         ...
#         245450    1599       2526356040         1  ...       NaN     NaN   NaN      NaN   NaN      NaN  2016-06-24
#         288490      56       2136232000    264148  ...       NaN     NaN   NaN      NaN   NaN      NaN         NaT
#         000547   12140       1864704000      8664  ...       NaN     NaN   NaN      NaN   NaN      NaN         NaT
#         """
#         if not self._kicm.empty:
#             return self._kicm
#
#         url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
#         kwargs = dict(date=self.tdate, market="ALL", alternative=True)
#         caps_cols = dict(종가='close', 시가총액='marketCap', 거래량='volume')
#         caps = get_market_cap_by_ticker(**kwargs).rename(columns=caps_cols).drop_duplicates()[caps_cols.values()]
#         muls = get_market_fundamental(**kwargs).drop_duplicates()
#         ipo = pd.read_html(io=url, header=0)[0][['종목코드', '상장일']]
#         ipo = ipo.rename(columns=dict(종목코드='ticker', 상장일='IPO')).set_index(keys='ticker')
#         ipo.index = ipo.index.astype(str).str.zfill(6)
#         ipo.IPO = pd.to_datetime(ipo.IPO)
#         ipo = ipo[ipo.IPO <= datetime.strptime(self.tdate, "%Y%m%d")].drop_duplicates()
#         self._kicm = self.join(pd.concat([caps, muls, ipo], axis=1), how='left')
#         return self._kicm
#
#     def save(self):
#         """
#         Save metadata to csv
#         :return:
#         """
#         meta = pd.concat(objs=[
#             self.getKrse(), self.getKrEtf(), self.getNyse(), self.getUsEtf(), self.getEcos(), self.getFred(), self.getOecd()
#         ], axis=0)
#         meta[[
#             'name', 'shortName', 'longName', 'korName', 'exchange', 'sector', 'quoteType', 'unit', 'country',
#             'benchmarkTicker', 'benchmarkName'
#         ]].to_csv(
#             r'./metadata.csv', index=True, encoding='utf-8'
#         )
#         return
#
#
# # Alias
# MetaData = _metadata()
#
#
# if __name__ == "__main__":
#     pd.set_option('display.expand_frame_repr', False)
#
#     API_SYMS = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
#     API_ECOS = "CEW3KQU603E6GA8VX0O9"
#
#     # print(MetaData)
#     # MetaData.getKrse()
#     # print(MetaData.krse)
#     # print(MetaData.ketf)
#     # print(MetaData.nyse)
#     # print(MetaData.uetf)
#     # print(MetaData.oecd)
#     # print(MetaData.ecos)
#     # print(MetaData.fred)
#     # print(MetaData.krse_market_caps_multiples_and_ipo)
#
#     MetaData.save()
