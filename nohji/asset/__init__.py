from nohji.asset.fetch import Data
from nohji.asset.technical import Technical
from nohji.asset.fundamental import Fundamental


class Asset(Technical, Fundamental):

    def __init__(self, ticker:str, period:int=10, freq:str="d"):
        self.D = D = Data(ticker, period, freq)
        Technical.__init__(self, D)
        Fundamental.__init__(self, D)
        return



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    asset = Asset("000660")

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

    # print(asset.MultipleBands)
    # print(asset.ProfitEstimate)
    # print(asset.PERs)
