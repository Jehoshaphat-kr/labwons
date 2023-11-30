from labwons.equity.ticker.kr import _req, urls
import pandas


class fetch(object):

    __slots__ = (
        "__url__",
        "__mem__",
        "ticker",
        "abstract",
        "analogy",
        "benchmarkMultiples",
        "businessSummary",
        "cashFlow",
        "consensusOutstanding",
        "consensusPrice",
        "consensusProfit",
        "consensusTendency",
        "currentPrice",
        "expenses",
        "financialStatement",
        "foreignRate",
        "growthRate",
        "incomeStatement",
        "marketCap",
        "marketShares",
        "multipleBand",
        "multiples",
        "multiplesOutstanding",
        "multiplesTrailing",
        "products",
        "profitRate",
        "shareHolders",
        "shortBalance",
        "shortSell",
        "snapShot",
        "stabilityRate",
    )

    class _two_dataframes(pandas.DataFrame):
        Y = pandas.DataFrame()
        Q = pandas.DataFrame()
        def __init__(self, Y:pandas.DataFrame, Q:pandas.DataFrame):
            self.Y, self.Q = Y, Q
            super().__init__(Y.values, Y.index, Y.columns)
            pass

    def __init__(self, ticker:str):
        self.__url__ = urls.url(ticker)
        self.__mem__ = {}
        self.ticker = ticker
        return

    def __call__(self, attr:str):
        return self.__getattr__(attr)

    def __getattr__(self, attr:str):
        if not attr in self.__mem__:
            self.__mem__[attr] = self.__slot__(attr)
        return self.__mem__[attr]

    def __slot__(self, attr:str):
        func = getattr(_req, attr)
        args = {"_url": self.__url__}
        if "period" in func.__code__.co_varnames:
            args2 = args.copy()
            args["period"] = "Q"
            return self._two_dataframes(Y=func(**args), Q=func(**args2))
        if "ticker" in func.__code__.co_varnames:
            args = {"ticker": self.ticker}
        return func(**args)


class stock:

    def __init__(self, ticker:str):
        self.ticker = ticker
        self.D = fetch(ticker) # Source Data
        return








if __name__ == "__main__":
    pandas.set_option('display.expand_frame_repr', False)

    # t = '316140'
    t = '051910'  # LG 화학
    # t = '058470'  # 리노공업
    myStock = fetch(t)
    print(myStock.abstract)
    print(myStock.abstract.Y)
    print(myStock.abstract.Q)
    print(myStock.analogy)
    print(myStock.benchmarkMultiples)
    print(myStock.businessSummary)
    print(myStock.cashFlow)
    print(myStock.cashFlow.Y)
    print(myStock.cashFlow.Q)
    print(myStock.consensusOutstanding)
    print(myStock.consensusPrice)
    print(myStock.consensusProfit)
    print(myStock.consensusTendency)
    print(myStock.currentPrice)
    print(myStock.expenses)
    print(myStock.financialStatement)
    print(myStock.foreignRate)
    print(myStock.growthRate)
    print(myStock.incomeStatement)
    print(myStock.marketCap)
    print(myStock.marketShares)
    print(myStock.multipleBand)
    print(myStock.multiples)
    print(myStock.multiplesOutstanding)
    print(myStock.multiplesTrailing)
    print(myStock.products)
    print(myStock.profitRate)
    print(myStock.shareHolders)
    print(myStock.shortBalance)
    print(myStock.shortSell)
    print(myStock.snapShot)
    print(myStock.stabilityRate)


