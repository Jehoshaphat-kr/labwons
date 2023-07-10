from labwons.equity.refine import _refine
from labwons.equity.apps.ohlcv import ohlcv
from labwons.equity.apps.lines import lines
import pandas as pd


class Equity(_refine):

    @property
    def ohlcv(self) -> ohlcv:
        if not hasattr(self, '__ohlcv__'):
            self.__setattr__('__ohlcv__', ohlcv(self))
        return self.__getattribute__('__ohlcv__')

    @property
    def typical(self) -> lines:
        base = (self.ohlcv['close'] + self.ohlcv['high'] + self.ohlcv['low']) / 3
        base.name = f"{self.name}(T)"
        return lines(base)
