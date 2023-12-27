from nohji.util.web import web
from nohji.config import api
from stocksymbol import StockSymbol
from pandas import concat, DataFrame, merge, to_datetime
from urllib.request import urlopen
from typing import Any
import json


class _krse:
    """
    KRX(Korea Stock Exchange) Provided Meta data
    * API key required for <StockSymbol>

    @stock:
        type        : DataFrame
        description : listed stock with implicit information
        columns     : ['korName', 'products', 'ipo', 'settlingMonth', 'shortName', 'longName',
                       'quoteType', 'country', 'exchange']
        example     :
                                korName                       products        ipo  settlingMonth ... exchange
            ticker
            000020              동화약품       의약품 제조,판매,수출입 1976-03-24           12월 ...    KOSPI
            000040              KR모터스    이륜차(오토바이) 제조,도매 1976-05-25           12월 ...    KOSPI
            000050                  경방       섬유류 제조,도매,수출입 1956-03-03           12월 ...    KOSPI
            000070            삼양홀딩스       지주회사,경영자문컨설팅 1968-12-27           12월...     KOSPI
            000080            하이트진로                          소주 2009-10-19           12월 ...    KOSPI
            ...                      ...                           ...        ...           ...  ...      ...
            950170                   JTC  식품류, 생활용품류, 화장품류 2018-04-06           02월 ...   KOSDAQ
            950190        고스트스튜디오    캐주얼게임, 소셜카지노게임 2020-08-18           12월 ...   KOSDAQ
            950200                소마젠            유전체 분석 서비스 2020-07-13           12월 ...   KOSDAQ
            950210  프레스티지바이오파마    바이오시밀러 및 항체의약품 2021-02-05           06월 ...    KOSPI
            950220            네오이뮨텍                    면역항암제 2021-03-16           12월 ...   KOSDAQ

    @etf:
        type        : DataFrame
        description : listed etf with implicit information
        columns     : ['korName', 'sector', 'nav', 'marketCap', 'quoteType', 'country',
                       'exchange', 'benchmark', 'benchmarkTicker']
        example     :
                                         korName          sector      nav  marketCap quoteType  ... benchmarkTicker
            ticker
            357870     TIGER CD금리투자KIS(합성)            채권    53576      66786       ETF  ...       KOSPI 200
            459580      KODEX CD금리액티브(합성)            채권  1021740      64783       ETF  ...       KOSPI 200
            069500                     KODEX 200   국내 시장지수    35601      64462       ETF  ...       KOSPI 200
            449170    TIGER KOFR금리액티브(합성)            채권   103860      50183       ETF  ...       KOSPI 200
            423160    KODEX KOFR금리액티브(합성)            채권   105311      46991       ETF  ...       KOSPI 200
            ...                              ...             ...      ...        ...       ...  ...             ...
            426410  ARIRANG 미국대체투자Top10MV        해외 주식    14413         22       ETF  ...       KOSPI 200
            433870         ARIRANG TDF2050액티브            기타    11365         20       ETF  ...       KOSPI 200
            315480  KBSTAR 200커뮤니케이션서비스  국내 업종/테마    11285         14       ETF  ...       KOSPI 200
            287330          KBSTAR 200생활소비재  국내 업종/테마     5991         13       ETF  ...       KOSPI 200
            287320              KBSTAR 200산업재  국내 업종/테마    12408         10       ETF  ...       KOSPI 200

    @data:
        type        : DataFrame
        description : listed stock and etf with implicit information (concatenated by @stock, @etf)
        columns     : ['name', 'korName', 'products', 'ipo', 'settlingMonth', 'shortName', 'longName',
                       'quoteType', 'country', 'exchange', 'sector', 'nav', 'marketCap',
                       'benchmark', 'benchmarkTicker']
        example     : pass
    """
    __data__: DataFrame = DataFrame()

    def __init__(self):
        self.__data__ = DataFrame()
        return

    def __call__(self) -> DataFrame:
        return self.data

    def __str__(self) -> str:
        return str(self.data)

    def __getattr__(self, item:Any):
        if item in dir(self):
            return getattr(self, item)
        if hasattr(self.data, item):
            return getattr(self.data, item)
        raise AttributeError

    def __getitem__(self, item:Any):
        return self.data[item]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    @property
    def stock(self) -> DataFrame:
        columns = {
            "회사명": "korName",
            "종목코드": "ticker",
            "주요제품": "products",
            "상장일": "ipo",
            "결산월": "settlingMonth"
        }
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
        data1 = web.list(url, encoding="euc-kr")[0][columns.keys()].rename(columns=columns)
        data1 = data1.set_index(keys="ticker")
        data1.index = data1.index.astype(str).str.zfill(6)
        data1["ipo"] = to_datetime(data1["ipo"])

        data2 = DataFrame(data=StockSymbol(api.stockSymbol).get_symbol_list(market='kr'))
        data2[['ticker', 'exchange']] = tuple(data2.symbol.str.split('.'))
        data2[['currency', 'country']] = ['KRW', 'KOR']
        data2["exchange"] = data2["exchange"].apply(lambda x: {"KS": "KOSPI", "KQ": "KOSDAQ"}[x])
        data2 = data2.set_index(keys='ticker')[['shortName', 'longName', 'quoteType', 'country', 'exchange']]

        data = merge(data1, data2, how="outer", left_index=True, right_index=True)
        return data[~data.korName.isna()].copy()

    @property
    def etf(self) -> DataFrame:
        columns = {
            "itemcode": "ticker",
            "itemname": "korName",
            "etfTabCode": "sector",
            "nav": "nav",
            "marketSum": "marketCap"
        }
        codes = {1:"국내 시장지수", 2:"국내 업종/테마", 3:"국내 파생",
                 4:"해외 주식", 5:"원자재", 6:"채권", 7:"기타"}
        url = 'https://finance.naver.com/api/sise/etfItemList.nhn'

        data = DataFrame(json.loads(urlopen(url).read().decode('cp949'))['result']['etfItemList'])
        data = data[columns.keys()].rename(columns=columns).set_index(keys="ticker")
        data[
            ["quoteType", "country", "exchange", "currency", "benchmark", "benchmarkTicker"]
        ] = ["ETF", "KOR", "KOSPI", "KRW", "069500", "KOSPI 200"]
        data["name"] = data["korName"]
        data["sector"] = data["sector"].apply(lambda x: codes[x])
        return data

    @property
    def data(self) -> DataFrame:
        if self.__data__.empty:
            self.__data__ = concat([self.stock, self.etf], axis=0)
        return self.__data__

# Alias
krse = _krse()


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    api.stockSymbol = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
    # api_es = "CEW3KQU603E6GA8VX0O9"

    print(krse.stock)
    print(krse.etf)
    print(krse)