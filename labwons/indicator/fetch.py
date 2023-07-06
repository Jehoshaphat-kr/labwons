from labwons.common.metadata.metadata import MetaData
from labwons.common.tools import xml2df
from pandas_datareader import get_data_fred
from datetime import datetime
from pytz import timezone
import pandas as pd
import requests


def fetchFred(ticker:str, startdate:str, enddate:str) -> pd.Series:
    fetched = get_data_fred(
        symbols=ticker,
        start=startdate,
        end=enddate
    )
    return pd.Series(name=ticker, index=fetched.index, data=fetched[ticker], dtype=float)

def fetchEcos(api:str, ticker:str, startdate:str, *args) -> pd.Series:
    keys = list(args)
    contained = MetaData.ecosContains(ticker)
    key = contained[contained.이름 == keys.pop(0)]
    if len(key) > 1:
        cnt = key['개수'].astype(int).max()
        key = key[key.개수 == str(cnt)]
    name, code, c, s, e, _ = tuple(key.values[0])
    code += ('/' + '/'.join([contained[(contained.이름 == l) & (contained.주기 == c)].iat[0, 1] for l in keys]))
    url = f'http://ecos.bok.or.kr/api/StatisticSearch/{api}/xml/kr/1/100000/{ticker}/{c}/{s}/{e}/{code}'
    fetch = xml2df(url=url)
    series = pd.Series(
        name=name, dtype=float,
        index=pd.to_datetime(fetch.TIME + ('01' if c == 'M' else '1231' if c == 'Y' else '')),
        data=fetch.DATA_VALUE.tolist()
    )
    if c == 'M':
        series.index = series.index.to_period('M').to_timestamp('M')
    return series[series.index >= datetime.strptime(startdate, "%Y%m%d")]

def fetchOecd(ticker:str, startdate:str, enddate:str, country:str) -> pd.Series:
    """
    :param ticker    : OECD provided data symbol
    :param startdate : [str] %Y-%m
    :param enddate   : [str] %Y-%m
    :param country   : [str] DEU@Germany, FRA@France, JPN@Japan, KOR@Korea, USA@United States, G7M@G7, G-20@G20 ...
    :return:
    1990-01-31     99.80950
    1990-02-28     99.74467
    1990-03-31     99.69218
                        ...
    2022-12-31     99.81123
    2023-01-31     99.72019
    2023-02-28     99.64526
    Freq: M, Name: LORSGPNO, Length: 398, dtype: float64
    """
    curr = datetime.strptime(enddate, "%Y%m%d").strftime("%Y-%m")
    prev = datetime.strptime(startdate, "%Y%m%d").strftime("%Y-%m")
    url = f"https://stats.oecd.org/SDMX-JSON/data/MEI_CLI/{ticker}.{country}.M/all?startTime={prev}&endTime={curr}"
    load = requests.get(url).json()

    times = [d['id'] for d in load['structure']['dimensions']['observation'][0]['values']]
    value = [v[0] for v in load['dataSets'][0]['series']['0:0:0']['observations'].values()]
    series = pd.Series(data=value, index=times, name=ticker, dtype=float)
    series.index = pd.to_datetime(series.index).to_period('M').to_timestamp('M')
    return series