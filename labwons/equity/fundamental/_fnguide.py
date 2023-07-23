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
    url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?" \
          f"pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=D&NewMenuID=Y&stkGb=701"
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
