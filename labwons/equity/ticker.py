from labwons.common.metadata.metadata import MetaData
from labwons.common.config import PATH
from labwons.common.service.fnguide import fnguide
from typing import Union
import yfinance as yf
import pandas as pd
import numpy as np
import requests, os, warnings


class _ticker(object):

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

        self._valid_prop = {
            "ticker": None,  # Metadata
            "name": None,  # Metadata
            "quoteType": None,  # Metadata
            "country": None,  # Metadata
            "exchange": None,  # Metadata
            "currency": None,  # Metadata
            "shortName": None,  # Metadata
            "longName": None,  # Metadata
            "korName": None,  # Metadata
            "sector": None,  # Metadata
            "industry": None,  # Metadata
            "benchmarkTicker": None,  # Metadata
            "benchmarkName": None,  # Metadata
            "previousClose": None,
            "fiftyTwoWeekLow": None,
            "fiftyTwoWeekHigh": None,
            "targetPrice": None,
            "marketCap": None,
            "shares": None,
            "floatShares": None,
            "volume": None,
            "previousForeignRate": None,
            "dividendYield": None,
            "businessSummary": None,
            "beta": None,
            "trailingPE": None,
            "forwardPE": None,
            "priceToBook": None,
            "pegRatio": None,
            "path": '',
        }

        self.ticker = ticker
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
                    self._valid_prop[prop] = getattr(srv, prop)
        else:
            try:
                info = yf.Ticker(self.ticker).info      # [dict]
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
                for key in info:
                    if key in self._valid_prop:
                        self._valid_prop[key] = info[key]
            except requests.exceptions.HTTPError:
                warnings.warn("Warning: Server Blocked", Warning)

        self._valid_prop['ticker'] = ticker
        self._valid_prop["form"] = ',d' if self._valid_prop['currency'] == "KRW" else ',.2f'
        self._valid_prop["path"] = os.path.join(PATH.BASE, f"{ticker}_{self._valid_prop['name']}")
        return

    @property
    def name(self) -> str:
        return self._valid_prop['name']

    @property
    def quoteType(self) -> Union[int, float]:
        return self._valid_prop['quoteType']

    @property
    def country(self) -> str:
        return self._valid_prop['country']

    @property
    def exchange(self) -> Union[int, float]:
        return self._valid_prop['exchange']

    @property
    def currency(self) -> str:
        return self._valid_prop['currency']

    @currency.setter
    def currency(self, currency:str):
        self._valid_prop['currency'] = currency

    @property
    def shortName(self) -> str:
        return self._valid_prop['shortName']

    @property
    def longName(self) -> str:
        return self._valid_prop['longName']

    @property
    def korName(self) -> str:
        return self._valid_prop['korName']

    @property
    def sector(self) -> str:
        return self._valid_prop['sector']

    @property
    def industry(self) -> str:
        return self._valid_prop['industry']

    @property
    def benchmarkTicker(self) -> str:
        return self._valid_prop['benchmarkTicker']

    @property
    def benchmarkName(self) -> str:
        return self._valid_prop['benchmarkName']

    @property
    def previousClose(self) -> Union[int, float]:
        return self._valid_prop['previousClose']

    @property
    def fiftyTwoWeekLow(self) -> Union[int, float]:
        return self._valid_prop['fiftyTwoWeekLow']

    @property
    def fiftyTwoWeekHigh(self) -> Union[int, float]:
        return self._valid_prop['fiftyTwoWeekHigh']

    @property
    def targetPrice(self) -> Union[int, float]:
        return self._valid_prop['targetPrice']

    @property
    def marketCap(self) -> Union[int, float]:
        return self._valid_prop['marketCap']

    @property
    def shares(self) -> Union[int, float]:
        return self._valid_prop['shares']

    @property
    def floatShares(self) -> Union[int, float]:
        return self._valid_prop['floatShares']

    @property
    def volume(self) -> Union[int, float]:
        return self._valid_prop['volume']

    @property
    def previousForeignRate(self) -> Union[int, float]:
        return self._valid_prop['previousForeignRate']

    @property
    def dividendYield(self) -> Union[int, float]:
        return self._valid_prop['dividendYield']

    @property
    def businessSummary(self) -> str:
        return self._valid_prop['businessSummary']

    @property
    def beta(self) -> Union[int, float]:
        return self._valid_prop['beta']

    @property
    def trailingPE(self) -> Union[int, float]:
        return self._valid_prop['trailingPE']

    @property
    def forwardPE(self) -> Union[int, float]:
        return self._valid_prop['forwardPE']

    @property
    def priceToBook(self) -> Union[int, float]:
        return self._valid_prop['priceToBook']

    @property
    def pegRatio(self) -> Union[int, float]:
        return self._valid_prop['pegRatio']

    @property
    def path(self) -> str:
        return self._valid_prop["path"]

    @path.setter
    def path(self, path:str):
        self._valid_prop["path"] = path

    @property
    def floatSharesRate(self) -> Union[int, float]:
        return round(100 * self.floatShares / self.shares, 2)

    @property
    def fiftyTwoWeekHighRatio(self) -> float:
        return round(100 * (self.previousClose / self.fiftyTwoWeekHigh - 1), 2)

    @property
    def fiftyTwoWeekLowRatio(self) -> float:
        return round(100 * (self.previousClose / self.fiftyTwoWeekLow - 1), 2)

    @property
    def targetPriceRatio(self) -> float:
        if not self.targetPrice:
            return np.nan
        return round(100 * (self.previousClose / self.targetPrice - 1), 2)

    def description(self) -> pd.Series:
        series = pd.Series(data=self._valid_prop)
        series['ticker'] = self.ticker
        if not self.exchange in ['FRED', 'OECD', 'ECOS']:
            series['floatSharesRate'] = self.floatSharesRate
            series['gapFiftyTwoWeekHigh'] = self.fiftyTwoWeekHighRatio
            series['gapFiftyTwoWeekLow'] = self.fiftyTwoWeekLowRatio
            series['gapTargetPrice'] = self.targetPriceRatio
        return series


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)

    # print(yf.Ticker('AAPL').info)

    # tester = _ticker('LTPZ', exchange='NYSE')
    # tester = _ticker('QQQ')
    tester = _ticker('AAPL')
    # tester = _ticker('058470')
    # tester = _ticker('457690')
    # tester = _ticker('383310')
    # tester = _ticker('142210')
    # tester = _ticker('PDOT.U')

    print(tester.description())
    # print(tester.name)
    # print(tester.exchange)
    # print(tester.quote)
    # print(tester.currency)
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

    import random
    # samples = random.sample(MetaData.KRSTOCK.index.tolist(), 10)
    # samples = random.sample(MetaData.USSTOCK.index.tolist(), 10)
    # for sample in samples:
    #     print(f'\n{sample}', "=" * 75)
    #     stock = _ticker(sample)
    #     print(stock.description())
