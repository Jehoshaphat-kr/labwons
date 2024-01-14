from nohji.asset.fetch import fetch
from nohji.asset.fundamental import (
    assetQuality,
    products,
    profit,
    profitExpense,
    multipleBand
)

from inspect import signature
from pandas import DataFrame, Series


class fundamental(object):

    __slots__ = (
        "__mem__",
        "__src__",
        "assetQuality",
        "products",
        "profit",
        "profitExpense",
        "multipleBand"

    )

    def __init__(self, _fetch:fetch):
        self.__src__ = _fetch
        self.__mem__ = {}
        return

    def __str__(self) -> str:
        return ""

    def __getitem__(self, item:str):
        return self.__mem__[item]

    def __getattr__(self, item:str):
        if item in self.__mem__:
            return self.__mem__[item]
        if item in self.__slots__:
            _attr_ = getattr(globals()[item], item)
            self.__mem__[item] = _attr_(self.__src__)
            return self.__mem__[item]
        return object.__getattribute__(self, item)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    # ticker = "000660"
    ticker = "005930"
    # ticker = "001230"
    # ticker = "138080"
    # ticker = "316140"
    # ticker = "247540"

    mySrc = fetch(ticker)
    myTech = fundamental(mySrc)

    # myTech.profit()
    # myTech.assetQuality()
    # myTech.products()
    # myTech.profitExpense()
    myTech.multipleBand()

    # print(myTech.profit)
    # print(myTech.assetQuality)
    # print(myTech.profitExpense)


    # from plotly.offline import plot
    # from labwons.common.config import PATH
    #
    # plot(
    #     figure_or_data=myTech.ohlcv.figure(),
    #     auto_open=False,
    #     filename=f'{PATH.BASE}/{myTech.meta.name}_{myTech.meta["name"]}.html'
    # )

