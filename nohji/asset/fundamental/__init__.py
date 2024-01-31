from nohji.asset.core.deco import stockonly, etfonly
from nohji.asset.fetch import Data

from pandas import DataFrame, Series


class Fundamental(object):

    def __init__(self, src:Data):
        self.src = src
        self.meta = src.meta
        return

    def __str__(self) -> str:
        return ""

    @stockonly
    def AssetQuality(self):
        from nohji.asset.fundamental.assetQuality import assetQuality
        return assetQuality(self.src.abstract, self.src.yearlyMarketCap, self.meta)

    @stockonly
    def Profit(self):
        from nohji.asset.fundamental.profit import profit
        return profit(self.src.abstract, self.src.yearlyMarketCap, self.src.quarterlyMarketCap, self.meta)

    @stockonly
    def ProfitExpenses(self):
        from nohji.asset.fundamental.profitExpense import profitExpense
        return profitExpense(self.src.incomeStatement, self.meta)

    @stockonly
    def ProfitEstimate(self):
        from nohji.asset.fundamental.profitEstimate import profitEstimate
        return profitEstimate(self.src.consensusProfit, self.meta)

    @stockonly
    def Products(self):
        from nohji.asset.fundamental.products import products
        return products(self.src.products, self.meta)

    @stockonly
    def MultipleBands(self):
        from nohji.asset.fundamental.multipleBand import multipleBand
        return multipleBand(self.src.multipleBand, self.meta)

    @stockonly
    def PERs(self):
        from nohji.asset.fundamental.perCompare import perCompare
        return perCompare(
            self.src.abstract,
            self.src.resemblances,
            self.src.multiplesOutstanding,
            self.src.snapShot,
            self.src.currentPrice,
            self.meta
        )

    @stockonly
    def Consensus(self):
        from nohji.asset.fundamental.consensus import consensus
        return consensus(self.src.consensusPrice, self.meta)

    @stockonly
    def ForeignRate(self):
        from nohji.asset.fundamental.foreignRate import foreignRate
        return foreignRate(self.src.foreignExhaustRate, self.meta)

    @stockonly
    def Shorts(self):
        from nohji.asset.fundamental.shorts import shorts
        return shorts(self.src.shortSell, self.src.shortBalance, self.meta)

    @stockonly
    def BenchmarkMultiples(self):
        from nohji.asset.fundamental.benchmarkMultiples import benchmarkMultiples
        return benchmarkMultiples(self.src.benchmarkMultiples, self.meta)

    @stockonly
    def Benchmarks(self):
        from nohji.asset.fundamental.benchmarks import benchmarks
        return benchmarks(self.src.resemblances, self.meta)

    @stockonly
    def DrawDowns(self):
        from nohji.asset.fundamental.drawdowns import drawDown
        return drawDown(self.src.resemblances, self.meta)
