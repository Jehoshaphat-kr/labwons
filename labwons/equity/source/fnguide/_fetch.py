from labwons.common.web import web
from labwons.common.tools import cutString
from typing import Union
from datetime import datetime, timedelta
from pykrx.stock import get_market_cap_by_date
from pykrx.stock import get_etf_portfolio_deposit_file
import pandas
import numpy as np


def str2num(src:str) -> int or float:
    src = "".join([char for char in src if char.isdigit() or char == "."])
    if not src:
        return np.nan
    if "." in src:
        return float(src)
    return int(src)

def fetchMarketCap(ticker:str) -> pandas.Series:
    """
    * EQUITY ONLY
    :param ticker: [str]
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
    cap['시가총액'] = (cap['시가총액'] / 100000000).astype(int)
    return cap['시가총액']

def fetchSnapShot(url:str) -> pandas.Series:
    """
    * COMMON for EQUITY, ETF
    :param url: [str]
    :return:
        date                 2023/11/17
        previousClose             12510
        fiftyTwoWeekHigh          13480
        fiftyTwoWeekLow           10950
        marketCap                 94069
        sharesOutstanding     751949461
        floatShares           663064556
        volume                   868029
        foreignRate                37.2
        beta                    0.74993
        return1M                    0.0
        return3M                  10.12
        return6M                   6.83
        return1Y                   5.13
        return3Y                  26.36
        dtype: object
    """
    src = web.html(url).find('price')
    return pandas.Series({
        "date": src.find("date").text,
        "previousClose": str2num(src.find("close_val").text),
        "fiftyTwoWeekHigh": str2num(src.find("high52week").text),
        "fiftyTwoWeekLow": str2num(src.find("low52week").text),
        "marketCap": str2num(src.find("mkt_cap_1").text),
        "sharesOutstanding": str2num(src.find("listed_stock_1").text),
        "floatShares": str2num(src.find("ff_sher").text),
        "volume": str2num(src.find("deal_cnt").text),
        "foreignRate": str2num(src.find("frgn_rate").text),
        "beta": str2num(src.find("beta").text),
        "return1M": str2num(src.find("change_1month").text),
        "return3M": str2num(src.find("change_3month").text),
        "return6M": str2num(src.find("change_6month").text),
        "return1Y": str2num(src.find("change_12month").text),
        "return3Y": str2num(src.find("change_36month").text),
    })

def fetchHeader(url:str) -> pandas.Series:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
        fiscalPE         2.90
        forwardPE        3.06
        sectorPE         6.17
        priceToBook      0.32
        dividendYield    9.03
        dtype: float64
    """
    src = web.html(url).find('div', id='corp_group2')
    src = [val for val in src.text.split('\n') if val]
    return pandas.Series({
        "fiscalPE": str2num(src[src.index('PER') + 1]),
        "forwardPE": str2num(src[src.index('12M PER') + 1]),
        "sectorPE": str2num(src[src.index('업종 PER') + 1]),
        "priceToBook": str2num(src[src.index('PBR') + 1]),
        "dividendYield": str2num(src[src.index('배당수익률') + 1]),
    })

