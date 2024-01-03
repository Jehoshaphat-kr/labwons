from nohji.asset.fetch import fetch
from nohji.util.brush import int2won
from nohji.util.chart import r1c1sy1
from nohji.asset.fundamental.profit import data

from plotly.graph_objects import Bar, Figure, Scatter


class profit:

    def __init__(self, _fetch:fetch):
        if _fetch.meta.country == "KOR":
            self.data = data.genKr(_fetch)
        elif _fetch.meta.country == "USA":
            self.data = data.genKr(_fetch)
        else:
            raise AttributeError
        self.title = f"{_fetch.meta['name']}({_fetch.meta.name}) : 실적"
        self.currency = _fetch.meta.currency
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
                "label" : "연간",
                "method" : "update",
                "args" : [
                    {"visible" : [True] * len(self.data.columns) + [False] * len(self.data.columns)},
                    {"title" : f"{self.title} (연간)"}
                ]
            },
            {
                "label": "분기",
                "method": "update",
                "args": [
                    {"visible": [False] * len(self.data.columns) + [True] * len(self.data.columns)},
                    {"title" : f"{self.title} (분기)"}
                ]
            }
        ]
        return buttons

    def figure(self, **kwargs) -> Figure:
        fig = r1c1sy1(x_title='기말')
        for n, df in enumerate([self.data.Y, self.data.Q]):
            for col in df:
                data = df[col].dropna()
                if col.startswith('EPS'):
                    trace = Scatter(
                        name=col,
                        x=data.index,
                        y=data,
                        mode="lines+text+markers",
                        visible=False if n else True,
                        showlegend=True,
                        yhoverformat=",d",
                        hovertemplate=col + ": %{y}원<extra></extra>"
                    )
                    secondary_y = True
                else:
                    trace = Bar(
                        name=col,
                        x=data.index,
                        y=data,
                        visible=False if n else True,
                        marker={
                            "color":"#9BC2E6" if col == self.data.columns[1] else "#A9D08E" if col == self.data.columns[2] else None,
                            "opacity":0.85 if col == self.data.columns[0] else 1.0
                        },
                        meta=[int2won(x) for x in data],
                        texttemplate="%{meta}원",
                        hovertemplate=col + ": %{meta}원<extra></extra>"
                    )
                    secondary_y = False
                fig.add_trace(secondary_y=secondary_y, trace=trace)
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
        fig.update_yaxes(secondary_y=True, patch={f"title": f"EPS [원]"})
        fig.update_yaxes(secondary_y=False, patch={f"title": f"[억원]"})
        return fig
