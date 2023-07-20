from datetime import datetime, timedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup as Soup
from pykrx import stock
import requests, json
import pandas as pd
import numpy as np


def get_summary_table(ticker:str, **kwargs) -> pd.DataFrame:
    """
    :return:
                            항목 #1                                              항목 #2
    0                종가/ 전일대비                65,900/ +800                   거래량              9,405,365
    1           52주.최고가/ 최저가              68,100/ 52,600           거래대금(억원)                   6200
    2        수익률(1M/ 3M/ 6M/ 1Y)  +1.38/ +4.44/ +6.63/ -0.90          외국인 보유비중                  51.97
    3   시가총액(상장예정포함,억원)                     4392435                베타(1년)                1.06273
    4         시가총액(보통주,억원)                     3934087                   액면가                    100
    5    발행주식수(보통주/ 우선주)  5,969,782,550/ 822,886,700  유동주식수/비율(보통주)  4,525,915,719 / 75.81
    """
    url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=D&NewMenuID=Y&stkGb=701"
    html = kwargs['html'] if 'html' in kwargs.keys() else pd.read_html(url, header=0)
    df = html[0]
    data = [df.columns.tolist()] + [list(r) for r in df.to_numpy() if len([_ for _ in r if str(_) == 'nan']) < 3]
    df = pd.DataFrame(data=data, columns=['항목 #1', '', '항목 #2', ''])
    return df

def get_statement(ticker:str, by:str='annual') -> pd.DataFrame:
    """
    Company Statement
    :return:
                 매출액 영업이익 영업이익(발표기준)  ...   PBR 발행주식수 배당수익률
    IFRS(연결)                                       ...
    2018/12     2437714   588867             588867  ...  1.10    5969783       3.66
    2019/12     2304009   277685             277685  ...  1.49    5969783       2.54
    2020/12     2368070   359939             359939  ...  2.06    5969783       3.70
    2021/12     2796048   516339             516339  ...  1.80    5969783       1.84
    2022/12     3022314   433766             433766  ...  1.09    5969783       2.61
    2023/12(E)  2729496   145857                NaN  ...  1.18        NaN        NaN
    2024/12(E)  3063428   386377                NaN  ...  1.04        NaN        NaN
    2025/12(E)  3404855   575935                NaN  ...  0.98        NaN        NaN
    """
    url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=D&NewMenuID=Y&stkGb=701"
    html = pd.read_html(url, header=0)
    if by == 'annual':
        s = html[14] if html[11].iloc[0].isnull().sum() > html[14].iloc[0].isnull().sum() else html[11]
    elif by == 'quarter':
        s = html[15] if html[11].iloc[0].isnull().sum() > html[14].iloc[0].isnull().sum() else html[12]
    else:
        raise KeyError

    cols = s.columns.tolist()
    s.set_index(keys=[cols[0]], inplace=True)
    s.index.name = None
    if isinstance(s.columns[0], tuple):
        s.columns = s.columns.droplevel()
    else:
        s.columns = s.iloc[0]
        s.drop(index=s.index[0], inplace=True)
    return s.T.astype(float)

def get_products(ticker: str) -> pd.DataFrame:
    """
    Business Model Products
    :return:
                IM 반도체     CE     DP  기타(계)
    기말
    2019/12  46.56  28.19  19.43  13.48     -7.66
    2020/12  42.05  30.77  20.34  12.92     -6.08
    2021/12  39.07  33.68  19.97  11.34     -4.06
    """
    url = f"http://cdn.fnguide.com/SVO2//json/chart/02/chart_A{ticker}_01_N.json"
    src = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'), strict=False)
    header = pd.DataFrame(src['chart_H'])[['ID', 'NAME']].set_index(keys='ID').to_dict()['NAME']
    header.update({'PRODUCT_DATE': '기말'})
    products = pd.DataFrame(src['chart']).rename(columns=header).set_index(keys='기말')
    products = products.drop(columns=[c for c in products.columns if products[c].astype(float).sum() == 0])

    i = products.columns[-1]
    products['Sum'] = products.astype(float).sum(axis=1)
    products = products[(90 <= products.Sum) & (products.Sum < 110)].astype(float)
    products[i] = products[i] - (products.Sum - 100)
    return products.drop(columns=['Sum'])

