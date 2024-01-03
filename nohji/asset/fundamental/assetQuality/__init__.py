from nohji.asset.fetch import fetch
from nohji.util.brush import int2won
from nohji.util.chart import r1c1sy1
from nohji.asset.fundamental.assetQuality import data

from plotly.graph_objects import Bar, Figure, Scatter


class assetQuality:
    colors = {
        "시가총액": "royalblue",
        "자본총계": "lightgreen",
        "부채총계": "red",
        "영업이익": "cadetblue"
    }
    def __init__(self, _fetch:fetch):
        if _fetch.meta.country == "KOR":
            self.data = data.genKr(_fetch)
        elif _fetch.meta.country == "USA":
            self.data = data.genKr(_fetch)
        else:
            raise AttributeError
        self.title = f"{_fetch.meta['name']}({_fetch.meta.name}) : 자산"
        if not self.data.columns[1] in self.colors:
            self.colors[self.data.columns[1]] = "#9BC2E6"
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
            if col.endswith('율'):
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
            elif col.startswith("자산"):
                trace = Bar(
                    name=col,
                    x=series.index,
                    y=[0] * len(series),
                    visible=True,
                    showlegend=False,
                    marker={"opacity":0.0},
                    base=None,
                    width=0.4,
                    offset=0.0,
                    meta=[int2won(x) for x in series],
                    texttemplate="총 자산: %{meta}원",
                    textposition="outside",
                    hoverinfo='none',
                    hovertemplate=None,
                )
            else:
                trace = Bar(
                    name=col,
                    x=series.index,
                    y=series,
                    base=0 if col == "시가총액" else None,
                    width=0.4,
                    offset=-0.4 if col == "시가총액" else 0.0,
                    visible='legendonly' if col in self.data.columns[1:3] else True,
                    marker=dict(
                        color=self.colors[col],
                        opacity=0.8 if col == '영업이익' else 0.9
                    ),
                    meta=[int2won(x) for x in series],
                    texttemplate="%{meta}원",
                    hovertemplate=col + ": %{meta}원<extra></extra>"
                )
            fig.add_trace(secondary_y=secondary_y, trace=trace)

        fig.update_layout(title=f"{self.title} (연간)", barmode='stack', **kwargs)
        fig.update_yaxes(secondary_y=True, patch={f"title": f"부채율 [%]"})
        fig.update_yaxes(secondary_y=False, patch={f"title": f"[억원]"})
        return fig
