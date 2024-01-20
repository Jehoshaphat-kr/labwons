from nohji.asset.core.deco import common
from nohji.asset.fetch import Data
from nohji.asset.technical.ohlcv import ohlcv
from nohji.asset.technical.tp import tp


class Technical(object):

    def __init__(self, src:Data):
        self.meta = src.meta
        self.Ohlcv = ohlcv(src.ohlcv, src.meta)
        self.TypicalPrice = tp(src.ohlcv, src.meta)
        return

    @common
    def Trend(self):
        from nohji.asset.technical.trend import trend
        return trend(self.Ohlcv, self.TypicalPrice, self.meta)

    @common
    def Deviation(self):
        from nohji.asset.technical.deviation import deviation
        return deviation(self.Trend, self.meta)

    @common
    def SMA(self):
        from nohji.asset.technical.sma import sma
        return sma(self.Ohlcv, self.TypicalPrice, self.meta)

    @common
    def BollingerBand(self):
        from nohji.asset.technical.bollingerband import bollingerband
        return bollingerband(self.Ohlcv, self.TypicalPrice, self.meta)

    @common
    def MACD(self):
        from nohji.asset.technical.macd import macd
        return macd(self.Ohlcv, self.TypicalPrice, self.meta)

    @common
    def PSAR(self):
        from nohji.asset.technical.psar import psar
        return psar(self.Ohlcv, self.TypicalPrice, self.meta)

    @common
    def RSI(self):
        from nohji.asset.technical.rsi import rsi
        return rsi(self.Ohlcv, self.meta)

    @common
    def MoneyFlow(self):
        from nohji.asset.technical.moneyflow import moneyflow
        return moneyflow(self.Ohlcv, self.TypicalPrice, self.meta)
