from nohji.asset.technical.ohlcv import ohlcv
from nohji.asset.technical.tp import tp
from nohji.asset.technical.trend import data, traces
from nohji.util.chart import r1c1nsy

from pandas import Series
from plotly.graph_objects import Figure


class trend(object):

    def __init__(self, ohlcv:ohlcv, tp:tp, meta:Series):
        self.ohlcv = ohlcv
        self.tp = tp
        self.data = data.gen(tp.data)
        self.meta = meta
        self.traces = traces.traces(self.data, meta)
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
        return object.__getattribute__(self, item)

    def figure(self, **kwargs) -> Figure:
        fig = r1c1nsy()
        fig.add_trace(trace=self.ohlcv.traces.ohlc)
        fig.add_trace(trace=self.tp.traces(visible="legendonly"))
        fig.add_traces(data=self.traces.all)
        fig.update_layout(title=f"{self.meta['name']}({self.meta.name}): Trend", **kwargs)
        fig.update_yaxes(title=f"Price [{self.meta.currency}]")
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()
        return
