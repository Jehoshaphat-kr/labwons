from pandas import DataFrame, Series


class stat(object):

    def __init__(self, data:DataFrame):
        self.data = data
        self.last = data.iloc[-1]
        self.stat = {}
        return

    def __call__(self):
        for attr in dir(self):
            if attr.startswith("_") or attr in ["data", "last", "stat"]:
                continue
            if isinstance(attr, (float, int, str)):
                if not attr in self.stat:
                    self.stat[attr] = getattr(self, attr)
        return Series(self.stat)

    @property
    def gapRatio200Days(self) -> float:
        return round(100 * (self.last["close"] / self.last["200TD"] - 1), 2)

    @property
    def gapRatio120Days(self) -> float:
        return round(100 * (self.last["close"] / self.last["120TD"] - 1), 2)

    @property
    def gapRatio60Days(self) -> float:
        return round(100 * (self.last["close"] / self.last["60TD"] - 1), 2)