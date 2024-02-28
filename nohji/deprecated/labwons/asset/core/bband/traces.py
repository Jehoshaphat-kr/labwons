from pandas import DataFrame, Series
from plotly.graph_objects import Scatter


class traces(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data[data.columns[1:]]
        self.meta = meta
        return

    @property
    def middle(self) -> Scatter:
        return Scatter(
            name="middle",
            x=self.data.index,
            y=self.data.middle,
            mode="lines",
            line={
                "dash": "dash",
                "color": "brown"
            },
            visible=True,
            showlegend=False,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="middle: %{y}" + self.meta.currency + "<extra></extra>"
        )

    @property
    def upperband(self) -> Scatter:
        return Scatter(
            name="x2 Band",
            x=self.data.index,
            y=self.data.upperband,
            mode="lines",
            line={
                "dash":"dash",
                "color":"maroon"
            },
            visible=True,
            showlegend=False,
            legendgroup="x2",
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="x2 Upper: %{y}" + self.meta.currency + "<extra></extra>"
        )

    @property
    def lowerband(self) -> Scatter:
        return Scatter(
            name="x2 Band",
            x=self.data.index,
            y=self.data.lowerband,
            mode="lines",
            line={
                "dash": "dash",
                "color": "maroon"
            },
            visible=True,
            showlegend=False,
            legendgroup="x2",
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="x2 Lower: %{y}" + self.meta.currency + "<extra></extra>"
        )

    @property
    def uppertrend(self) -> Scatter:
        return Scatter(
            name="x1 Band",
            x=self.data.index,
            y=self.data.uppertrend,
            mode="lines",
            line={
                "dash": "dot",
                "color": "green"
            },
            visible=True,
            showlegend=False,
            legendgroup="x1",
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="x1 Upper: %{y}" + self.meta.currency + "<extra></extra>"
        )

    @property
    def lowertrend(self) -> Scatter:
        return Scatter(
            name="x1 Band",
            x=self.data.index,
            y=self.data.lowertrend,
            mode="lines",
            line={
                "dash": "dot",
                "color": "green"
            },
            visible=True,
            showlegend=False,
            legendgroup="x1",
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="x1 Lower: %{y}" + self.meta.currency + "<extra></extra>"
        )

    @property
    def width(self) -> Scatter:
        return Scatter(
            name="Width",
            x=self.data.index,
            y=self.data.width,
            mode="lines",
            line={
                "color": "grey"
            },
            visible=True,
            showlegend=False,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="Width: %{y}%<extra></extra>"
        )

    @property
    def pctb(self) -> Scatter:
        return Scatter(
            name="%B",
            x=self.data.index,
            y=self.data.pctb,
            mode="lines",
            line={
                "color": "grey"
            },
            visible=True,
            showlegend=False,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="%B: %{y}<extra></extra>"
        )