def fetchBusinessSummary(url:str) -> str:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
        동사는 2019년 1월 설립한 지주회사로 주요 종속회사들의 사업은 은행업, 신용카드업, 종합금융업 등임.
        ...
        비금융 포트폴리오를 확대하기 위해 중형급 이상 증권사를 인수하는 방안도 지속 고려하고 있음.
    """
    html = web.html(url).find('ul', id='bizSummaryContent').find_all('li')
    t = '\n\n '.join([e.text for e in html])
    w = [
        '.\n' if t[n] == '.' and not any([t[n - 1].isdigit(), t[n + 1].isdigit(), t[n + 1].isalpha()]) else t[n]
        for n in range(1, len(t) - 2)
    ]
    s = ' ' + t[0] + ''.join(w) + t[-2] + t[-1]
    return s.replace(' ', '').replace('\xa0\xa0', ' ').replace('\xa0', ' ').replace('\n ', '\n')

def fetchAbstract(url:str, gb:str='D', period:str='Y') -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url    : [str]
    :param gb     : [str] 연결 = 'D', 별도 = 'B'
    :param period : [str] 연간 = 'Y', 분기 = 'Q'
    :return:
                  이자수익 영업이익 당기순이익 ...   PER   PBR 발행주식수 배당수익률
        기말
        2018/12        NaN     NaN        NaN  ...   NaN   NaN       NaN        NaN
        2019/12     105768   28000      20376  ...  4.29  0.39    722268       6.03
        2020/12      95239   20804      15152  ...  5.38  0.30    722268       3.70
        2021/12      98947   36597      28074  ...  3.56  0.36    728061       7.09
        2022/12     146545   44305      33240  ...  2.68  0.29    728061       9.78
        2023/12(E)  198704   40045      30132  ...  3.25  0.30       NaN        NaN

    :columns: ['이자수익', '영업이익', '영업이익(발표기준)', '당기순이익',
               '지배주주순이익', '비지배주주순이익',
               '자산총계', '부채총계', '자본총계', '지배주주지분', '비지배주주지분',
               '자본금', '부채비율', '유보율', '영업이익률',
               '지배주주순이익률', 'ROA', 'ROE', 'EPS(원)', 'BPS(원)', 'DPS(원)', 'PER', 'PBR',
               '발행주식수', '배당수익률']
    """
    index = {'DY':11, 'BY':14, 'DQ':12, 'BQ':15}[f"{gb}{period}"]
    table = web.list(url)[index]
    data = table.set_index(keys=[table.columns[0]])
    if isinstance(data.columns[0], tuple):
        data.columns = data.columns.droplevel()
    else:
        data.columns = data.iloc[0]
        data = data.drop(index=data.index[0])
    data = data.T
    data = data.head(len(data) - len([i for i in data.index if i.endswith(')')]) + 1)
    data.index.name = '기말'
    data.columns.name = None
    return data

def fetchForeignRate(url:Union[str, list, tuple]) -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
                                3M              1Y              3Y
                       종가   비중     종가   비중     종가   비중
        날짜
        2020-11-01      NaN    NaN      NaN    NaN  10105.0  25.67
        2020-12-01      NaN    NaN      NaN    NaN  10033.0  25.21
        2021-01-01      NaN    NaN      NaN    NaN   9629.0  25.05
        ...             ...    ...      ...    ...      ...    ...
        2023-11-20  12490.0  37.18      NaN    NaN      NaN    NaN
        2023-11-21  12720.0  37.34      NaN    NaN      NaN    NaN
        2023-11-22  12700.0  37.36  12604.0  37.25      NaN    NaN
    """
    cols = {'TRD_DT': '날짜', 'J_PRC': '종가', 'FRG_RT': '비중'}
    objs = {}
    for u in [url] if isinstance(url, str) else url:
        data = web.json2data(u)[cols.keys()]
        data = data.rename(columns=cols).set_index(keys='날짜')
        data.index = pandas.to_datetime(data.index)
        objs[u[u.rfind('_') + 1: u.rfind('.')]] = data.replace('', '0.0').replace('-', '0.0')
    return pandas.concat(objs=objs, axis=1).astype(float)

def fetchConsensus(url:str) -> pandas.Series:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
        투자의견         4.0
        목표주가     15411.0
        EPS           3908.0
        PER              3.3
        추정기관수      18.0
        dtype: float64
    """
    src = web.list(url)[7]
    return pandas.Series(dict(zip(src.columns.tolist(), src.iloc[0].tolist())))

