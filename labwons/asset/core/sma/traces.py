from pandas import DataFrame, Series
from plotly.graph_objects import Scatter


class traces(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data[data.columns[1:]]
        self.meta = meta
        return

    def __getattr__(self, item:str) -> Scatter:
        if not item in self.data:
            return Scatter()
        data = self.data[item].dropna()
        if not data.empty:
            return Scatter(
                name=data.name,
                x=data.index,
                y=data,
                mode='lines',
                visible="legendonly",
                showlegend=True,
                line={
                    "dash":"dot",
                },
                connectgaps=True,
                xhoverformat='%Y/%m/%d',
                yhoverformat=".2f",
                hovertemplate=str(data.name) + ': %{y}' + self.meta.currency + '<extra></extra>'
            )
        if data.empty or not item in dir(self):
            raise AttributeError

    @property
    def all(self) -> list:
        return [getattr(self, col) for col in self.data]
