from pandas import DataFrame, Series
from plotly.graph_objects import Scatter, Bar


class traces(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data
        self.meta = meta
        return

    @property
    def mfi(self) -> Scatter:
        return Scatter(
            name="MFI",
            x=self.data.index,
            y=self.data.mfi,
            mode="lines",
            visible=True,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate="MFI: %{y}%<extra></extra>"
        )

    @property
    def cmf(self) -> Scatter:
        return Scatter(
            name="CMF",
            x=self.data.index,
            y=self.data.cmf,
            mode="lines",
            visible=True,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".4f",
            hovertemplate="CMF: %{y}<extra></extra>"
        )

    @property
    def obv(self) -> Scatter:
        return Scatter(
            name="OBV",
            x=self.data.index,
            y=self.data.obv,
            mode="lines",
            visible=True,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=",d",
            hovertemplate="OBV: %{y}<extra></extra>"
        )
