from labwons.common.metadata.metadata import MetaData
from labwons.common.config import PATH
from bs4 import BeautifulSoup as Soup
import xml.etree.ElementTree as xml
import yfinance as yf
import pandas as pd
import numpy as np
import requests, os


class _ticker(object):
    _valid_args = [
        'KOSPI', 'KOSDAQ',
        'NYSE', 'NASDAQ', 'OTC', 'PCX', 'AMEX', 'CBOE', 'NCM', 'NMS'
        'FRED', 'ECOS', 'OECD'
    ]

    def __init__(self, ticker:str, **kwargs):
        if not ticker:
            return
        self._valid_prop = {
            'name': np.nan,
            'ticker': ticker,
            'unit': np.nan,
            'path': '',
            'sector': np.nan,
            'market': np.nan,
            "businessSummary": np.nan,
            "previousClose": np.nan,
            "foreignRate": np.nan,
            "dividendYield": np.nan,
            # "benchmarkTicker": np.nan,
            # "benchmarkName": np.nan,
            "beta": np.nan,
            "trailingPE": np.nan,
            "trailingEps": np.nan,
            "forwardPE": np.nan,
            "forwardEps": np.nan,
            "volume": np.nan,
            "marketCap": np.nan,
            "fiftyTwoWeekLow": np.nan,
            "fiftyTwoWeekHigh": np.nan,
            "floatShares": np.nan,
            "shares": np.nan,
            "priceToBook": np.nan,
            "bookValue": np.nan,
            "pegRatio": np.nan,
            "exchange": np.nan,
            "quoteType": np.nan,
            "shortName": np.nan,
            "longName": np.nan,
            "korName": np.nan,
            "targetPrice": np.nan,
            "returnOnEquity": np.nan,
        }

        if not ticker in MetaData.index:
            if 'exchange' not in kwargs:
                raise KeyError(f"_ticker Not Found Error: @exchange must be specified for ticker, {ticker}")
            if not kwargs['exchange'].lower() in [v.lower for v in self._valid_args]:
                raise KeyError(f"Invalid @exchange! Valid arguments: {self._valid_args}")
            kwargs.update(dict(name=ticker))
            self._valid_prop.update({key:kwargs[key] for key in self._valid_prop if key in kwargs})
        else:
            self._valid_prop.update({key:MetaData.loc[ticker, key] for key in MetaData.columns})

        if self.exchange in ['FRED', 'OECD', 'ECOS']:
            return
        # ticker, name, quoteType, market, exchange, unit, shortName, longName, korName, sector, industry, benchmarkTicker, benchmarkName
        self.ticker = ticker
        self.dtype = self._valid_prop['dtype'] = ',d' if self.market == 'KOR' else '.2f'
        self._is_etf = self.quoteType == 'ETF'
        if self.market == 'KOR':
            self.__kr__()
        elif self.market == 'USA':
            self.__us__()
        else:
            pass

        self.path = self._valid_prop['path'] = os.path.join(PATH.BASE, f"{self.ticker}_{self.name}")
        os.makedirs(self.path, exist_ok=True)
        return

    @staticmethod
    def _fnguideSummary(ticker:str):
        url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A" \
              f"{ticker}&cID=&MenuYn=Y&ReportGB=D&NewMenuID=Y&stkGb=701"
        html = Soup(requests.get(url).content, 'lxml').find('ul', id='bizSummaryContent').find_all('li')
        t = '\n\n '.join([e.text for e in html])
        w = [
            '.\n' if t[n] == '.' and not any([t[n - 1].isdigit(), t[n + 1].isdigit(), t[n + 1].isalpha()]) else t[n]
            for n in range(1, len(t) - 2)
        ]
        s = ' ' + t[0] + ''.join(w) + t[-2] + t[-1]
        return s.replace(' ', '').replace('\xa0\xa0', ' ').replace('\xa0', ' ').replace('\n ', '\n')

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

    def __kr__(self):
        str2int = lambda x: int(x.replace(', ', '').replace(',', ''))
        nav2num = lambda x, n: float(x.replace(' ', '').replace('배', '').replace('원', '').replace(',', '').split('l')[n])

        # Common Properties
        guide = f"http://cdn.fnguide.com/SVO2/xml/Snapshot_all/{self.ticker}.xml"
        src = xml.fromstring(requests.get(url=guide).text).find('price')
        self._valid_prop.update({
            "previousClose": str2int(src.find('close_val').text),
            "foreignRate": float(src.find('frgn_rate').text),
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
                'businessSummary': self._fnguideSummary(self.ticker),
                "dividendYield": str(mul.iloc[3, 1]).replace('%', ''),
                "trailingPE": None if mul.iloc[0, 1].startswith('N/A') else nav2num(mul.iloc[0, 1], 0),
                "trailingEps": None if mul.iloc[0, 1].startswith('N/A') else nav2num(mul.iloc[0, 1], 1),
                "forwardPE": None if mul.iloc[1, 1].startswith('N/A') else nav2num(mul.iloc[1, 1], 0),
                "forwardEps": None if mul.iloc[1, 1].startswith('N/A') else nav2num(mul.iloc[1, 1], 1),
                "priceToBook": None if mul.iloc[2, 1].startswith('N/A') else nav2num(mul.iloc[2, 1], 0),
                "bookValue": None if mul.iloc[2, 1].startswith('N/A') else nav2num(mul.iloc[2, 1], 1),
                "targetPrice": None if cons.iloc[0, 1].startswith('N/A') else nav2num(cons.iloc[0, 1], 1),
                "returnOnEquity": comp.iloc[11, 1],  # Most Recent
                "floatShares": str2int(src.find('ff_sher').text),
                "shares": str2int(src.find('listed_stock_1').text),
            })
        if self._is_etf:
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
    def market(self) -> str:
        return self._valid_prop['market']

    @market.setter
    def market(self, market:str):
        self._valid_prop['market'] = market

    @property
    def businessSummary(self) -> str:
        return self._valid_prop['businessSummary']

    @property
    def previousClose(self) -> int or float:
        return self._valid_prop['previousClose']

    @property
    def foreignRate(self) -> int or float:
        return self._valid_prop['foreignRate']

    @property
    def dividendYield(self) -> int or float:
        return self._valid_prop['dividendYield']

    @property
    def benchmark_ticker(self) -> str:
        return self._valid_prop['benchmark_ticker']

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
    def gapTargetPrice(self):
        if not self.targetPrice:
            return None
        return round(100 * (self.previousClose / self.targetPrice - 1), 2)

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
    tester = _ticker('AAPL')
    # tester = _ticker('000660')
    # tester = _ticker('457690')
    # tester = _ticker('383310')
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

    # import random
    # samples = random.sample(MetaData.KRSTOCK.index.tolist(), 10)
    # samples = random.sample(MetaData.USSTOCK.index.tolist(), 10)
    # for sample in samples:
    #     print(f'\n{sample}', "=" * 75)
    #     stock = _ticker(sample)
    #     print(stock.description())
