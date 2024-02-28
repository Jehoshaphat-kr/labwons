from typing import Any
from nohji.deprecated.labwons.equity import fetch
from nohji.deprecated.labwons.equity import trend
from nohji.deprecated.labwons.equity import sma
from nohji.deprecated.labwons.equity import bollingerband
from nohji.deprecated.labwons.equity import rsi
from nohji.deprecated.labwons.equity._de.technical.moneyflow import moneyflow
from nohji.deprecated.labwons.equity import psar
from nohji.deprecated.labwons.equity import macd
from nohji.deprecated.labwons.equity._de.fundamental.profit import profit
from nohji.deprecated.labwons.equity._de.fundamental.profitestimate import profitestimate
from nohji.deprecated.labwons.equity import profitexpenses
from nohji.deprecated.labwons.equity import soundness
from nohji.deprecated.labwons.equity._de.fundamental.per import per
from nohji.deprecated.labwons.equity._de.fundamental.perband import perband
from nohji.deprecated.labwons.equity import products
from nohji.deprecated.labwons.equity import foreigner
from nohji.deprecated.labwons.equity import shorts
from nohji.deprecated.labwons.equity import consensus
from nohji.deprecated.labwons.equity._de.benchmark import performance
from nohji.deprecated.labwons.equity import drawdown
from nohji.deprecated.labwons.equity import multiples


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
