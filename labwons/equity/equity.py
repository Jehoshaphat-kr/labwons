from labwons.equity.refine import _refine
from labwons.equity.technical import (
    ohlcv,
    line,
    lines,
    benchmark,
    drawdown,
    bollingerband,
    rsi,
    moneyflow,
    psar,
    macd
)
from labwons.equity.fundamental import (
    foreigner,
    products,
    consensus
)


class Equity(_refine):

    def __hasattr__(self, attr):
        return hasattr(self, attr)

    """
    PRICE
    """
    @property
    def ohlcv(self) -> ohlcv:
        if not self.__hasattr__('__ohlcv__'):
            self.__setattr__('__ohlcv__', ohlcv(self))
        return self.__getattribute__('__ohlcv__')

    @property
    def typical(self) -> line:
        if not self.__hasattr__('__typical__'):
            attr = line(base=(self.ohlcv['close'] + self.ohlcv['high'] + self.ohlcv['low']) / 3, name=f"{self.name}(T)")
            self.__setattr__('__typical__', attr)
        return self.__getattribute__('__typical__')

    @property
    def open(self) -> line:
        if not self.__hasattr__('__open__'):
            self.__setattr__('__open__', line(base=self.ohlcv['open'], name=f"{self.name}(O)"))
        return self.__getattribute__('__open__')

    @property
    def high(self) -> line:
        if not self.__hasattr__('__high__'):
            self.__setattr__('__high__', line(base=self.ohlcv['high'], name=f"{self.name}(H)"))
        return self.__getattribute__('__high__')

    @property
    def low(self) -> line:
        if not self.__hasattr__('__low__'):
            self.__setattr__('__low__', line(base=self.ohlcv['low'], name=f"{self.name}(L)"))
        return self.__getattribute__('__low__')

    @property
    def close(self) -> line:
        if not self.__hasattr__('__close__'):
            self.__setattr__('__close__', line(base=self.ohlcv['close'], name=f"{self.name}(C)"))
        return self.__getattribute__('__close__')

    @property
    def sma(self) -> lines:
        if not self.__hasattr__('__sma__'):
            self.__setattr__('__sma__', lines(self.calcMA(), base=self, title='SMA'))
        return self.__getattribute__('__sma__')

    @property
    def trend(self) -> lines:
        if not self.__hasattr__('__trend__'):
            self.__setattr__('__trend__', lines(self.calcTrend(), base=self, title='TREND'))
        return self.__getattribute__('__trend__')

    """
    COMPARISON
    """
    @property
    def benchmark(self) -> benchmark:
        if not self.__hasattr__('__benchmark__'):
            self.__setattr__('__benchmark__', benchmark(self))
        return self.__getattribute__('__benchmark__')

    @property
    def drawDown(self) -> drawdown:
        if not self.__hasattr__('__drawdown__'):
            self.__setattr__('__drawdown__', drawdown(self))
        return self.__getattribute__('__drawdown__')

    """
    VOLATILITY
    """
    @property
    def bollingerBand(self) -> bollingerband:
        if not self.__hasattr__('__bollingerband__'):
            self.__setattr__('__bollingerband__', bollingerband(self))
        return self.__getattribute__('__bollingerband__')

    """
    MOMENTUM
    """
    @property
    def rsi(self) -> rsi:
        if not self.__hasattr__('__rsi__'):
            self.__setattr__('__rsi__', rsi(self))
        return self.__getattribute__('__rsi__')

    """
    VOLUME
    """
    @property
    def moneyFlow(self) -> moneyflow:
        if not self.__hasattr__('__moneyflow__'):
            self.__setattr__('__moneyflow__', moneyflow(self))
        return self.__getattribute__('__moneyflow__')

    """
    TREND
    """
    @property
    def psar(self) -> psar:
        if not self.__hasattr__('__psar__'):
            self.__setattr__('__psar__', psar(self))
        return self.__getattribute__('__psar__')

    @property
    def macd(self) -> macd:
        if not self.__hasattr__('__macd__'):
            self.__setattr__('__macd__', macd(self))
        return self.__getattribute__('__macd__')

    """
    FUNDAMENTAL
    """
    @property
    def foreigner(self) -> foreigner:
        if not self.__hasattr__('__foreigner__'):
            self.__setattr__('__foreigner__', foreigner(self))
        return self.__getattribute__('__foreigner__')

    @property
    def products(self) -> foreigner:
        if not self.__hasattr__('__products__'):
            self.__setattr__('__products__', products(self))
        return self.__getattribute__('__products__')

    @property
    def consensus(self) -> consensus:
        if not self.__hasattr__('__concensus__'):
            self.__setattr__('__concensus__', consensus(self))
        return self.__getattribute__('__concensus__')