def fetchConsensusPrice(url:str) -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
                   투자의견  컨센서스     종가   격차
        날짜
        2022-11-23      4.0   16378.0  12300.0 -24.90
        2022-11-24      4.0   16378.0  12550.0 -23.37
        2022-11-25      4.0   16378.0  12450.0 -23.98
        ...             ...       ...      ...    ...
        2023-11-20      4.0   15411.0  12490.0 -18.95
        2023-11-21      4.0   15411.0  12720.0 -17.46
        2023-11-22      4.0   15411.0  12700.0 -17.59
    """
    data = web.json2data(url)
    data = data.rename(columns={'TRD_DT': '날짜', 'VAL1': '투자의견', 'VAL2': '컨센서스', 'VAL3': '종가'})
    data = data.set_index(keys='날짜')
    data.index = pandas.to_datetime(data.index)
    data = data.astype(float)
    data['격차'] = round(100 * (data['종가'] / data['컨센서스'] - 1), 2)
    return data

def fetchBenchmarkMultiples(url:str) -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
                                              PER  ...                           배당수익률
              우리금융지주  코스피 금융업  코스피  ...  우리금융지주  코스피 금융업  코스피
        2021          3.56           5.94   11.08  ...          7.09           3.48    1.78
        2022          2.68           5.53   10.87  ...          9.78           4.32    2.22
        2023E         3.25           6.08   17.54  ...           NaN            NaN     NaN

    :columns: MultiIndex([(       'PER',  '우리금융지주'),
                          (       'PER', '코스피 금융업'),
                          (       'PER',     '코스피'),
                          ( 'EV/EBITDA',  '우리금융지주'),
                          ( 'EV/EBITDA', '코스피 금융업'),
                          ( 'EV/EBITDA',     '코스피'),
                          (       'ROE',  '우리금융지주'),
                          (       'ROE', '코스피 금융업'),
                          (       'ROE',     '코스피'),
                          ('배당수익률',  '우리금융지주'),
                          ('배당수익률', '코스피 금융업'),
                          ('배당수익률',     '코스피')
                        ])
    """
    json = web.json(url)
    def mul(key:str) -> pandas.DataFrame:
        head = pandas.DataFrame(json[f'{key}_H'])[['ID', 'NAME']].set_index(keys='ID')
        head['NAME'] = head['NAME'].str.replace("'", "20")
        head = head.to_dict()['NAME']
        head.update({'CD_NM': '이름'})

        data = pandas.DataFrame(json[key])[head.keys()].rename(columns=head).set_index(keys='이름')
        data.index.name = None
        return data.replace('-', np.nan).T.astype(float)
    return pandas.concat(
        objs={'PER': mul('02'), 'EV/EBITDA': mul('03'), 'ROE': mul('04'), '배당수익률': mul('05')},
        axis=1
    )

def fetchMultipleBand(url:str) -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
                                            PER  ...                           PBR
                       종가     2.46X     3.42X  ...     0.38X     0.46X     0.54X
        날짜                                     ...
        2018-12-01      NaN       NaN       NaN  ...       NaN       NaN       NaN
        2019-01-01      NaN       NaN       NaN  ...       NaN       NaN       NaN
        2019-02-01  14800.0       NaN       NaN  ...       NaN       NaN       NaN
        ...             ...       ...       ...  ...       ...       ...       ...
        2025-10-01      NaN  10455.54  14535.75  ...  17745.94  21650.05  25554.16
        2025-11-01      NaN  10488.84  14582.04  ...  17844.72  21770.56  25696.39
        2025-12-01      NaN  10522.13  14628.33  ...  17943.50  21891.06  25838.63
    """
    json = web.json(url)
    def band(key:str) -> pandas.DataFrame:
        head = pandas.DataFrame(json[key])[['ID', 'NAME']].set_index(keys='ID')
        head = head.to_dict()['NAME']
        head.update({'GS_YM': '날짜', 'PRICE': '종가'})
        data = pandas.DataFrame(json['CHART'])
        data = data[head.keys()].replace('-', np.nan).replace('', np.nan)
        data['GS_YM'] = pandas.to_datetime(data['GS_YM'])
        return data.rename(columns=head).set_index(keys='날짜').astype(float)
    return pandas.concat(objs={'PER': band('CHART_E'), 'PBR': band('CHART_B')}, axis=1)

def fetchShortSell(url:str) -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
                    공매도비중     종가
        날짜
        2022-11-28        1.37  12150.0
        2022-12-05        5.70  12800.0
        2022-12-12        1.75  12850.0
        ...                ...      ...
        2023-11-06        8.32  12570.0
        2023-11-13        0.09  12400.0
        2023-11-20        0.13  12490.0
    """
    cols = {'TRD_DT': '날짜', 'VAL': '공매도비중', 'ADJ_PRC': '종가'}
    data = web.json2data(url).rename(columns=cols).set_index(keys='날짜')
    data.index = pandas.to_datetime(data.index)
    return data.astype(float)

