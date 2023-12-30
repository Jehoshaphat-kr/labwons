from nohji.asset.technical.ohlcv import ohlcv
from nohji.asset.technical.tp import tp
from nohji.asset.technical.psar import data, traces
from nohji.util.chart import r3c1nsy

from pandas import Series
from plotly.graph_objects import Figure


class psar(object):

    def __init__(self, ohlcv:ohlcv, tp:tp, meta:Series):
        self.ohlcv = ohlcv
        self.tp = tp
        self.data = data.gen(ohlcv.data)
        self.meta = meta
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
        if item in dir(self):
            return getattr(self, item)
        if hasattr(self.data, item):
            return getattr(self.data, item)
        raise AttributeError

    def figure(self, **kwargs) -> Figure:
        fig = r3c1nsy()
        fig.add_trace(row=1, col=1, trace=self.ohlcv.traces.ohlc)
        fig.add_trace(row=1, col=1, trace=self.tp.traces(visible="legendonly"))
        fig.add_trace(row=1, col=1, trace=self.trac.rise)
        fig.add_trace(row=1, col=1, trace=self.trac.fall)
        fig.add_trace(row=2, col=1, trace=self.ohlcv.traces.vol)
        fig.add_trace(row=3, col=1, trace=self.trac.pct)
        fig.add_hline(row=3, col=1, y=0, line_color="black", line_dash="dash", line_width=0.9)

        fig.update_layout(title=f"{self.meta['name']}({self.meta.name}): Parabolic Stop and Reverse", **kwargs)
        fig.update_xaxes(patch={"autorange": False, "range": [self.index[0], self.index[-1]]})
        fig.update_yaxes(row=1, col=1, title=f"Price [{self.meta.currency}]")
        fig.update_yaxes(row=2, col=1, title=f"Vol.")
        fig.update_yaxes(row=3, col=1, title=f"%b [%]")
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()
        return
