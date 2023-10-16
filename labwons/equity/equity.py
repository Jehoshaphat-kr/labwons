from labwons.equity.fetch import fetch
from labwons.equity.technical.trend import trend
from labwons.equity.technical.sma import sma
from labwons.equity.technical.benchmark import benchmark
from labwons.equity.technical.drawdown import drawdown
from labwons.equity.technical.bollingerband import bollingerband
from labwons.equity.technical.rsi import rsi
from labwons.equity.technical.moneyflow import moneyflow
from labwons.equity.technical.psar import psar
from labwons.equity.technical.macd import macd
from labwons.equity.technical.backtest import backtest
from labwons.equity.fundamental.performance import performance
from labwons.equity.fundamental.soundness import soundness
from labwons.equity.fundamental.foreigner import foreigner
from labwons.equity.fundamental.consensus import consensus
from labwons.equity.fundamental.short import short
from labwons.equity.fundamental.products import products
from labwons.equity.fundamental.expense import expense
from labwons.equity.fundamental.multipleband import multipleband
from labwons.equity.fundamental.benchmarkmultiple import benchmarkmultiple
from labwons.equity.fundamental.similarity import similarity



class Equity(fetch):

    def __hasattr__(self, attr):
        return hasattr(self, attr)

    @property
    def backtest(self) -> backtest:
        if not self.__hasattr__(self._attr('backt')):
            self.__setattr__(self._attr('backt'), backtest(self.ohlcv, **self._valid_prop))
        return self.__getattribute__(self._attr('backt'))

    @property
    def sma(self) -> sma:
        if not self.__hasattr__(self._attr('sma')):
            self.__setattr__(self._attr('sma'), sma(self))
        return self.__getattribute__(self._attr('sma'))

    @property
    def trend(self) -> trend:
        if not self.__hasattr__(self._attr('trend')):
            self.__setattr__(self._attr('trend'), trend(self))
        return self.__getattribute__(self._attr('trend'))

    """
    COMPARISON
    """
    @property
    def benchmarkReturn(self) -> benchmark:
        if not self.__hasattr__(self._attr('benchmarkReturn')):
            self.__setattr__(self._attr('benchmarkReturn'), benchmark(self))
        return self.__getattribute__(self._attr('benchmarkReturn'))

    @property
    def drawDown(self) -> drawdown:
        if not self.__hasattr__(self._attr('drawdown')):
            self.__setattr__(self._attr('drawdown'), drawdown(self))
        return self.__getattribute__(self._attr('drawdown'))

    """
    VOLATILITY
    """
    @property
    def bollingerBand(self) -> bollingerband:
        if not self.__hasattr__(self._attr('bollinger')):
            self.__setattr__(self._attr('bollinger'), bollingerband(self))
        return self.__getattribute__(self._attr('bollinger'))

    """
    MOMENTUM
    """
    @property
    def rsi(self) -> rsi:
        if not self.__hasattr__(self._attr('rsi')):
            self.__setattr__(self._attr('rsi'), rsi(self))
        return self.__getattribute__(self._attr('rsi'))

    """
    VOLUME
    """
    @property
    def moneyFlow(self) -> moneyflow:
        if not self.__hasattr__(self._attr('moneyflow')):
            self.__setattr__(self._attr('moneyflow'), moneyflow(self))
        return self.__getattribute__(self._attr('moneyflow'))

    """
    TREND
    """
    @property
    def psar(self) -> psar:
        if not self.__hasattr__(self._attr('psar')):
            self.__setattr__(self._attr('psar'), psar(self))
        return self.__getattribute__(self._attr('psar'))

    @property
    def macd(self) -> macd:
        if not self.__hasattr__(self._attr('macd')):
            self.__setattr__(self._attr('macd'), macd(self))
        return self.__getattribute__(self._attr('macd'))

    """
    SUPPLY
    """
    @property
    def foreignHold(self) -> foreigner:
        if not self.__hasattr__(self._attr('foreignhold')):
            self.__setattr__(self._attr('foreignhold'), foreigner(self))
        return self.__getattribute__(self._attr('foreignhold'))

    @property
    def consensus(self) -> consensus:
        if not self.__hasattr__(self._attr('consensus')):
            self.__setattr__(self._attr('consensus'), consensus(self))
        return self.__getattribute__(self._attr('consensus'))

    @property
    def short(self) -> short:
        if not self.__hasattr__(self._attr('short')):
            self.__setattr__(self._attr('short'), short(self))
        return self.__getattribute__(self._attr('short'))

    """
    FUNDAMENTALS
    """
    @property
    def performance(self) -> performance:
        if not self.__hasattr__(self._attr('performance')):
            self.__setattr__(self._attr('performance'), performance(self))
        return self.__getattribute__(self._attr('performance'))

    @property
    def soundness(self) -> soundness:
        if not self.__hasattr__(self._attr('soundness')):
            self.__setattr__(self._attr('soundness'), soundness(self))
        return self.__getattribute__(self._attr('soundness'))

    @property
    def products(self) -> foreigner:
        if not self.__hasattr__(self._attr('products')):
            self.__setattr__(self._attr('products'), products(self))
        return self.__getattribute__(self._attr('products'))

    @property
    def expense(self) -> expense:
        if not self.__hasattr__(self._attr('expense')):
            self.__setattr__(self._attr('expense'), expense(self))
        return self.__getattribute__(self._attr('expense'))

    """
    MULTIPLES
    """
    @property
    def multipleBand(self) -> multipleband:
        if not self.__hasattr__(self._attr('multipleband')):
            self.__setattr__(self._attr('multipleband'), multipleband(self))
        return self.__getattribute__(self._attr('multipleband'))

    @property
    def benchmarkMultiple(self) -> benchmarkmultiple:
        if not self.__hasattr__(self._attr('benchmarkMultiple')):
            self.__setattr__(self._attr('benchmarkMultiple'), benchmarkmultiple(self))
        return self.__getattribute__(self._attr('benchmarkMultiple'))

    """
    ETC
    """
    @property
    def similarities(self) -> similarity:
        if not self.__hasattr__(self._attr('similarity')):
            self.__setattr__(self._attr('similarity'), similarity(self.similar))
        return self.__getattribute__(self._attr('similarity'))

