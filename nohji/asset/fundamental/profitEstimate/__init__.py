from nohji.util.tools import int2won
from nohji.util.chart import r1c1nsy

from pandas import DataFrame, Series
from plotly.graph_objects import Bar, Figure


class profitEstimate:
    colors = {
        "매출실적" : "#9BC2E6",
        "매출전망" : "#BDD7EE",
        "영업이익실적" : "#A9D08E",
        "영업이익전망" : "#C6E0B4"
    }

    def __init__(self, estimation:DataFrame, meta:Series):
        if meta.country == "KOR":
            self.data = estimation
        elif meta.country == "USA":
            self.data = estimation
        else:
            raise AttributeError
        self.title = f"{meta['name']}({meta.name}) : 실적 전망"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    @property
    def buttons(self) -> list:
        buttons = [
            {
                "label": "연간",
                "method": "update",
                "args": [
                    {"visible": [True] * len(self.data.columns) + [False] * len(self.data.Q.columns)},
                    {"title": f"{self.title} (연간)"}
                ]
            },
            {
                "label": "분기",
                "method": "update",
                "args": [
                    {"visible": [False] * len(self.data.columns) + [True] * len(self.data.Q.columns)},
                    {"title": f"{self.title} (분기)"}
                ]
            }
        ]
        return buttons

    def figure(self, **kwargs) -> Figure:
        fig = r1c1nsy()
        for n, obj in enumerate([self.data.Y, self.data.Q]):
            for col in obj:
                series = obj[col]
                trace = Bar(
                    name=col,
                    x=series.index,
                    y=series,
                    visible=False if n else True,
                    marker={
                        "color": self.colors[col]
                    },
                    meta=[int2won(x) for x in obj[col]],
                    texttemplate="%{meta}원",
                    hovertemplate=col + ": %{meta}원<extra></extra>"
                )
                fig.add_trace(trace=trace)
        fig.update_layout(
            title=f"{self.title} (연간)",
            updatemenus=[
                dict(
                    direction="down",
                    active=0,
                    xanchor='left', x=0.005,
                    yanchor='bottom', y=0.99,
                    buttons=self.buttons
                )
            ],
            **kwargs
        )
        fig.update_xaxes(title="기말")
        fig.update_yaxes(title="[억원]")
        return fig