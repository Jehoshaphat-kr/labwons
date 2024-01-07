from nohji.asset.fetch import fetch
from nohji.util.brush import int2won
from nohji.util.chart import r1c1sy1
from nohji.asset.fundamental.profitExpense import data

from plotly.graph_objects import Bar, Figure, Scatter


class profitExpense:

    # colors = {
    #     "매출액": "#9BC2E6",
    #     "매출원가": "#FF7C80",
    #     "판매비와관리비": "#F4B084",
    #     "영업이익": "#A9D08E",
    # }

    def __init__(self, _fetch:fetch):
        if _fetch.meta.country == "KOR":
            self.data = data.genKr(_fetch)
        elif _fetch.meta.country == "USA":
            self.data = data.genKr(_fetch)
        else:
            raise AttributeError
        self.title = f"{_fetch.meta['name']}({_fetch.meta.name}) : 비용"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r1c1sy1(x_title='기말')
        for col in self.data.columns:
            series = self.data[col].dropna()
            secondary_y = False
            if col == "영업이익률":
                trace = Scatter(
                    name=col,
                    x=series.index,
                    y=series,
                    mode="lines+text+markers",
                    visible=True,
                    showlegend=True,
                    yhoverformat=".2f",
                    texttemplate="%{y:.2f}%",
                    hovertemplate=col + ": %{y}%<extra></extra>"
                )
                secondary_y = True
            elif col == self.data.columns[0]:
                trace = Bar(
                    name=col,
                    x=series.index,
                    y=series,
                    visible=True,
                    showlegend=True,
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
                    # marker=dict(
                    #     color=self.colors[col],
                    #     opacity=0.85 if col in ['시가총액', '영업이익'] else 0.9
                    # ),
                    meta=[int2won(x) for x in series],
                    texttemplate="%{meta}원",
                    hovertemplate=col + ": %{meta}원<extra></extra>"
                )
            fig.add_trace(secondary_y=secondary_y, trace=trace)
        fig.update_layout(
            title=f"{self.title}",
            barmode="stack",
            **kwargs
        )
        fig.update_yaxes(row=1, col=1, secondary_y=False, patch={"title": "[억원]"})
        fig.update_yaxes(row=1, col=1, secondary_y=True, patch={"title": "영업이익률 [%]"})
        return fig
