from labwons.equity.refine import _refine
from labwons.equity.technical.ohlcv import ohlcv
from labwons.equity.technical.lines import line, lines
from labwons.equity.technical.benchmark import benchmark
from labwons.equity.technical.drawdown import drawdown
import pandas as pd


class Equity(_refine):

    @property
    def ohlcv(self) -> ohlcv:
        if not hasattr(self, '__ohlcv__'):
            self.__setattr__('__ohlcv__', ohlcv(self))
        return self.__getattribute__('__ohlcv__')

    @property
    def typical(self) -> line:
        base = (self.ohlcv['close'] + self.ohlcv['high'] + self.ohlcv['low']) / 3
        base.name = f"{self.name}(T)"
        return line(base)

    @property
    def open(self) -> line:
        base = self.ohlcv['open']
        base.name = f"{self.name}(O)"
        return line(base)

    @property
    def high(self) -> line:
        base = self.ohlcv['high']
        base.name = f"{self.name}(H)"
        return line(base)

    @property
    def low(self) -> line:
        base = self.ohlcv['low']
        base.name = f"{self.name}(L)"
        return line(base)

    @property
    def close(self) -> line:
        base = self.ohlcv['close']
        base.name = f"{self.name}(C)"
        return line(base)

    @property
    def benchmark(self) -> benchmark:
        return benchmark(self)

    @property
    def drawdown(self) -> drawdown:
        return drawdown(self)

    @property
    def sma(self) -> lines:
        return lines(self.calcMA(), base=self, title='SMA')

    @property
    def trend(self) -> lines:
        return lines(self.calcTrend(), base=self, title='TREND')