def get_products_recent(ticker: str = str(), products: pd.DataFrame = None) -> pd.DataFrame:
    if not isinstance(products, pd.DataFrame):
        products = get_products(ticker=ticker)
    i = -1 if products.iloc[-1].astype(float).sum() > 10 else -2
    df = products.iloc[i].T.dropna().astype(float)
    df.drop(index=df[df < 0].index, inplace=True)
    df[df.index[i]] += (100 - df.sum())
    return df[df.values != 0]

def get_expenses(ticker:str) -> pd.DataFrame:
    url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Corp.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=102&stkGb=701"
    html = pd.read_html(url, header=0)

    sales_cost = html[4].set_index(keys=['항목'])
    sales_cost.index.name = None

    sg_n_a = html[5].set_index(keys=['항목'])
    sg_n_a.index.name = None

    r_n_d = html[8].set_index(keys=['회계연도'])
    r_n_d.index.name = None
    r_n_d = r_n_d[['R&D 투자 총액 / 매출액 비중.1', '무형자산 처리 / 매출액 비중.1', '당기비용 처리 / 매출액 비중.1']]
    r_n_d = r_n_d.rename(columns={
        'R&D 투자 총액 / 매출액 비중.1': 'R&D투자비중',
        '무형자산 처리 / 매출액 비중.1': '무형자산처리비중',
        '당기비용 처리 / 매출액 비중.1': '당기비용처리비중'
    })
    if '관련 데이터가 없습니다.' in r_n_d.index:
        r_n_d.drop(index=['관련 데이터가 없습니다.'], inplace=True)
    return pd.concat(objs=[sales_cost.T, sg_n_a.T, r_n_d], axis=1).sort_index(ascending=True).astype(float)

def get_consensus(ticker:str) -> pd.DataFrame:
    url = f"http://cdn.fnguide.com/SVO2/json/chart/01_02/chart_A{ticker}.json"
    raw = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
    frm = pd.DataFrame(raw['CHART'])
    frm = frm.rename(columns={'TRD_DT': '날짜', 'VAL1': '투자의견', 'VAL2': '목표주가', 'VAL3': '종가'})
    frm = frm.set_index(keys='날짜')
    frm.index = pd.to_datetime(frm.index)
    frm['목표주가'] = frm['목표주가'].apply(lambda x: int(x) if x else np.nan)
    frm['종가'] = frm['종가'].astype(int)
    frm['괴리율'] = round(100 * (frm.종가/frm.목표주가 - 1), 2)
    return frm

def get_foreign_rate(ticker:str) -> pd.DataFrame:
    objs = dict()
    for dt in ['3M', '1Y', '3Y']:
        url = f"http://cdn.fnguide.com/SVO2/json/chart/01_01/chart_A{ticker}_{dt}.json"
        data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        frm = pd.DataFrame(data["CHART"])[['TRD_DT', 'J_PRC', 'FRG_RT']]
        frm = frm.rename(columns={'TRD_DT':'date', 'J_PRC':'close', 'FRG_RT':'rate'}).set_index(keys='date')
        frm.index = pd.to_datetime(frm.index)
        frm = frm.replace('', '0.0')
        frm['close'] = frm['close'].astype(int)
        frm['rate'] = frm['rate'].astype(float)
        objs[dt] = frm
    return pd.concat(objs=objs, axis=1)

def get_nps(ticker:str) -> pd.DataFrame:
    url = f"http://cdn.fnguide.com/SVO2/json/chart/05/chart_A{ticker}_D.json"
    src = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
    header = pd.DataFrame(src['01_Y_H'])[['ID', 'NAME']].set_index(keys='ID').to_dict()['NAME']
    header.update({'GS_YM': '날짜'})
    data = pd.DataFrame(src['01_Y']).rename(columns=header)[header.values()].set_index(keys='날짜')
    data = data[data != '-']
    for col in data.columns:
        data[col] = data[col].astype(str).str.replace(',', '').astype(float)

    missing = [col for col in ['EPS', 'BPS', 'EBITDAPS', '보통주DPS'] if not col in data.columns]
    if missing:
        data[missing] = np.nan
    return data

def get_multi_factor(ticker:str) -> pd.DataFrame:
    url = f"http://cdn.fnguide.com/SVO2/json/chart/05_05/A{ticker}.json"
    data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
    header = pd.DataFrame(data['CHART_H'])['NAME'].tolist()
    return pd.DataFrame(data['CHART_D']).rename(
        columns=dict(zip(['NM', 'VAL1', 'VAL2'], ['팩터'] + header))
    ).set_index(keys='팩터').astype(float)

