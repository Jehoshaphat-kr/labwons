from nohji.asset.fetch import fetch
from nohji.asset.technical.ohlcv import ohlcv
from nohji.asset.technical import (
    bollingerband,
    deviation,
    macd,
    moneyflow,
    psar,
    rsi,
    sma,
    tp,
    trend,
)

from inspect import signature


class tech(object):

    __slots__ = (
        "__mem__",
        "data",
        "meta",
        "bollingerband",
        "deviation",
        "macd",
        "moneyflow",
        "psar",
        "rsi",
        "sma",
        "trend",
        "tp"
    )

    def __init__(self, fetch:fetch):
        self.data = fetch.krx.ohlcv
        self.meta = fetch.meta
        self.__mem__ = {"data": self.data, "meta": self.meta, "ohlcv": ohlcv(self.data, self.meta)}
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getitem__(self, item:str):
        return self.data[item]

    def __getattr__(self, item:str):
        if item in self.__mem__:
            return self.__mem__[item]
        if item in self.__slots__:
            _attr_ = getattr(globals()[item], item)
            _args_ = {arg: getattr(self, arg) for arg in signature(_attr_).parameters}
            self.__mem__[item] = _attr_(**_args_)
            return self.__mem__[item]
        return object.__getattribute__(self, item)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    ticker = "000660"

    mySrc = fetch(ticker)
    myTech = tech(mySrc)

    # myTech.bollingerband()
    # myTech.deviation()
    # myTech.macd()
    myTech.moneyflow()
    myTech.psar()
    # myTech.ohlcv()
    # myTech.rsi()
    myTech.sma()
    # myTech.tp()
    # myTech.trend()


    # from plotly.offline import plot
    # from labwons.common.config import PATH
    #
    # plot(
    #     figure_or_data=myTech.ohlcv.figure(),
    #     auto_open=False,
    #     filename=f'{PATH.BASE}/{myTech.meta.name}_{myTech.meta["name"]}.html'
    # )