def fetchShortBalance(url:str) -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
                   대차잔고비중   종가
        날짜
        2022-10-17        3.50  139900
        2022-10-24        3.50  140000
        2022-10-31        3.44  136800
        ...                ...     ...
        2023-10-02        9.45  153800
        2023-10-09        9.52  154700
        2023-10-16        8.69  156800
    """
    cols = {'TRD_DT': '날짜', 'BALANCE_RT': '대차잔고비중', 'ADJ_PRC': '종가'}
    data = web.json2data(url).rename(columns=cols)[cols.values()].set_index(keys='날짜')
    data.index = pandas.to_datetime(data.index)
    return data.astype(float)

def fetchProducts(url:str) -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
                유가증권평가및처분이익  이자수익  수수료수익  외환거래이익  기타(계)
        기말
        2019/12                  41.49     46.58        7.53          2.65      1.75
        2020/12                  56.93     33.26        5.92          2.65      1.24
        2021/12                  50.70     36.39        7.19          2.07      3.65
        2022/12                  54.21     34.58        5.27          3.31      2.63
    """
    json = web.json(url)
    head = pandas.DataFrame(json['chart_H'])[['ID', 'NAME']].set_index(keys='ID').to_dict()['NAME']
    head.update({'PRODUCT_DATE': '기말'})
    data = pandas.DataFrame(json['chart']).rename(columns=head).set_index(keys='기말')
    data = data.drop(columns=[c for c in data.columns if data[c].astype(float).sum() == 0])

    i = data.columns[-1]
    data['Sum'] = data.astype(float).sum(axis=1)
    data = data[(90 <= data.Sum) & (data.Sum < 110)].astype(float)
    data[i] = data[i] - (data.Sum - 100)
    return data.drop(columns=['Sum'])

def fetchExpenses(url:str, period:str='Y') -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url    : [str]
    :param period : [str] 연간 = 'Y', 분기 = 'Q'
    :return:
                 판관비율  매출원가율
        기말
        2019/12     16.58       20.62
        2020/12     13.81       12.31
        2021/12     15.25       10.70
        2022/12     10.69       14.06
    """
    json = web.json(url)
    def exp(key:str) -> pandas.Series:
        data = pandas.DataFrame(json[f"{key}_{period}"]).set_index(keys="GS_YM")["VAL1"]
        data.index.name = '기말'
        return data.replace('-', np.nan).replace('', np.nan)
    return pandas.concat(objs={"판관비율": exp('05'), "매출원가율": exp('06')}, axis=1)

def fetchMarketShares(url:str, gb:str='D', by:str='product') -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url : [str]
    :param gb  : [str] 연길 = 'D', 별도 = 'B'
    :param by  : [str] "product" / "market"
    :return:
                IC TEST SOCKET 류   LEENO PIN 류          상품     상품 등  의료기기 부품류          합계
                    내수     수출    내수   수출    내수  수출  내수  수출       내수  수출   내수   수출
        2020/12      NaN      NaN    NaN    NaN     NaN   NaN    NaN   NaN       NaN    NaN    NaN    NaN
        2021/12      NaN      NaN    NaN    NaN     NaN   NaN    NaN   NaN       NaN    NaN    NaN    NaN
        2022/12    10.50    89.50  27.80  72.20  100.00  0.00  95.80  4.20     99.30   0.70  24.30  75.70
    """
    src = web.list(url)[{'D':10, 'B':11}[gb]]
    data = src[src.columns[1:]].set_index(keys=src.columns[1])
    data = data.T.copy()
    data.columns = [col.replace("\xa0", " ") for col in data.columns]

    domestic = data[data[data.columns[0]] == "내수"].drop(columns=data.columns[0])
    exported = data[data[data.columns[0]] == "수출"].drop(columns=data.columns[0])
    domestic.index = exported.index = [i.replace('.1', '') for i in domestic.index]
    domestic.columns.name = exported.columns.name = None
    data = pandas.concat(objs={"내수": domestic, "수출": exported}, axis=1)
    if by == 'market':
        return data # 내수/수출 구분 우선 시
    data = pandas.concat(objs={(c[1], c[0]): data[c] for c in data}, axis=1)
    return data[sorted(data.columns, key=lambda x: x[0])] # 상품 구분 우선 시

