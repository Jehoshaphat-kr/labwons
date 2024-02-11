
from pandas import DataFrame, Series
from numpy import nan


class stat(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data
        self.meta = meta
        self.__mem__ = {
            f"slopeByAll": None,
            "slopeBy5Y": None,
            "slopeBy2Y": None,
            "slopeBy1Y": None,
            "slopeBy6M": None,
            "slopeBy3M": None,
        }
        return

    def __repr__(self):
        return repr(self.carrier)

    def __contains__(self, item:str):
        return item in self.__mem__

    def __iter__(self):
        return iter(self.__mem__)

    def __getitem__(self, item:str):
        if not self.__mem__[item]:
            if item.startswith("slopeBy"):
                self.__mem__[item] = self._calcSlope(item.replace("slopeBy", ""))
        return self.__mem__[item]

    def _calcSlope(self, col:str) -> float:
        price = self.data.columns[0]
        sample = self.data[[price, col]].dropna().copy()
        if sample.empty:
            return nan
        offset = sample.iloc[0][price] - sample.iloc[0][col]
        if offset >= 0:
            offseted = sample[col] + offset
        else:
            offseted = sample[col] - offset
        return round((offseted[-1] - offseted[0]) / offseted[0], 4)

    @property
    def carrier(self) -> Series:
        __mem__ = {key: self[key] for key in self}
        return Series(__mem__, name=self.meta["ticker"])