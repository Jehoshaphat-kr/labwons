from labwons.equity.ohlcv import _ohlcv
from labwons.equity.technical.trend import trend
#     _trend,
#     # line,
#     # lines,
#     # benchmark,
#     # drawdown,
#     # bollingerband,
#     # rsi,
#     # moneyflow,
#     # psar,
#     # macd
# )
from labwons.equity.fundamental import (
    foreigner,
    products,
    consensus,
    short,
    expense,
    multipleband,
    benchmarkmultiple,
    performance,
    statement
)


class Equity(_ohlcv):
    _by_ = 'annual'
    def __hasattr__(self, attr):
        return hasattr(self, attr)

    @property
    def by(self) -> str:
        return self._by_

    @by.setter
    def by(self, by:str):
        self._by_ = by


    #
    # @property
    # def sma(self) -> lines:
    #     if not self.__hasattr__('__sma__'):
    #         self.__setattr__('__sma__', lines(self.calcMA(), base=self, title='SMA'))
    #     return self.__getattribute__('__sma__')
    #
    @property
    def trend(self) -> trend:
        attr = f'_trend_{self.enddate}_{self.period}_{self.freq}'
        if not self.__hasattr__(attr):
            self.__setattr__(attr, trend(self.typical, **self._valid_prop))
        return self.__getattribute__(attr)
    #
    # """
    # COMPARISON
    # """
    # @property
    # def benchmark(self) -> benchmark:
    #     if not self.__hasattr__('__benchmark__'):
    #         self.__setattr__('__benchmark__', benchmark(self))
    #     return self.__getattribute__('__benchmark__')
    #
    # @property
    # def drawDown(self) -> drawdown:
    #     if not self.__hasattr__('__drawdown__'):
    #         self.__setattr__('__drawdown__', drawdown(self))
    #     return self.__getattribute__('__drawdown__')
    #
    # """
    # VOLATILITY
    # """
    # @property
    # def bollingerBand(self) -> bollingerband:
    #     if not self.__hasattr__('__bollingerband__'):
    #         self.__setattr__('__bollingerband__', bollingerband(self))
    #     return self.__getattribute__('__bollingerband__')
    #
    # """
    # MOMENTUM
    # """
    # @property
    # def rsi(self) -> rsi:
    #     if not self.__hasattr__('__rsi__'):
    #         self.__setattr__('__rsi__', rsi(self))
    #     return self.__getattribute__('__rsi__')
    #
    # """
    # VOLUME
    # """
    # @property
    # def moneyFlow(self) -> moneyflow:
    #     if not self.__hasattr__('__moneyflow__'):
    #         self.__setattr__('__moneyflow__', moneyflow(self))
    #     return self.__getattribute__('__moneyflow__')
    #
    # """
    # TREND
    # """
    # @property
    # def psar(self) -> psar:
    #     if not self.__hasattr__('__psar__'):
    #         self.__setattr__('__psar__', psar(self))
    #     return self.__getattribute__('__psar__')
    #
    # @property
    # def macd(self) -> macd:
    #     if not self.__hasattr__('__macd__'):
    #         self.__setattr__('__macd__', macd(self))
    #     return self.__getattribute__('__macd__')
    #
    # """
    # FUNDAMENTAL
    # """
    # @property
    # def foreigner(self) -> foreigner:
    #     if not self.__hasattr__('__foreigner__'):
    #         self.__setattr__('__foreigner__', foreigner(self))
    #     return self.__getattribute__('__foreigner__')
    #
    # @property
    # def products(self) -> foreigner:
    #     if not self.__hasattr__('__products__'):
    #         self.__setattr__('__products__', products(self))
    #     return self.__getattribute__('__products__')
    #
    # @property
    # def consensus(self) -> consensus:
    #     if not self.__hasattr__('__concensus__'):
    #         self.__setattr__('__concensus__', consensus(self))
    #     return self.__getattribute__('__concensus__')
    #
    # @property
    # def short(self) -> short:
    #     if not self.__hasattr__('__short__'):
    #         self.__setattr__('__short__', short(self))
    #     return self.__getattribute__('__short__')
    #
    # @property
    # def expense(self) -> expense:
    #     if not self.__hasattr__('__expense__'):
    #         self.__setattr__('__expense__', expense(self))
    #     return self.__getattribute__('__expense__')
    #
    # @property
    # def multipleBand(self) -> multipleband:
    #     if not self.__hasattr__('__multipleband__'):
    #         self.__setattr__('__multipleband__', multipleband(self))
    #     return self.__getattribute__('__multipleband__')
    #
    # @property
    # def benchmarkMultiple(self) -> benchmarkmultiple:
    #     if not self.__hasattr__('__benchmarkmultiple__'):
    #         self.__setattr__('__benchmarkmultiple__', benchmarkmultiple(self))
    #     return self.__getattribute__('__benchmarkmultiple__')
    #
    # @property
    # def performance(self) -> performance:
    #     if not self.__hasattr__(f'__performance_{self.by}__'):
    #         self.__setattr__(f'__performance_{self.by}__', performance(self, by=self.by))
    #     return self.__getattribute__(f'__performance_{self.by}__')
    #
    # @property
    # def statement(self) -> statement:
    #     if not self.__hasattr__(f'__statement_{self.by}__'):
    #         self.__setattr__(f'__statement_{self.by}__', statement(self, by=self.by))
    #     return self.__getattribute__(f'__statement_{self.by}__')