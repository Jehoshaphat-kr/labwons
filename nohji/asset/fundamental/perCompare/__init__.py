from nohji.util.tools import int2won
from nohji.util.chart import r1c1nsy
from nohji.asset.fundamental.perCompare import data

from pandas import DataFrame, Series
from plotly.graph_objects import Bar, Figure


class perCompare:

    def __init__(
        self,
        abstract:DataFrame,
        resembles:DataFrame,
        multipleOutstanding:Series,
        snapShot:Series,
        currentPrice:int,
        meta:Series
    ):
        if meta.country == "KOR":
            self.data = data.genKr(abstract, resembles, multipleOutstanding, snapShot, currentPrice)
        elif meta.country == "USA":
            self.data = data.genKr(abstract, resembles, multipleOutstanding, snapShot, currentPrice)
        else:
            raise AttributeError
        self.meta = meta
        self.title = f"{meta['name']}({meta.name}) : PER 비교"
        self.currency = meta.currency
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r1c1nsy()
        names = []
        for i, x in self.data.iterrows():
            if i == self.meta.name:
                names.append(x.종목명)
            elif not x.종목명.startswith("Sector"):
                names.append(f"{x.종목명}({i})")
            else:
                names.append(x.종목명)
        trace = Bar(
            name="",
            x=names,
            y=self.data.PER,
            visible=True,
            showlegend=False,
            marker={
                "color":["#70AD47", "#A9D08E", "#A9D08E", "#A9D08E", "#C6E0B4",
                         "royalblue", "#800080", "#FFA500", "#FFC0CB", "#808080"]
            },
            texttemplate="%{y:.2f}",
            hovertemplate="%{y:.2f}<extra></extra>"
        )
        fig.add_trace(trace=trace)

        fig.update_layout(title=f"{self.title}", **kwargs)
        fig.update_yaxes(title="PER[-]")
        return fig
