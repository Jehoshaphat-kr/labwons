from typing import Any
from labwons.equity.fetch import fetch
from labwons.equity.technical.trend import trend
from labwons.equity.technical.sma import sma
from labwons.equity.technical.bollingerband import bollingerband
from labwons.equity.technical.rsi import rsi
from labwons.equity.technical.moneyflow import moneyflow
from labwons.equity.technical.psar import psar
from labwons.equity.technical.macd import macd
from labwons.equity.fundamental.profit import profit
from labwons.equity.fundamental.profitestimate import profitestimate
from labwons.equity.fundamental.profitexpenses import profitexpenses
from labwons.equity.fundamental.soundness import soundness
from labwons.equity.fundamental.per import per
from labwons.equity.fundamental.perband import perband
from labwons.equity.fundamental.products import products
from labwons.equity.supply.foreigner import foreigner
from labwons.equity.supply.shorts import shorts
from labwons.equity.supply.consensus import consensus
from labwons.equity.benchmark.performance import performance
from labwons.equity.benchmark.drawdown import drawdown
from labwons.equity.benchmark.multiples import multiples


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

    @property
    def sma(self) -> sma:
        return self.__attr__('sma', sma)

    @property
    def trend(self) -> trend:
        return self.__attr__('trend', trend)

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
    def consensus(self) -> consensus:
        return self.__attr__('consensus', consensus)

    @property
    def shorts(self) -> shorts:
        return self.__attr__('shorts', shorts)

    """
    FUNDAMENTALS
    """
    @property
    def profit(self) -> profit:
        return self.__attr__('profit', profit)

    @property
    def profitEstimate(self) -> profitestimate:
        return self.__attr__('profitestimate', profitestimate)

    @property
    def profitExpenses(self) -> profitexpenses:
        # TODO
        # 특이산업 (매출 외) 예외 처리
        return self.__attr__('profitexpenses', profitexpenses)

    @property
    def soundness(self) -> soundness:
        # TODO
        # 재고비율 추가
        return self.__attr__('soundness', soundness)

    @property
    def per(self) -> per:
        return self.__attr__('per', per)

    @property
    def perBand(self) -> perband:
        return self.__attr__('perband', perband)

    @property
    def products(self) -> products:
        return self.__attr__('products', products)

    """
    BENCHMARK
    """
    @property
    def benchmarkReturns(self) -> performance:
        return self.__attr__('benchmarkreturn', performance)

    @property
    def benchmarkDrawDowns(self) -> drawdown:
        return self.__attr__('benchmarkdrawdown', drawdown)

    @property
    def benchmarkMultiples(self) -> multiples:
        return self.__attr__('benchmarkmultiple', multiples)

    # """
    # ETC
    # """
    # @property
    # def similarities(self) -> similarities:
    #     return self.__attr__('similarities', similarities)
    #
