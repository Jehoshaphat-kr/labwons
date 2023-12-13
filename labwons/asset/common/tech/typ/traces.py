from labwons.common.traces import lineTY
from pandas import Series
from plotly.graph_objects import Scatter


class traces(object):

    def __init__(self, data:Series):
        self.data = data
        return

    def __call__(self, **kwargs) -> Scatter:
        trace = self.trace
        for key, val in kwargs.items():
            try:
                setattr(trace, key, val)
            except (AttributeError, KeyError, TypeError, ValueError):
                pass
        return trace

    @property
    def trace(self) -> Scatter:
        if not hasattr(self, "_line"):
            self.__setattr__("_line", lineTY(data=self.data, drop=True))
        return self.__getattribute__("_line")