from pandas import DataFrame, Series


class stat(object):

    def __init__(self, data:DataFrame):
        self.data = data

        self.__mem__ = {
            f"deviationByAll": None,
            "deviationBy5Y": None,
            "deviationBy2Y": None,
            "deviationBy1Y": None,
            "deviationBy6M": None,
            "deviationBy3M": None,
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
            if item.startswith("deviationBy"):
                self.__mem__[item] = self.data.iloc[-1][item.replace("deviationBy", "")]
        return self.__mem__[item]

    @property
    def carrier(self) -> Series:
        __mem__ = {key: self[key] for key in self}
        return Series(__mem__)
