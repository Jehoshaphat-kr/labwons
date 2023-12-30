from pandas import DataFrame, Series
from plotly.graph_objects import Scatter, Bar


class traces(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data
        self.meta = meta
        return

    @property
    def macd(self) -> Scatter:
        return Scatter(
            name="MACD",
            x=self.data.index,
            y=self.data.macd,
            mode="lines",
            line={
                "color": "orange",
            },
            visible=True,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="MACD: %{y}<extra></extra>"
        )

    @property
    def signal(self) -> Scatter:
        return Scatter(
            name="Signal",
            x=self.data.index,
            y=self.data.signal,
            mode="lines",
            line={
                "dash": "dash",
                "color": "#999"
            },
            visible=True,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="Signal: %{y}<extra></extra>"
        )

    @property
    def diff(self) -> Bar:
        return Bar(
            name="Diff",
            x=self.data.index,
            y=self.data["diff"],
            marker={
                "color":"grey",
            },
            visible=True,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="Diff: %{y}<extra></extra>"
        )
