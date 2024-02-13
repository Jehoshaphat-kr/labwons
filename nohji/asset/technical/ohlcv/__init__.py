from nohji.asset.technical.ohlcv.traces import traces
from nohji.util.chart import r2c1nsy

from pandas import DataFrame, Series
from plotly.graph_objects import Figure


class ohlcv(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data
        self.meta = meta
        self.traces = traces(data, meta['name'])
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
        fig = r2c1nsy()
        fig.add_trace(row=1, col=1, trace=self.traces.ohlc)
        fig.add_trace(row=2, col=1, trace=self.traces.vol)
        fig.update_layout(title=f"{self.meta['name']}({self.meta.name}): OHLCV", **kwargs)
        fig.update_yaxes(row=1, col=1, title=f"Price [{self.meta.currency}]")
        fig.update_yaxes(row=2, col=1, title=f"Vol.")
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()
        return
