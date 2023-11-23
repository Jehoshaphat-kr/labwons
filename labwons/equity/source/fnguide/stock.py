from labwons.equity.source.fnguide._url import url
from labwons.equity.source.fnguide._fetch import (
    fetchSnapShot,
    fetchHeader,
)
import pandas




class stock(object):

    def __init__(self, ticker:str):
        self.ticker = ticker
        self.url = url(ticker)
        return

    @property
    def basic(self) -> pandas.Series:
        """
        :return:
        date                 2023/11/21
        previousClose             12720
        fiftyTwoWeekHigh          13480
        fiftyTwoWeekLow           10950
        marketCap                 95648
        sharesOutstanding     751949461
        floatShares           662964566
        volume                  2486148
        foreignRate               37.34
        beta                    0.76677
        return1M                   1.52
        return3M                  10.99
        return6M                   5.65
        return1Y                   5.12
        return3Y                  27.58
        dtype: object
        """
        return fetchSnapShot(self.url.xml)


if __name__ == "__main__":
    pandas.set_option('display.expand_frame_repr', False)

    t = '316140'
    myStock = stock(t)
    print(myStock.basic)
    print(myStock.basic['date'])
    print(myStock.basic['volume'])