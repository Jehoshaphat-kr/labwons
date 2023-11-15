from labwons.common.metadata.metadata import MetaData
from labwons.common.config import PATH
from labwons.common.service.fnguide import fnguide
from labwons.common.service.naver import naver
from typing import Union
import yfinance as yf
import pandas as pd
import numpy as np
import requests, os, warnings


class krstock(naver, fnguide):

    def __init__(self, ticker:str, **kwargs):
        super().__init__(ticker=ticker)
        super().__init__(ticker=ticker)
        # super(fnguide, self).__init__(ticker=ticker)
        # super(naver, self).__init__(ticker=ticker)


        # if ticker not in MetaData.index and 'exchange' not in kwargs:
        #     """
        #     Possible @exchange list
        #     - for KOR: "KOSPI", "KOSDAQ",
        #     - for USA: "NYSE", "NASDAQ", "OTC", "PCX", "AMEX", "CBOE", "NCM", "NMS", ... ,
        #     - others : "FRED", "ECOS", "OECD"
        #     """
        #     raise KeyError(
        #         f'@ticker not found in MetaData, @exchange must be specified for ticker: {ticker}'
        #     )
        #
        # if ticker in MetaData.index:
        #     kwargs.update(MetaData.loc[ticker].to_dict())
        #
        # self.language = kwargs['language'] if 'language' in kwargs else 'eng'
        # self._valid_prop = {
        #     "ticker": np.nan,  # Metadata
        #     "name": np.nan,  # Metadata
        #     "quoteType": np.nan,  # Metadata
        #     "country": np.nan,  # Metadata
        #     "exchange": np.nan,  # Metadata
        #     "currency": np.nan,  # Metadata
        #     "shortName": np.nan,  # Metadata
        #     "longName": np.nan,  # Metadata
        #     "korName": np.nan,  # Metadata
        #     "sector": np.nan,  # Metadata
        #     "industry": np.nan,  # Metadata
        #     "benchmarkTicker": np.nan,  # Metadata
        #     "benchmarkName": np.nan,  # Metadata
        #     "previousClose": np.nan,
        #     "fiftyTwoWeekLow": np.nan,
        #     "fiftyTwoWeekHigh": np.nan,
        #     "targetPrice": np.nan,
        #     "marketCap": np.nan,
        #     "shares": np.nan,
        #     "floatShares": np.nan,
        #     "volume": np.nan,
        #     "previousForeignRate": np.nan,
        #     "dividendYield": np.nan,
        #     "businessSummary": np.nan,
        #     "beta": np.nan,
        #     "trailingPE": np.nan,
        #     "forwardPE": np.nan,
        #     "priceToBook": np.nan,
        #     "pegRatio": np.nan,
        #     "path": '',
        # }
        #
        # self.ticker = ticker
        # for key in self._valid_prop:
        #     if key in kwargs:
        #         self._valid_prop[key] = kwargs[key]
        #
        # if self._valid_prop['exchange'].upper() in ['FRED', 'OECD', 'ECOS']:
        #     return
        #
        # self._fnguide, self._naver = None, None
        # if self._valid_prop['country'].upper() == 'KOR' or self._valid_prop['exchange'].startswith('KO'):
        #     self._fnguide = _fnguide = fnguide(ticker)
        #     self._naver = naver(ticker)
        #     for prop in self._valid_prop:
        #         if hasattr(_fnguide, prop):
        #             self._valid_prop[prop] = getattr(_fnguide, prop)
        # else:
        #     try:
        #         info = yf.Ticker(self.ticker).info      # [dict]
        #         matches = dict(
        #             longBusinessSummary='businessSummary',
        #             sharesOutstanding='shares',
        #             trailingAnnualDividendRate='dividendYield',
        #             targetMeanPrice='targetPrice',
        #             category='sector',
        #             name='korName'
        #         )
        #         for k, v in matches.items():
        #             if k in info:
        #                 info[v] = info[k]
        #         for key in info:
        #             if key in self._valid_prop:
        #                 self._valid_prop[key] = info[key]
        #     except requests.exceptions.HTTPError:
        #         warnings.warn("Warning: Server Blocked", Warning)
        #
        # self._valid_prop['ticker'] = ticker
        # self._valid_prop["form"] = ',d' if self._valid_prop['currency'] == "KRW" else ',.2f'
        # self._valid_prop["path"] = os.path.join(PATH.BASE, f"{ticker}_{self._valid_prop['name']}")
        # return

if __name__ == "__main__":
    ticker = '316140'

    stock = krstock(ticker)
    print(stock.previousClose)