def fetchSharesHolders(url:str) -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
                    최대주주등  10%이상주주  5%이상주주  임원  자기주식  우리사주조합
        2021/01/01       56.03          NaN        6.26   NaN       NaN           NaN
        2022/01/01       54.95          NaN        6.25   NaN       NaN           NaN
        2023/01/01       54.79          NaN        6.25   NaN       NaN           NaN
        2023/11/14       54.79          NaN        6.25   NaN       NaN           NaN
    """
    data = web.list(url)[12]
    data = data.set_index(keys=[data.columns[0]])
    data.index.name = None
    data.index = [col[:col.index("(") - 1] if "(" in col else col for col in data.index]
    data.index = [i.replace(" ", "").replace("&nbsp;", "") for i in data.index]
    return data.T

def fetchIncomeStatement(url:str, period:str='Y') -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url   : [str]
    :param period: [str] 연간 = 'Y', 분기 = 'Q'
    :return:
                 매출액 매출원가 매출총이익 판매비와관리비 영업이익 금융수익 금융원가 기타수익 기타비용 ... 당기순이익
        2020/12  319004   210898     108106          57980    50126    33279    19804      848     1716 ...      47589
        2021/12  429978   240456     189522   		 65419   124103    23775    14699     1161     1804 ...      96162
        2022/12  446216   289937     156279  		 88184    68094    37143    50916     2414    18019 ...      22417
        2023/2Q  123940   152172     -28231  		 34613   -62844    15203    25144      261      739 ...     -55734

    columns: ['매출액', '매출원가', '매출총이익', '판매비와관리비', '영업이익', '영업이익발표기준',
              '금융수익', '금융원가', '기타수익', '기타비용', '종속기업,공동지배기업및관계기업관련손익',
              '세전계속사업이익', '법인세비용', '계속영업이익', '중단영업이익', '당기순이익',
              '지배주주순이익', '비지배주주순이익']
    """
    cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*']
    data = web.list(url)[{"Y":0, "Q":1}[period]]
    data = data.set_index(keys=[data.columns[0]])
    data = data.drop(columns=[col for col in data if not col.startswith('20')])
    data.index.name = None
    data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
    data.index = [cutString(x, cutter) for x in data.index]
    return data.T.astype(float)

def fetchFinancialStatement(url:str, period:str='Y') -> pandas.DataFrame:
    """
    * EQUITY ONLY
    :param url   : [str]
    :param period: [str] 연간 = 'Y', 분기 = 'Q'
    :return:
        [연결]
                 자산  유동자산  비유동자산  기타금융업자산  부채  유동부채  비유동부채  ...  이익잉여금결손금
        2020/12  3615      2577        1038             NaN   242       219          23  ...              3265
        2021/12  4664      3357        1306             NaN   487       460          27  ...              4068
        2022/12  5315      3770        1545             NaN   383       364          19  ...              4823
        2023/3Q  5773      4194        1579             NaN   460       438          22  ...              5205

    :columns: ['자산', '유동자산', '비유동자산', '기타금융업자산', '부채', '유동부채', '비유동부채', '기타금융업부채',
               '자본', '자본금', '신종자본증권', '자본잉여금', '기타자본', '기타포괄손익누계액', '이익잉여금결손금']

    :return:
        [별도]
                 유동자산  현금및단기예금  유가증권  매출채권  재고자산  임대주택자산  비유동자산  ...  투하자본
        2020/12      2577            2066       NaN       291       123           NaN        1038  ...      1235
        2021/12      3357    	     2830       NaN       354       116           NaN        1306  ...      1340
        2022/12      3770            3171       NaN       393       131           NaN        1545  ...      1740
        2023/3Q      4194            3545       NaN       433       143           NaN        1579  ...      1719

    :columns: ['유동자산', '현금및단기예금', '유가증권', '매출채권', '재고자산', '임대주택자산', '비유동자산',
               '투자자산', '유형자산', '감가상각자산', '무형자산', '자산총계', '유동부채', '매입채무',
               '단기차입금', '유동성장기부채', '비유동부채', '사채', '장기차입금', '이연부채', '부채총계',
               '자본금', '자본잉여금', '자본조정', '자기주식', '기타포괄손익누계액', '이익잉여금', '자본총계',
               '순운전자본', '순차입금', '투하자본']

    """
    cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
    data = web.list(url)[{"Y": 2, "Q": 3}[period]]
    data = data.set_index(keys=[data.columns[0]])
    data = data.drop(columns=[col for col in data if not col.startswith('20')])
    data.index.name = None
    data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
    data.index = [cutString(x, cutter) for x in data.index]
    return data.T.astype(float)

def fetchCashFlow(url:str, period:str="Y") -> pandas.DataFrame:
    """
    * EQUITY ONLU
    :param url   : [str]
    :param period: [str] 연간 = 'Y', 분기 = 'Q'
    :return:
    """
    cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
    cols = {
        "영업활동으로인한현금흐름": "영업현금흐름",
        "투자활동으로인한현금흐름": "투자현금흐름",
        "재무활동으로인한현금흐름": "재무현금흐름",
        "환율변동효과": "환율변동손익",
        "기말현금및현금성자산": "현금및현금성자산"
    }
    data = web.list(url)[{"Y": 4, "Q": 5}[period]]
    data = data.set_index(keys=[data.columns[0]])
    data = data.drop(columns=[col for col in data if not col.startswith('20')])
    data.index.name = None
    data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
    data.index = [cutString(x, cutter) for x in data.index]
    data = data.T
    # data = data.T.astype(int)

    return data[cols.keys()].rename(columns=cols).fillna(0).astype(int)
























