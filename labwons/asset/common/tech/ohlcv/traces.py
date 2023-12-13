from labwons.common.traces import candleStick, barTY
from pandas import DataFrame
from plotly.graph_objects import Bar, Candlestick
from typing import Union, Hashable


class traces(object):

    def __init__(self, data:DataFrame, name:Union[str, Hashable]):
        self.data = data
        self.name = name
        return

    @property
    def ohlc(self) -> Candlestick:
        if not hasattr(self, "_ohlc"):
            self.__setattr__("_ohlc", candleStick(data=self.data, name=self.name, drop=True))
        return self.__getattribute__("_ohlc")

    @property
    def volume(self) -> Bar:
        if not hasattr(self, "_vol"):
            self.__setattr__("_vol", barTY(self.data.volume, drop=True))
        return self.__getattribute__("_vol")
