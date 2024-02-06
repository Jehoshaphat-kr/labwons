from nohji.asset.fetch import Data
from nohji.asset.technical import Technical
from nohji.asset.fundamental import Fundamental


class Asset(Technical, Fundamental):

    def __init__(self, ticker:str, period:int=10, freq:str="d"):
        self._src_ = __src__ = Data(ticker, period, freq)

        Technical.__init__(self, __src__)
        Fundamental.__init__(self, __src__)
        return

    def __getitem__(self, item):
        if hasattr(self._src_, item):
            return getattr(self._src_, item)
        raise KeyError(f"No such <item; {item}> in <Asset; {self['ticker']}>")





if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    asset = Asset(
        "005930"
        # "316140" # 우리금융지주
        # "058470" # 리노공업
        # "096770" # SK이노베이션
    )
    print(asset["meta"])
    print(asset["meta"]["products"])
    print(asset["businessSummary"])
    # print(asset._src_.businessSummary)

    # asset.Ohlcv()
    # asset.TypicalPrice()
    # asset.Trend()
    # asset.Deviation()
    # asset.SMA()
    # asset.BollingerBand()
    # asset.RSI()
    # asset.MACD()
    # asset.PSAR()
    # asset.MoneyFlow()
    #
    # asset.AssetQuality()
    # asset.Profit()
    # asset.ProfitExpenses()
    # asset.Products()
    # asset.MultipleBands()
    # asset.ProfitEstimate()
    # asset.PERs()
    # asset.Consensus()
    # asset.ForeignRate()
    # asset.Shorts()
    # asset.BenchmarkMultiples()
    # asset.Benchmarks()
    # asset.DrawDowns()

    # print(asset.MultipleBands)
    # print(asset.ProfitEstimate)
    # print(asset.PERs)
    # print(asset.Benchmarks)
