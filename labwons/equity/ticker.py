from labwons.common.metadata.metadata import MetaData
from labwons.common.config import PATH
from labwons.common.service.tools import stringDel
from labwons.common.service.fnguide import fnguide
from bs4 import BeautifulSoup as Soup
import xml.etree.ElementTree as xml
import yfinance as yf
import pandas as pd
import numpy as np
import requests, os


class _ticker(object):
    _valid_prop = {
        "name": None,            # Metadata
        "quoteType": None,       # Metadata
        "country": None,         # Metadata
        "exchange": None,        # Metadata
        "unit": None,            # Metadata
        "shortName": None,       # Metadata
        "longName": None,        # Metadata
        "korName": None,         # Metadata
        "sector": None,          # Metadata
        "industry": None,        # Metadata
        "benchmarkTicker": None, # Metadata
        "benchmarkName": None,   # Metadata

        "previousClose": None,
        "fiftyTwoWeekLow": None,
        "fiftyTwoWeekHigh": None,
        "targetPrice": None,
        "marketCap": None,
        "shares": None,
        "floatShares": None,
        "volume": None,
        "foreignHold": None,
        "dividendYield": None,

        "businessSummary": None,
        "beta": None,
        "trailingPE": None,
        "forwardPE": None,
        "priceToBook": None,
        "pegRatio": None,

        "path": '',
    }

    def __init__(self, ticker:str, **kwargs):
        if ticker not in MetaData.index and 'exchange' not in kwargs:
            """
            Possible @exchange list
            - for KOR: "KOSPI", "KOSDAQ",
            - for USA: "NYSE", "NASDAQ", "OTC", "PCX", "AMEX", "CBOE", "NCM", "NMS", ... ,
            - others : "FRED", "ECOS", "OECD"            
            """
            raise KeyError(
                f'@ticker not found in MetaData, @exchange must be specified for ticker: {ticker}'
            )

        if ticker in MetaData.index:
            kwargs.update(MetaData.loc[ticker].to_dict())

        self.ticker = ticker
        self.__init_prop__()
        for key in self._valid_prop:
            if key in kwargs:
                self._valid_prop[key] = kwargs[key]

        if self._valid_prop['exchange'].upper() in ['FRED', 'OECD', 'ECOS']:
            return

        self._serv = None
        if self._valid_prop['country'].upper() == 'KOR' or self._valid_prop['exchange'].startswith('KO'):
            self._serv = srv = fnguide(ticker)
            for prop in self._valid_prop:
                if hasattr(srv, prop):
                    self._valid_prop[prop] = getattr(srv,prop)
            # self._valid_prop.update({
            #     "previousClose": srv.previousClose,
            #     "fiftyTwoWeekLow": srv.fiftyTwoWeekLow,
            #     "fiftyTwoWeekHigh": srv.fiftyTwoWeekHigh,
            #     "targetPrice": srv.targetPrice,
            #     "marketCap": srv.marketCap,
            #     "shares": srv.shares,
            #     "floatShares": srv.floatShares,
            #     "volume": srv.volume,
            #     "foreignHold": srv.foreignHold,
            #     "dividendYield": None,
            #     "businessSummary": srv.businessSummary,
            #     "beta": srv.beta,
            #     "trailingPE": None,
            #     "forwardPE": None,
            #     "priceToBook": None,
            #     "pegRatio": None,
            #     "path": os.path.join(PATH.BASE, f"{ticker}_{self._valid_prop['name']}")
            # })

        self._valid_prop["path"] = os.path.join(PATH.BASE, f"{ticker}_{self._valid_prop['name']}")
        # if self.country == 'KOR':
        #     self._fnguide = fnguide(ticker)
        #     self.__kr__()
        # elif self.country == 'USA':
        #     self.__us__()
        # else:
        #     pass


        return

    def __init_prop__(self):
        for key in self._valid_prop:
            self._valid_prop[key] = np.nan
        return

    @staticmethod
    def _fnguideEtf(ticker: str):
        """
        FuGuide provided ETF general information
        :return:
        [Example: 091160]

        """
        url = f"http://comp.fnguide.com/SVO2/ASP/" \
            f"etf_snapshot.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=401&stkGb=770"

        key = ''
        dataset = {'price': [], 'comp': [], 'sector': []}
        for line in requests.get(url).text.split('\n'):
            if "etf1PriceData" in line:
                key = 'price'
            if "etf1StyleInfoStkData" in line:
                key = 'comp'
            if "etf1StockInfoData" in line:
                key = 'sector'
            if "]" in line and key:
                key = ''
            if key:
                dataset[key].append(line)
        return (pd.DataFrame(data=eval(f"[{''.join(dataset[k][1:])}]")).set_index(keys='val01')['val02'] for k in dataset)

    @staticmethod
    def _findSimilar(ticker:str) -> pd.DataFrame:
        url = f"https://finance.naver.com/item/main.naver?code={ticker}"
        sim = pd.read_html(io=url, header=0, encoding='euc-kr')[4]
        sim = sim.set_index(keys='종목명')
        sim = sim.drop(index=['전일대비'])
        sim.index.name = None
        for col in sim:
            sim[col] = sim[col].apply(lambda x: stringDel(str(x), ['하향', '상향', '%', '+', ' ']))
        tickers = [c.replace('*', '')[-6:] for c in sim.columns]
        labels = [c.replace('*', '')[:-6] for c in sim.columns]
        sim.columns = tickers
        return pd.concat(objs=[pd.DataFrame(columns=tickers, index=['종목명'], data=[labels]), sim], axis=0).T

    def __kr__(self):
        str2int = lambda x: int(x.replace(', ', '').replace(',', ''))
        nav2num = lambda x, n: float(x.replace(' ', '').replace('배', '').replace('원', '').replace(',', '').split('l')[n])

        # Common Properties
        guide = f"http://cdn.fnguide.com/SVO2/xml/Snapshot_all/{self.ticker}.xml"
        src = xml.fromstring(requests.get(url=guide).text).find('price')
        self._valid_prop.update({

            "previousClose": str2int(src.find('close_val').text),
            "foreignHold": float(src.find('frgn_rate').text),
            "beta": float(src.find('beta').text) if src.find('beta').text else None,
            "volume": str2int(src.find('deal_cnt').text),
            "marketCap": str2int(src.find('mkt_cap_1').text) * 100000000,
            "fiftyTwoWeekLow": str2int(src.find('low52week').text),
            "fiftyTwoWeekHigh": str2int(src.find('high52week').text),
        })

        if not self._is_etf:
            _, _, _, _, comp, _, _, cons, mul, _, _, _, _ = tuple(pd.read_html(
                io=f"https://finance.naver.com/item/main.naver?code={self.ticker}", encoding='euc-kr'
            ))
            self._valid_prop.update({
                'businessSummary': self._fnguide.summary,
                "dividendYield": str(mul.iloc[3, 1]).replace('%', ''),
                "trailingPE": None if mul.iloc[0, 1].startswith('N/A') else nav2num(mul.iloc[0, 1], 0),
                "trailingEps": None if mul.iloc[0, 1].startswith('N/A') else nav2num(mul.iloc[0, 1], 1),
                "forwardPE": None if mul.iloc[1, 1].startswith('N/A') else nav2num(mul.iloc[1, 1], 0),
                "forwardEps": None if mul.iloc[1, 1].startswith('N/A') else nav2num(mul.iloc[1, 1], 1),
                "priceToBook": None if mul.iloc[2, 1].startswith('N/A') else nav2num(mul.iloc[2, 1], 0),
                "bookValue": None if mul.iloc[2, 1].startswith('N/A') else nav2num(mul.iloc[2, 1], 1),
                "targetPrice": None if cons.iloc[0, 1].endswith('N/A') else nav2num(cons.iloc[0, 1], 1),
                "returnOnEquity": comp.iloc[11, 1],  # Most Recent
                "floatShares": str2int(src.find('ff_sher').text),
                "shares": str2int(src.find('listed_stock_1').text),
                "similar": self._findSimilar(self.ticker)
            })
        else:
            price, mul, sec = self._fnguideEtf(self.ticker)
            self._valid_prop.update({
                "trailingPE": mul['PER'],
                "bookValue": mul['PBR'],
                "shares": str2int(price['발행주식수']),
                'sector': sec[sec == max(sec)].index[0] if all(sec.values) else None
            })
        return

    def __us__(self):
        try:
            info = yf.Ticker(self.ticker).info
            # for k, v in info.items():
            #     print(k, ":", v)
        except requests.exceptions.HTTPError:
            return
        matches = dict(
            longBusinessSummary='businessSummary',
            sharesOutstanding='shares',
            trailingAnnualDividendRate='dividendYield',
            targetMeanPrice='targetPrice',
            category='sector'
        )
        for k, v in matches.items():
            if k in info:
                info[v] = info[k]
        info['unit'] = 'USD'
        for key in info:
            if key in self._valid_prop:
                self._valid_prop[key] = info[key]
        return

    @property
    def name(self) -> str:
        return self._valid_prop['name']

    @name.setter
    def name(self, name:str):
        self._valid_prop['name'] = name

    @property
    def unit(self) -> str:
        return self._valid_prop['unit']

    @unit.setter
    def unit(self, unit:str):
        self._valid_prop['unit'] = unit

    @property
    def sector(self) -> str:
        return self._valid_prop['sector']

    @sector.setter
    def sector(self, sector:str):
        self._valid_prop['sector'] = sector

    @property
    def country(self) -> str:
        return self._valid_prop['country']

    @country.setter
    def country(self, country:str):
        self._valid_prop['country'] = country

    @property
    def businessSummary(self) -> str:
        return self._valid_prop['businessSummary']

    @property
    def previousClose(self) -> int or float:
        return self._valid_prop['previousClose']

    @property
    def foreignHold(self) -> int or float:
        return self._valid_prop['foreignHold']

    @property
    def dividendYield(self) -> int or float:
        return self._valid_prop['dividendYield']

    @property
    def benchmarkTicker(self) -> str:
        return self._valid_prop['benchmarkTicker']

    @property
    def benchmarkName(self) -> str:
        return self._valid_prop['benchmarkName']

    @property
    def beta(self) -> int or float:
        return self._valid_prop['beta']

    @property
    def trailingPE(self) -> int or float:
        return self._valid_prop['trailingPE']

    @property
    def trailingEps(self) -> int or float:
        return self._valid_prop['trailingEps']

    @property
    def forwardPE(self) -> int or float:
        return self._valid_prop['forwardPE']

    @property
    def forwardEps(self) -> int or float:
        return self._valid_prop['forwardEps']

    @property
    def volume(self) -> int or float:
        return self._valid_prop['volume']

    @property
    def marketCap(self) -> int or float:
        return self._valid_prop['marketCap']

    @property
    def fiftyTwoWeekLow(self) -> int or float:
        return self._valid_prop['fiftyTwoWeekLow']

    @property
    def fiftyTwoWeekHigh(self) -> int or float:
        return self._valid_prop['fiftyTwoWeekHigh']

    @property
    def floatShares(self) -> int or float:
        return self._valid_prop['floatShares']

    @property
    def shares(self) -> int or float:
        return self._valid_prop['shares']

    @property
    def priceToBook(self) -> int or float:
        return self._valid_prop['priceToBook']

    @property
    def bookValue(self) -> int or float:
        return self._valid_prop['bookValue']

    @property
    def pegRatio(self) -> int or float:
        return self._valid_prop['pegRatio']

    @property
    def exchange(self) -> int or float:
        return self._valid_prop['exchange']

    @property
    def quoteType(self) -> int or float:
        return self._valid_prop['quoteType']

    @property
    def shortName(self) -> int or float:
        return self._valid_prop['shortName']

    @property
    def longName(self) -> int or float:
        return self._valid_prop['longName']

    @property
    def targetPrice(self) -> int or float:
        return self._valid_prop['targetPrice']

    @property
    def returnOnEquity(self) -> int or float:
        return self._valid_prop['returnOnEquity']

    @property
    def floatSharesRate(self):
        if not self.floatShares or not self.shares:
            return None
        return round(100 * self.floatShares / self.shares, 2)

    @property
    def gapFiftyTwoWeekHigh(self) -> float:
        return round(100 * (self.previousClose / self.fiftyTwoWeekHigh - 1), 2)

    @property
    def gapFiftyTwoWeekLow(self) -> float:
        return round(100 * (self.previousClose / self.fiftyTwoWeekLow - 1), 2)

    @property
    def gapTargetPrice(self) -> float or None:
        if not self.targetPrice:
            return None
        return round(100 * (self.previousClose / self.targetPrice - 1), 2)

    @property
    def similar(self) -> pd.DataFrame:
        return self._valid_prop['similar']

    def description(self) -> pd.Series:
        series = pd.Series(data=self._valid_prop)
        series['ticker'] = self.ticker
        if not self.exchange in ['FRED', 'OECD', 'ECOS']:
            series['floatSharesRate'] = self.floatSharesRate
            series['gapFiftyTwoWeekHigh'] = self.gapFiftyTwoWeekHigh
            series['gapFiftyTwoWeekLow'] = self.gapFiftyTwoWeekLow
            series['gapTargetPrice'] = self.gapTargetPrice
        return series


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)

    # print(yf.Ticker('AAPL').info)

    # tester = _ticker('LTPZ', exchange='NYSE')
    # tester = _ticker('QQQ')
    # tester = _ticker('AAPL')
    # tester = _ticker('058470')
    # tester = _ticker('457690')
    # tester = _ticker('383310')
    # tester = _ticker('142210')
    tester = _ticker('VVZZXX')

    # print(tester.description())
    # print(tester.name)
    # print(tester.exchange)
    # print(tester.quote)
    # print(tester.unit)
    # print(tester.businessSummary)
    # print(tester.sector)
    # print(tester.marketCap)
    # print(tester.previousClose)
    # print(tester.fiftyTwoWeekHigh)
    # print(tester.fiftyTwoWeekLow)
    # print(tester.dividendYield)
    # print(tester.beta)
    # print(tester.shares)
    # print(tester.sharesFloat)
    # print(tester.previousClose)
    # print(tester.targetPrice)
    # print(tester.similar)

    # import random
    # samples = random.sample(MetaData.KRSTOCK.index.tolist(), 10)
    # samples = random.sample(MetaData.USSTOCK.index.tolist(), 10)
    # for sample in samples:
    #     print(f'\n{sample}', "=" * 75)
    #     stock = _ticker(sample)
    #     print(stock.description())
    #     print(stock.similar)
