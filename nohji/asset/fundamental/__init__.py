from nohji.asset.fetch import fetch
from nohji.asset.fundamental import profit

from inspect import signature
from pandas import DataFrame, Series


class fundamental(object):

    __slots__ = (
        "__mem__",
        "__src__",
        "profit",

    )

    def __init__(self, _fetch:fetch):
        self.__src__ = _fetch
        # self.data = data
        # self.meta = meta
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
            # _args_ = {arg: getattr(self, arg) for arg in signature(_attr_).parameters}
            # self.__mem__[item] = _attr_(**_args_)
            self.__mem__[item] = _attr_(self.__src__)
            return self.__mem__[item]
        return object.__getattribute__(self, item)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    ticker = "000660"

    mySrc = fetch(ticker)
    myTech = fundamental(mySrc)

    myTech.profit()


    # from plotly.offline import plot
    # from labwons.common.config import PATH
    #
    # plot(
    #     figure_or_data=myTech.ohlcv.figure(),
    #     auto_open=False,
    #     filename=f'{PATH.BASE}/{myTech.meta.name}_{myTech.meta["name"]}.html'
    # )

