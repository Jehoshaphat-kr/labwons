from labwons.equity.source.fnguide import _url
from labwons.equity.source.fnguide import _req
from typing import Union, Callable
import pandas


class stock(object):

    class _two_dataframes(pandas.DataFrame):
        Y = pandas.DataFrame()
        Q = pandas.DataFrame()
        def __init__(self, Y:pandas.DataFrame, Q:pandas.DataFrame):
            self.Y, self.Q = Y, Q
            super().__init__(Y.values, Y.index, Y.columns)
            pass

    def __init__(self, ticker:str):
        self.__url__ = url = _url.url(ticker)
        self.__arg__ = {
            "abstract": {
                "url": url.snapshot,
                "gb" : url.gb,
                "period" : "Y"
            },
            "benchmarkMultiples": {
                "url": url.benchmarkMultiples
            },
            "businessSummary": {
                "url": url.snapshot
            },
            "cashFlow": {
                "url": url.finance,
                "period": "Y"
            },
            "consensusOutstanding" :{
                "url": url.snapshot
            },
            # "consensusPrice",
            # "consensusProfit",
            # "consensusTendency",
            # "expenses",
            # "financialStatement",
            # "foreignRate",
            # "growthRate",
            # "incomeStatement",
            # "marketCap",
            # "marketShares",
            # "multipleBand",
            # "multiples",
            # "multiplesOutstanding",
            # "products",
            # "profitRate",
            # "shareHolders",
            # "shortSell",
            "snapShot": {
                "url": url.xml
            },
            # "stabilityRate",
        }
        self.__mem__ = {}
        self.ticker = ticker
        return

    def __getattr__(self, attr:str):
        if not attr in self.__arg__:
            raise KeyError(f"""Invalid attribute name: {attr}""")
        if not attr in self.__mem__:
            self.__mem__[attr] = self.__slot__(attr)
        return self.__mem__[attr]

    def __slot__(self, attr:str):
        if "period" in self.__arg__[attr]:
            args = self.__arg__[attr].copy()
            args["period"] = "Q"
            return self._two_dataframes(
                Y = getattr(_req, attr)(**self.__arg__[attr]),
                Q = getattr(_req, attr)(**args)
            )
        return getattr(_req, attr)(**self.__arg__[attr])


if __name__ == "__main__":
    pandas.set_option('display.expand_frame_repr', False)

    t = '316140'
    myStock = stock(t)
    print(myStock.abstract)
    print(myStock.abstract.Y)
    print(myStock.abstract.Q)
    print(myStock.benchmarkMultiples)
    print(myStock.businessSummary)
    print(myStock.cashFlow)
    print(myStock.cashFlow.Y)
    print(myStock.cashFlow.Q)
    # print(myStock.snapShot)

