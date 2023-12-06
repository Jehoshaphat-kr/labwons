from typing import Union
from datetime import datetime
import yfinance, requests, warnings, pandas


class equity(object):

    _ed_:datetime.date = datetime.today().date()
    _pr_:int = 10
    _fq_:str = '1d'
    def __init__(self, ticker):
        self.ticker = ticker
        self._yahoo = yfinance.Ticker(ticker)
        return

    @property
    def enddate(self) -> str:
        return self._ed_.strftime("%Y%m%d")

    @enddate.setter
    def enddate(self, enddate: Union[str, datetime, datetime.date]):
        if isinstance(enddate, str):
            self._ed_ = datetime.strptime(enddate, "%Y%m%d").date()
        elif isinstance(enddate, datetime):
            self._ed_ = enddate.date()
        else:
            self._ed_ = enddate

    @property
    def period(self) -> int:
        return self._pr_

    @period.setter
    def period(self, period: int):
        self._pr_ = period

    @property
    def freq(self) -> str:
        return self._fq_

    @freq.setter
    def freq(self, freq: str):
        if not freq in ['30m', '60m', '1h', '1d', '5d', '1wk', '1mo', '3mo']:
            raise KeyError
        self._fq_ = freq

    @property
    def price(self) -> pandas.DataFrame:
        attr = f"_{self.enddate}_{self.period}_{self.freq}_"
        if not hasattr(self, attr):
            columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            ohlcv = self._yahoo.history(period=f'{self._pr_}y', interval=self._fq_)[columns]
            ohlcv = ohlcv.rename(columns=dict(zip(columns, [n.lower() for n in columns])))
            ohlcv['date'] = pandas.to_datetime(ohlcv.index)
            ohlcv['date'] = ohlcv['date'].dt.tz_convert('Asia/Seoul')
            ohlcv.index = ohlcv['date'].dt.date
            self.__setattr__(attr, ohlcv.drop(columns=['date']))
        return self.__getattribute__(attr)

    @property
    def info(self) -> pandas.Series:
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
        try:
            if not hasattr(self, '_desc'):
                desc = pandas.Series(self._yahoo.info)
                desc["name"] = desc["shortName"]
                self.__setattr__('_desc', desc)
            return self.__getattribute__('_desc')
        except requests.exceptions.HTTPError:
            warnings.warn("Warning: Server Blocked", Warning)
        return pandas.Series(dtype=float)



if __name__ == "__main__":
    pandas.set_option('display.expand_frame_repr', False)

    myEquity = equity('AAPL')
    # print(myEquity.price)
    # print(myEquity.info)
    for i, v in myEquity.info.items():
        print(i, v)
