from labwons.asset.core.ohlcv import ohlcv
from labwons.asset.core.typ import typ
from labwons.asset.core.macd import data
from nohji.deprecated.labwons.asset.core.macd import traces
from labwons.common.charts import r3c1sy3
from pandas import Series
from plotly.graph_objects import Figure


class macd(object):


    def __init__(self, ohlcv:ohlcv, typ:typ, meta:Series):
        self.ohlcv = ohlcv
        self.typ = typ
        self.data = data.gen(typ.data)
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
        fig = r3c1sy3()
        fig.add_trace(row=1, col=1, trace=self.ohlcv.traces.ohlc)
        fig.add_trace(row=1, col=1, trace=self.typ.traces(visible="legendonly"))
        fig.add_trace(row=2, col=1, trace=self.ohlcv.traces.vol)
        fig.add_trace(row=3, col=1, trace=self.trac.macd)
        fig.add_trace(row=3, col=1, trace=self.trac.signal)
        fig.add_trace(row=3, col=1, trace=self.trac.diff, secondary_y=True)

        fig.update_layout(title=f"{self.meta['name']}({self.meta.name}): MACD", **kwargs)
        fig.update_yaxes(row=1, col=1, title=f"Price [{self.meta.currency}]")
        fig.update_yaxes(row=2, col=1, title=f"Vol.")
        fig.update_yaxes(row=3, col=1, title=f"MACD [-]", secondary_y=False)
        fig.update_yaxes(row=3, col=1, title=f"Diff [-]", secondary_y=True)
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()
        return
