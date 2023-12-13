from labwons.asset.common.tech.typ.traces import traces
from labwons.common.charts import r1c1nsy
from pandas import DataFrame, Series
from plotly.graph_objects import Figure


class typ(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = (data.high + data.low + data.close) / 3
        self.data.name = f"{meta['name']}/T"
        self.meta = meta
        self.traces = traces(self.data)
        return

    def __call__(self, **kwargs):
        self.show(**kwargs)
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getitem__(self, item: str):
        return self.data[item]

    def __getattr__(self, item: str):
        if hasattr(self.data, item):
            return getattr(self.data, item)
        if not item in dir(self):
            raise AttributeError

    def figure(self, **kwargs) -> Figure:
        fig = r1c1nsy()
        fig.add_trace(trace=self.traces.trace)
        fig.update_layout(title=f"{self.meta['name']}({self.meta.name}): Typical Price", **kwargs)
        fig.update_yaxes(title=f"Price [{self.meta.currency}]")
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()
        return