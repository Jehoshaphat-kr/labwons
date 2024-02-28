from pandas import DataFrame, Series
from plotly.graph_objects import Scatter


class traces(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data
        self.meta = meta
        return

    @property
    def up(self) -> Scatter:
        return Scatter(
            name="High",
            x=self.data.index,
            y=self.data.up,
            mode="markers",
            marker={
                "symbol": "circle",
                "color": "#999",
                "size": 5
            },
            visible=True,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="Up: %{y}" + self.meta.currency + "<extra></extra>"
        )

    @property
    def down(self) -> Scatter:
        return Scatter(
            name="Down",
            x=self.data.index,
            y=self.data.down,
            mode="markers",
            marker={
                "symbol": "circle",
                "color": "#999",
                "size": 5
            },
            visible=True,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="Down: %{y}" + self.meta.currency + "<extra></extra>"
        )

    @property
    def pct(self) -> Scatter:
        return Scatter(
            name="%b",
            x=self.data.index,
            y=self.data.pct,
            mode="lines",
            visible=True,
            showlegend=False,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="%b: %{y}%<extra></extra>"
        )