def get_benchmark_return(ticker:str):
    """
    :return:
                                          3M  ...                               3Y
              삼성전자 KOSPI전기,전자  KOSPI  ...  삼성전자 KOSPI전기,전자   KOSPI
    TRD_DT                                    ...
    2020-03-01     NaN           NaN     NaN  ...    100.00         100.00  100.00
    2020-04-01     NaN           NaN     NaN  ...    105.76         106.99  113.56
    2020-05-01     NaN           NaN     NaN  ...    105.88         109.09  120.65
    ...            ...           ...     ...  ...       ...            ...     ...
    2023-03-15  100.50        105.33  101.17  ...       NaN            NaN     NaN
    2023-03-16  100.67        105.87  101.09  ...       NaN            NaN     NaN
    2023-03-17  103.03        106.85  101.85  ...       NaN            NaN     NaN
    """
    objs = dict()
    for period in ['3M', '1Y', '3Y']:
        url = f"http://cdn.fnguide.com/SVO2/json/chart/01_01/chart_A{ticker}_{period}.json"
        data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        header = pd.DataFrame(data["CHART_H"])[['ID', 'PREF_NAME']]
        header = header[header['PREF_NAME'] != ""]
        inner = pd.DataFrame(data["CHART"])[
            ['TRD_DT'] + header['ID'].tolist()
            ].set_index(keys='TRD_DT').rename(columns=header.set_index(keys='ID').to_dict()['PREF_NAME'])
        inner.index = pd.to_datetime(inner.index)
        objs[period] = inner
    df = pd.concat(objs=objs, axis=1).copy()
    for c in df.columns:
        df[c] = df[c].str.replace(',', '').astype(float)
    return df

def get_benchmark_multiple(ticker:str) -> pd.DataFrame:
    url = f"http://cdn.fnguide.com/SVO2/json/chart/01_04/chart_A{ticker}_D.json"
    data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
    objs = dict()
    for label, index in (('PER', '02'), ('EV/EBITDA', '03'), ('ROE', '04')):
        header1 = pd.DataFrame(data[f'{index}_H'])[['ID', 'NAME']].set_index(keys='ID')
        header1['NAME'] = header1['NAME'].astype(str).str.replace("'", "20")
        header1 = header1.to_dict()['NAME']
        header1.update({'CD_NM': '이름'})

        inner1 = pd.DataFrame(data[index])[list(header1.keys())].rename(columns=header1).set_index(keys='이름')
        inner1.index.name = None
        for col in inner1.columns:
            inner1[col] = inner1[col].apply(lambda x: np.nan if x == '-' else x)
        objs[label] = inner1.T
    return pd.concat(objs=objs, axis=1).astype(float)

def get_short_sell(ticker:str) -> pd.DataFrame:
    url = f"http://cdn.fnguide.com/SVO2/json/chart/11_01/chart_A{ticker}_SELL1Y.json"
    data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
    frm = pd.DataFrame(data['CHART'])
    frm = frm.rename(columns={'TRD_DT': '날짜', 'VAL': '차입공매도비중', 'ADJ_PRC': '수정종가'}).set_index(keys='날짜')
    frm.index = pd.to_datetime(frm.index)
    frm['수정종가'] = frm['수정종가'].astype(int)
    frm['차입공매도비중'] = frm['차입공매도비중'].astype(float)
    return frm

def get_short_balance(ticker:str) -> pd.DataFrame:
    url = f"http://cdn.fnguide.com/SVO2/json/chart/11_01/chart_A{ticker}_BALANCE1Y.json"
    data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
    frm = pd.DataFrame(data['CHART'])[['TRD_DT', 'BALANCE_RT', 'ADJ_PRC']]
    frm = frm.rename(columns={'TRD_DT': '날짜', 'BALANCE_RT': '대차잔고비중', 'ADJ_PRC': '수정종가'}).set_index(keys='날짜')
    frm.index = pd.to_datetime(frm.index)
    frm['수정종가'] = frm['수정종가'].astype(int)
    frm['대차잔고비중'] = frm['대차잔고비중'].astype(float)
    return frm