from labwons.common.config import PATH
from nohji.deprecated.labwons.common.tools import xml2df
from labwons.common.basis import baseSeriesChart
from pandas_datareader import get_data_fred
from datetime import datetime, timedelta
import pandas as pd
import requests


# class _fetch(pd.Series):
class Indicator(baseSeriesChart):
    def __init__(
        self,
        ticker: str,
        *args,
        name: str='',
        source: str='',
        country: str='',
        period: int=20,
        enddate: str='',
        dformat: str='.2f',
        unit: str='',
    ):
        if not ticker in MetaData.index and not source:
            raise KeyError(f'@ticker: "{ticker}" NOT FOUND in metadata, @source must be specified')

        source = source if source else MetaData.loc[ticker, 'exchange']
        if source.lower() == 'oecd' and not country:
            raise KeyError(f"OECD data requires @country symbol: ex) KOR, USA, G-20...")
        if source.lower() == 'ecos' and not args:
            raise KeyError(f"ECOS data requires specific parameters")

        enddate = enddate if enddate else datetime.today().strftime("%Y%m%d")
        startdate = (datetime.strptime(enddate, "%Y%m%d") - timedelta(20 * 365)).strftime("%Y%m%d")
        name = name if name else args[-1] if args else ticker
        if not unit and ticker in MetaData.index:
            unit = MetaData.loc[ticker, 'unit']
            if pd.isna(unit):
                unit = ''

        if source.lower() == 'ecos':
            series = self.fetchEcos(MetaData.API_ECOS, ticker, startdate, *args)
        elif source.lower() == 'oecd':
            series = self.fetchOecd(ticker, startdate, enddate, country)
        elif source.lower() == 'fred':
            series = self.fetchFred(ticker, startdate, enddate)
        else:
            raise KeyError(f'Invalid @source: "{source}", possible source is ["fred", "ecos", "oecd"]')
        M = series.resample('M').ffill()
        super().__init__(series, name=name, dtype=dformat, unit=unit, path=PATH())

        self.ticker = ticker
        self.name = name
        self.startdate = startdate
        self.enddate = enddate
        self.period = period
        self.source = source
        self.dformat = dformat
        self.unit = unit
        self.M = baseSeriesChart(M, name=f'{ticker}(M)', dtype=dformat, unit=unit, path=PATH())
        self.MoM = baseSeriesChart(100 * M.pct_change(), name=f'{ticker}(MoM)', dtype='.2f', unit='%', path=PATH())
        self.YoY = baseSeriesChart(100 * M.pct_change(12), name=f'{ticker}(YoY)', dtype='.2f', unit='%', path=PATH())
        return

    @staticmethod
    def fetchFred(ticker: str, startdate: str, enddate: str) -> pd.Series:
        fetched = get_data_fred(
            symbols=ticker,
            start=startdate,
            end=enddate
        )
        return pd.Series(name=ticker, index=fetched.index, data=fetched[ticker], dtype=float)

    @staticmethod
    def fetchEcos(api: str, ticker: str, startdate: str, *args) -> pd.Series:
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

    @staticmethod
    def fetchOecd(ticker: str, startdate: str, enddate: str, country: str) -> pd.Series:
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
