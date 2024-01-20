from nohji.util.tools import int2won
from nohji.util.chart import r1c1sy1
from nohji.asset.fundamental.profitExpense import data

from pandas import DataFrame, Series
from plotly.graph_objects import Bar, Figure, Scatter


class profitExpense:
    colors = {
        "매출액": "#9BC2E6",
        "매출원가": "red",
        "판매비와관리비": "magenta",
        "영업이익": "#A9D08E",
    }

    def __init__(self, incomeStatement:DataFrame, meta:Series):
        if meta.country == "KOR":
            self.data = data.genKr(meta, incomeStatement)
        elif meta.country == "USA":
            self.data = data.genKr(meta, incomeStatement)
        else:
            raise AttributeError
        self.title = f"{meta['name']}({meta.name}) : 비용"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r1c1sy1(x_title='기말')
        for col in self.data.columns:
            if col.endswith("%"):
                continue
            series = self.data[col].fillna(0)
            if col == self.data.columns[0]:
                trace = Bar(
                    name=col,
                    x=series.index,
                    y=series,
                    visible=True,
                    showlegend=True,
                    opacity=0.85,
                    base=0,
                    width=0.4,
                    offset=-0.4,
                    meta=[int2won(x) for x in series],
                    texttemplate="%{meta}원",
                    hovertemplate=col + ": %{meta}원<extra></extra>",
                )
            else:
                trace = Bar(
                    name=col,
                    x=series.index,
                    y=series,
                    base=None,
                    width=0.4,
                    offset=0.0,
                    visible=True,
                    marker=dict(
                        color=self.colors[col],
                        opacity=0.85 if col == '영업이익' else 0.9
                    ),
                    meta=[int2won(x) for x in series],
                    customdata=self.data[f"{col}%"],
                    texttemplate="%{meta}원",
                    hovertemplate=col + ": %{meta}원(%{customdata:.2f}%)<extra></extra>"
                )
            fig.add_trace(secondary_y=False, trace=trace)

            if col == "영업이익":
                trace = Scatter(
                    name=f"{col}률",
                    x=series.index,
                    y=self.data[f"{col}%"],
                    mode="lines+text+markers",
                    visible=True,
                    showlegend=True,
                    yhoverformat=".2f",
                    texttemplate="%{y:.2f}%",
                    hovertemplate=col + ": %{y}%<extra></extra>"
                )
                fig.add_trace(secondary_y=True, trace=trace)
        fig.update_layout(
            title=f"{self.title}",
            barmode="stack",
            **kwargs
        )
        fig.update_yaxes(row=1, col=1, secondary_y=False, patch={"title": "[억원]"})
        fig.update_yaxes(row=1, col=1, secondary_y=True, patch={"title": "영업이익률 [%]"})
        return fig