def fetchEtfMultiples(url:str) -> pandas.Series:
    """
    * ETF ONLY
    :param url: [str]
    :return:
        dividendYield     1.68
        fiscalPE         12.58
        priceToBook       1.15
        dtype: float64
    """
    script = web.html(url).find_all('script')[-1].text.split('\n')
    pe = script[[n for n, h in enumerate(script) if "PER" in h][0] + 1]
    pb = script[[n for n, h in enumerate(script) if "PBR" in h][0] + 1]
    return pandas.Series({
        "dividendYield": str2num(web.html(url).find_all('td', class_='r cle')[-1].text),
        "fiscalPE" : str2num(pe[pe.index(":"): ]),
        "priceToBook": str2num(pb[pb.index(":"):])
    })

def fetchEtfComponent(ticker:str, meta:pandas.DataFrame=pandas.DataFrame()) -> pandas.DataFrame:
    """
    * ETF ONLY
    :param ticker: [str]
    :param meta  : [pandas.DataFrame]
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
    if meta.empty:
        from labwons.common.metadata.metadata import MetaData as meta
    data['이름'] = meta[meta.index.isin(data.index)]['korName']
    return data[['이름', '비중']]

def fetchEtfSectors(url:str, ticker:str, meta:pandas.DataFrame=pandas.DataFrame()) -> pandas.DataFrame:
    """
    * ETF ONLY
    :param url    : [str]
    :param ticker : [str]
    :param meta   : [pandas.DataFrame]
    :return:
                    KODEX 삼성그룹  유사펀드   시장
    섹터
    에너지                                2.44
    소재                                 10.09
    산업재              17.44      7.48   9.92
    경기소비재           2.67     11.58  10.57
    필수소비재                            2.85
    의료                10.37      5.64   7.46
    금융                12.47      6.49   7.74
    IT                  57.05     52.54  47.36
    통신서비스                            1.01
    유틸리티                              0.57
    미분류
    """
    n, base = 100, ""
    src = str(web.html(url)).split('\r\n')
    while n < len(src):
        if 'etf1StockInfoData' in src[n]:
            while not "];" in src[n + 1]:
                base += src[n + 1]
                n += 1
            break
        n += 1
    data = pandas.DataFrame(data=eval(base)).drop(columns=['val05'])
    if meta.empty:
        from labwons.common.metadata.metadata import MetaData as meta
    data.columns = np.array(["섹터", meta.loc[ticker, 'name'], "유사펀드", "시장"])
    return data.set_index(keys='섹터')






if __name__ == "__main__":
    from labwons.equity.source.fnguide._url import url

    pandas.set_option('display.expand_frame_repr', False)
    # ticker = '316140' # 우리금융지주
    # ticker = '051910' # LG 화학
    ticker = '058470'  # 리노공업
    # ticker = '102780' # KODEX

    url = url(ticker)
    # print(fetchMarketCap(ticker))
    # print(fetchSnapShot(url.xml))
    # print(fetchBusinessSummary(url.snapshot))
    # print(fetchHeader(url.snapshot))
    # print(fetchAbstract(url.snapshot))
    # print(fetchForeignRate(url.foreignRates))
    # print(fetchConsensus(url.snapshot))
    # print(fetchConsensusPrice(url.consensusPrice))
    # print(fetchBenchmarkMultiples(url.benchmarkMultiples))
    # print(fetchShortSell(url.shortSell))
    # print(fetchShortBalance(url.shortBalance))
    # print(fetchMultipleBand(url.multipleBands))
    # print(fetchProducts(url.products))
    # print(fetchExpenses(url.expenses))
    # print(fetchMarketShares(url.corp, url.gb, 'product'))
    # print(fetchSharesHolders(url.corp))
    # print(fetchIncomeStatement(url.finance))
    # print(fetchFinancialStatement(url.finance))
    # print(fetchFinancialStatement(url.separateFinance))
    print(fetchCashFlow(url.finance))

    # print(fetchEtfMultiples(url.etf))
    # print(fetchEtfComponent(ticker))
    # print(fetchEtfSectors(url.etf, ticker))