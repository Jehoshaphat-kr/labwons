from labwons.asset.core.trend import trend
from labwons.asset.core.deviation.data import gen
from labwons.asset.core.deviation.traces import traces
from labwons.common.charts import r2c3nsy
from pandas import Series
from plotly.graph_objects import Figure


class deviation(object):

    def __init__(self, trend:trend, meta:Series):
        self.trend = trend
        self.data = gen(trend.data)
        self.meta = meta
        self.traces = traces(self.data, meta)
        return

    def __call__(self, **kwargs):
        self.show(**kwargs)
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getitem__(self, item: str):
        return self.data[item]

    def __getattr__(self, item: str):
        if item in dir(self):
            return getattr(self, item)
        if hasattr(self.data, item):
            return getattr(self.data, item)
        raise AttributeError

    def figure(self, **kwargs) -> Figure:
        fig = r2c3nsy(subplot_titles=self.columns)
        for name, row, col in (('All', 1, 1), ('5Y', 1, 2), ('2Y', 1, 3), ('1Y', 2, 1), ('6M', 2, 2), ('3M', 2, 3)):
            if self[name].dropna().empty:
                fig.add_annotation(row=row, col=col, x=0.5, y=0.5, text="<b>No Data</b>", showarrow=False)
            else:
                fig.add_trace(row=row, col=col, trace=getattr(self.traces, f"D{name}"))
        fig.update_layout(title=f"{self.meta['name']}({self.meta.name}): Deviation", **kwargs)
        fig.update_yaxes(autorange=False, range=[1.1 * self.min().min(), 1.1 * self.max().max()])
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()
        return