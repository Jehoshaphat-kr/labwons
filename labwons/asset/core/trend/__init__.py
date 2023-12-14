from labwons.asset.core.ohlcv import ohlcv
from labwons.asset.core.typ import typ
from labwons.asset.core.trend.data import gen
from labwons.asset.core.trend.traces import traces
from labwons.common.charts import r1c1nsy
from pandas import Series
from plotly.graph_objects import Figure


class trend(object):

    def __init__(self, ohlcv:ohlcv, typ:typ, meta:Series):
        self.ohlcv = ohlcv
        self.typ = typ
        self.data = gen(typ.data)
        self.meta = meta
        self.traces = traces(self.data, meta)
        return

    def __call__(self, **kwargs):
        self.show(**kwargs)
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getitem__(self, item:str):
        return self.data[item]

    def __getattr__(self, item:str):
        if hasattr(self.data, item):
            return getattr(self.data, item)
        if not item in dir(self):
            raise AttributeError

    def figure(self, **kwargs) -> Figure:
        fig = r1c1nsy()
        fig.add_trace(trace=self.ohlcv.traces.ohlc)
        fig.add_trace(trace=self.typ.traces(visible="legendonly"))
        fig.add_traces(data=self.traces.all)
        fig.update_layout(title=f"{self.meta['name']}({self.meta.name}): Trend", **kwargs)
        fig.update_yaxes(title=f"Price [{self.meta.currency}]")
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()
        return
