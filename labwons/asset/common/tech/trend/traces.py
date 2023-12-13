from labwons.common.traces import lineTY
from pandas import DataFrame


class traces(object):

    def __init__(self, data:DataFrame):
        self.data = data[data.columns[1:]]
        return

    def __getattr__(self, item:str):
        if item[1:] in self.data:
            return lineTY(
                data=self.data[item[1:]],
                drop=True,
                line={"color":"black", "dash":"dash", "width": 0.8},
                visible="legendonly"
            )
        if not item in dir(self):
            raise AttributeError

    @property
    def all(self) -> list:
        return [getattr(self, f"L{col}") for col in self.data]

