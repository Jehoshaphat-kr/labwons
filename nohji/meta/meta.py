from nohji._config import api
from nohji.meta import fetch

from pandas import concat, DataFrame, read_pickle, Series
from typing import Any, Hashable, Union
from requests import exceptions
from yfinance import Ticker
import os


class _meta:
    """
    Meta data for <project; nohji>

    @data
        type        : DataFrame
        description : listed asset with implicit information
        columns     : ['korName', 'sector', 'industry', 'name', 'benchmark', 'benchmarkTicker',
                       'products', 'ipo', 'settlingMonth', 'shortName', 'longName',
                       'quoteType', 'country', 'exchange', 'nav', 'marketCap', 'currency']
        example     : pass

    @__call__()
        :param      : <str; ticker>
        type        : Series
        description : single asset meta data
                      for yfinance(Yahoo) accessible asset, try Ticker(*).info once for full meta data.
                      if failed, normal condition will return
        index       : for normal case,
                      ['korName', 'sector', 'industry', 'name', 'benchmark', 'benchmarkTicker',
                       'products', 'ipo', 'settlingMonth', 'shortName', 'longName',
                       'quoteType', 'country', 'exchange', 'nav', 'marketCap', 'currency']

                      for yfinace accessible case
                      ["address1", "city", "state", "zip", "country", "phone", "website",
                       "industry", "industryKey", "industryDisp", "sector", "sectorKey", "sectorDisp",
                       "longBusinessSummary", "fullTimeEmployees", "companyOfficers",
                       "auditRisk", "boardRisk", "compensationRisk", "shareHolderRightsRisk", "overallRisk",
                       "governanceEpochDate", "compensationAsOfEpochDate",
                       "maxAge", "priceHint", "previousClose", "open", "dayLow", "dayHigh",
                       "regularMarketPreviousClose", "regularMarketOpen", "regularMarketDayLow", "regularMarketDayHigh",
                       "dividendRate", "dividendYield", "exDividendDate", "payoutRatio", "fiveYearAvgDividendYield",
                       "beta", "trailingPE", "forwardPE",
                       "volume", "regularMarketVolume", "averageVolume", "averageVolume10days", "averageDailyVolume10Day",
                       "bid", "ask", "bidSize", "askSize",
                       "marketCap", "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "priceToSalesTrailing12Months",
                       "fiftyDayAverage", "twoHundredDayAverage",
                       "trailingAnnualDividendRate", "trailingAnnualDividendYield",
                       "currency", "enterpriseValue", "profitMargins", "floatShares", "sharesOutstanding",
                       "sharesShort", "sharesShortPriorMonth", "sharesShortPreviousMonthDate",
                       "dateShortInterest", "sharesPercentSharesOut", "heldPercentInsiders", "heldPercentInstitutions",
                       "shortRatio", "shortPercentOfFloat", "impliedSharesOutstanding",
                       "bookValue", "priceToBook",
                       "lastFiscalYearEnd", "nextFiscalYearEnd",
                       "mostRecentQuarter", "earningsQuarterlyGrowth", "netIncomeToCommon",
                       "trailingEps", "forwardEps", "pegRatio",
                       "lastSplitFactor", "lastSplitDate",
                       "enterpriseToRevenue", "enterpriseToEbitda",
                       "52WeekChange", "SandP52WeekChange",
                       "lastDividendValue", "lastDividendDate",
                       "exchange", "quoteType", "symbol", "underlyingSymbol", "shortName", "longName",
                       "firstTradeDateEpochUtc", "timeZoneFullName", "timeZoneShortName",
                       "uuid", "messageBoardId", "gmtOffSetMilliseconds",
                       "currentPrice", "targetHighPrice", "targetLowPrice", "targetMeanPrice",  "targetMedianPrice",
                       "recommendationMean", "recommendationKey", "numberOfAnalystOpinions",
                       "totalCash", "totalCashPerShare", "ebitda", "totalDebt",
                       "quickRatio", "currentRatio",
                       "totalRevenue", "debtToEquity", "revenuePerShare", "returnOnAssets", "returnOnEquity",
                       "grossProfits", "freeCashflow", "operatingCashflow", "earningsGrowth", "revenueGrowth",
                       "grossMargins", "ebitdaMargins", "operatingMargins",
                       "financialCurrency", "trailingPegRatio"]
        example     :
            for normal case,
            korName                                                     삼성전자
            sector                                                            IT
            industry                                                 WI26 반도체
            name                                                        삼성전자
            benchmark                                                 KRX 반도체
            benchmarkTicker                                               091160
            products           통신 및 방송 장비 제조(무선) 제품, 반도체 제조...
            ipo                                                       1975-06-11
            settlingMonth                                                   12월
            shortName                                                SamsungElec
            longName                               Samsung Electronics Co., Ltd.
            quoteType                                                     EQUITY
            country                                                          KOR
            exchange                                                       KOSPI
            nav                                                              NaN
            marketCap                                                        NaN
            currency                                                         NaN
            ticker                                                        005930

            for yfinace accessible case
            address1             One Apple Park Way
            city                          Cupertino
            state                                CA
            zip                               95014
            country                   United States
                                        ...
            grossMargins                    0.44131
            ebitdaMargins                   0.32827
            operatingMargins                0.30134
            financialCurrency                   USD
            trailingPegRatio                 2.2706
    """
    ecos = fetch.ecos
    krse = fetch.krse
    nyse = fetch.nyse
    wise = fetch.wise

    __data__:DataFrame = DataFrame()
    def __init__(self):
        # src = "https://github.com/Jehoshaphat-kr/labwons/raw/master/nohji/meta/meta.pkl"
        src = os.path.join(os.path.dirname(__file__), r"meta.pkl")
        self.__data__ = read_pickle(src)
        return

    def __call__(self, ticker: Union[str, Hashable]) -> Series:
        if ticker.isalpha():
            try:
                asset = Series(Ticker(ticker).info)
                asset["name"] = asset["shortName"]
                return asset
            except exceptions.HTTPError: pass

        if ticker in self.index:
            asset = self.loc[ticker].copy()
            asset["ticker"] = ticker
            return asset

        asset = Series(index=self.columns, name=ticker)
        asset[["name", "country", "ticker"]] = ticker, "KOR" if ticker.isdigit() else "USA", ticker
        return asset

    def __str__(self) -> str:
        return str(self.__data__)

    def __getattr__(self, item:Any):
        if item in dir(self):
            return getattr(self, item)
        if hasattr(self.__data__, item):
            return getattr(self.__data__, item)
        raise AttributeError(f"No such attribute as {item} in <class; _meta>")

    def __getitem__(self, item:Any):
        return self.__data__[item]

    def __len__(self):
        return len(self.__data__)

    def __iter__(self):
        return iter(self.__data__)

    def update(self):
        krse = self.wise.data.join(self.krse.stock.drop(columns=["korName"]))
        data = concat([krse, self.krse.etf, self.nyse.data], axis=0)
        data["ipo"] = data["ipo"].dt.strftime("%Y-%m-%d")
        data.to_pickle(r"./meta.pkl")
        self.__data__ = data
        return

    @property
    def data(self) -> DataFrame:
        return self.__data__


# Alias
meta = _meta()


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    api.stockSymbol = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
    meta.update()
    # print(meta)
    # print(meta.columns)
    # print(meta("005930"))
    # print(meta("AAPL"))