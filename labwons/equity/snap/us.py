from pandas import Series
from requests import exceptions
from warnings import warn
from yfinance import Ticker


class snap(object):
    """
    :return:
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

    :indexes: ["address1", "city", "state", "zip", "country", "phone", "website",
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
    """
    def __init__(self, ticker:str):
        try:
            self.description = Series(Ticker(ticker).info)
            self.description["name"] = self.description["shortName"]
        except exceptions.HTTPError:
            warn(f"Warning: Server Blocked for <Ticker: {ticker}>", Warning)
            self.description = Series(dtype=float)
            self.description[["name", "ticker"]] = ticker, ticker
        self.description["label"] = f"{self.description['name']}({self.description['ticker']})"
        return

    def __call__(self) -> Series:
        return self.description

    def __getattr__(self, item):
        if item in self.description:
            return self.description[item]
        raise AttributeError
