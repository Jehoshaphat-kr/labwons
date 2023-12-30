from nohji.asset.technical.ohlcv import ohlcv
from nohji.asset.technical.tp import tp
from nohji.asset.technical.sma import data, traces, stat

from pandas import concat, Series
from plotly.graph_objects import Figure


class sma(object):

    def __init__(self, ohlcv:ohlcv, tp:tp, meta:Series):
        self.ohlcv = ohlcv
        self.tp = tp
        self.data = data.gen(tp.data)
        self.meta = meta
        self.stat = stat.stat(concat(objs=[ohlcv.data, self.data], axis=1))
        self.trac = traces.traces(self.data, meta)
        return

    def __call__(self, **kwargs):
        self.show(**kwargs)
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getitem__(self, item:str):
        return self.data[item]

    def __getattr__(self, item:str):
        for obj in (self.stat, self.data):
            if hasattr(obj, item):
                return getattr(obj, item)
        return object.__getattribute__(self, item)

    def figure(self, **kwargs) -> Figure:
        fig = self.ohlcv.figure(**kwargs)
        fig.add_trace(trace=self.tp.traces(visible="legendonly"))
        fig.add_traces(data=self.trac.all)
        fig.update_layout(title=f"{self.meta['name']}({self.meta.name}): Moving Average", **kwargs)
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()
        return
