from pandas import DataFrame, Series
from plotly.graph_objects import Scatter


class traces(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data[data.columns[1:]]
        self.meta = meta
        return

    def __line__(self, item:str) -> Scatter:
        if not item in self.data:
            return Scatter()
        data = self.data[item].dropna()
        return Scatter(
            name=data.name,
            x=data.index,
            y=data,
            mode='lines',
            visible="legendonly",
            showlegend=True,
            line={
                "color":"black",
                "dash":"dash",
                "width": 0.8
            },
            connectgaps=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=".2f",
            hovertemplate=str(data.name) + ': %{y}' + self.meta.currency + '<extra></extra>'
        )

    @property
    def all(self) -> list:
        return [self.__line__(col) for col in self.data]

