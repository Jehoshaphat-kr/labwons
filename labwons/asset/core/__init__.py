from labwons.asset.core.ohlcv import ohlcv
from labwons.asset.core import bband, deviation, macd, moneyflow, psar, rsi, sma, trend, typ
from inspect import signature
from pandas import DataFrame, Series


class tech(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data
        self.meta = meta
        self._inst_ = {"data":data, "meta":meta, "ohlcv": ohlcv(data, meta)}
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getitem__(self, item:str):
        return self.data[item]

    def __getattr__(self, item:str):
        if item in self._inst_:
            return self._inst_[item]
        if item in globals():
            _attr_ = getattr(globals()[item], item)
            _args_ = {arg: getattr(self, arg) for arg in signature(_attr_).parameters}
            self._inst_[item] = _attr_(**_args_)
            return self._inst_[item]
        if not item in dir(self):
            raise AttributeError


if __name__ == "__main__":
    from pandas import set_option
    from labwons.asset.kr.etf.fetch import fetch
    set_option('display.expand_frame_repr', False)

    mySrc = fetch(
        # "005930"
        # "091170"
        "316140"
    )
    myTech = tech(mySrc.ohlcv, mySrc.meta)
    # print(myTech.typ)

    # myTech.ohlcv()

    print(myTech.trend)
    myTech.trend()

    # print(myTech.deviation)
    # myTech.deviation()

    # print(myTech.sma)
    # print(myTech.sma.stat())
    # myTech.sma()

    # print(myTech.bband)
    # myTech.bband()

    # print(myTech.rsi)
    # myTech.rsi()

    # print(myTech.psar)
    # myTech.psar()

    # print(myTech.macd)
    # myTech.macd()

    # print(myTech.moneyflow)
    # myTech.moneyflow()

    # from plotly.offline import plot
    # from labwons.common.config import PATH
    #
    # plot(
    #     figure_or_data=myTech.ohlcv.figure(),
    #     auto_open=False,
    #     filename=f'{PATH.BASE}/{myTech.meta.name}_{myTech.meta["name"]}.html'
    # )