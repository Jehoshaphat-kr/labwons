from pandas import Series
from plotly.graph_objects import Scatter


class traces(object):

    def __init__(self, data:Series, meta:Series):
        self.data = data.dropna()
        self.meta = meta
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
            trace = Scatter(
                name=self.meta.name,
                x=self.data.index,
                y=self.data,
                mode='lines',
                visible=True,
                showlegend=True,
                line={
                    "color":"royalblue"
                },
                connectgaps=True,
                xhoverformat='%Y/%m/%d',
                yhoverformat=".2f",
                hovertemplate=str(self.meta.name) + ': %{y}' + self.meta.currency + '<extra></extra>'
            )
            setattr(self, "_line", trace)
        return getattr(self, "_line")