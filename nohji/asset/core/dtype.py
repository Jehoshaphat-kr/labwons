from pandas import DataFrame
from typing import Dict


class multiframes(DataFrame):

    __mem__ = {}
    def __init__(self, frames:Dict[str, DataFrame]):
        base = list(frames.values())[0]
        self.__mem__ = frames.copy()
        super().__init__(data=base.values, index=base.index, columns=base.columns)
        return

    def __getattr__(self, item):
        if item in self.__mem__:
            return self.__mem__[item]
        return super().__getattr__(name=item)
