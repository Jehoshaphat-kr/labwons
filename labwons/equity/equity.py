from typing import Any
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
from labwons.equity.fundamental.consensusprice import consensusprice
from labwons.equity.fundamental.consensusprofit import consensusprofit
from labwons.equity.fundamental.per import per
from labwons.equity.fundamental.consensustendency import consensustendency
from labwons.equity.fundamental.short import short
from labwons.equity.fundamental.products import products
from labwons.equity.fundamental.expense import expense
from labwons.equity.fundamental.multipleband import multipleband
from labwons.equity.fundamental.benchmarkmultiple import benchmarkmultiple
from labwons.equity.fundamental.similarity import similarity



class Equity(fetch):

    def __hasattr__(self, attr):
        return hasattr(self, attr)

    def __attr__(self, attr:str, cls:Any, **kwargs):
        _attr = self._attr(attr)
        if not hasattr(self, _attr):
            if kwargs:
                self.__setattr__(_attr, cls(**kwargs))
            else:
                self.__setattr__(_attr, cls(self))
        return self.__getattribute__(_attr)

    # @property
    # def backtest(self) -> backtest:
    #     if not self.__hasattr__(self._attr('backt')):
    #         self.__setattr__(self._attr('backt'), backtest(self.ohlcv, **self._valid_prop))
    #     return self.__getattribute__(self._attr('backt'))

    @property
    def sma(self) -> sma:
        return self.__attr__('sma', sma)

    @property
    def trend(self) -> trend:
        return self.__attr__('trend', trend)

    """
    COMPARISON
    """
    @property
    def benchmarkReturn(self) -> benchmark:
        return self.__attr__('benchmarkreturn', benchmark)

    @property
    def drawDown(self) -> drawdown:
        return self.__attr__('drawdown', drawdown)

    """
    VOLATILITY
    """
    @property
    def bollingerBand(self) -> bollingerband:
        return self.__attr__('bollingerband', bollingerband)

    """
    MOMENTUM
    """
    @property
    def rsi(self) -> rsi:
        return self.__attr__('rsi', rsi)

    """
    VOLUME
    """
    @property
    def moneyFlow(self) -> moneyflow:
        return self.__attr__('moneyflow', moneyflow)

    """
    TREND
    """
    @property
    def psar(self) -> psar:
        return self.__attr__('psar', psar)

    @property
    def macd(self) -> macd:
        return self.__attr__('macd', macd)

    """
    SUPPLY
    """
    @property
    def foreignRate(self) -> foreigner:
        return self.__attr__('foreignrate', foreigner)

    @property
    def consensusPrice(self) -> consensusprice:
        return self.__attr__('consensusprice', consensusprice)

    @property
    def consensusProfit(self) -> consensusprofit:
        return self.__attr__('consensusprofit', consensusprofit)

    @property
    def consensusTendency(self) -> consensustendency:
        # TODO
        return self.__attr__('consensustendency', consensustendency)

    @property
    def short(self) -> short:
        # TODO
        return

    """
    FUNDAMENTALS
    """
    @property
    def performance(self) -> performance:
        return self.__attr__('performance', performance)

    @property
    def soundness(self) -> soundness:
        return self.__attr__('soundness', soundness)

    @property
    def per(self) -> per:
        return self.__attr__('per', per)

    @property
    def products(self) -> products:
        # TODO
        return

    @property
    def expense(self) -> expense:
        # TODO
        return

    """
    MULTIPLES
    """
    @property
    def multipleBand(self) -> multipleband:
        return self.__attr__('multipleband', multipleband)

    @property
    def benchmarkMultiple(self) -> benchmarkmultiple:
        return self.__attr__('benchmarkmultiple', benchmarkmultiple)

    """
    ETC
    """
    @property
    def similarities(self) -> similarity:
        # TODO
        return

