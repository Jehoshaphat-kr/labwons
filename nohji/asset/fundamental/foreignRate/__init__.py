from nohji.util.chart import r1c1sy1

from pandas import DataFrame, Series
from plotly.graph_objects import Figure, Scatter


class foreignRate:

    def __init__(self, foreignrate: DataFrame, meta: Series):
        if meta.country == "KOR":
            self.data = foreignrate.copy()
        elif meta.country == "USA":
            self.data = foreignrate.copy()
        else:
            raise AttributeError
        self.meta = meta
        self.title = f"{meta['name']}({meta.name}) : Foreign Rate"
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
                "label": "3개월",
                "method": "update",
                "args": [
                    {"visible": [True, True, False, False, False, False]},
                    {"title": f"{self.title} (3개월)"}
                ]
            },
            {
                "label": "1년",
                "method": "update",
                "args": [
                    {"visible": [False, False, True, True, False, False]},
                    {"title": f"{self.title} (1년)"}
                ]
            },
            {
                "label": "3년",
                "method": "update",
                "args": [
                    {"visible": [False, False, False, False, True, True]},
                    {"title": f"{self.title} (3년)"}
                ]
            }
        ]
        return buttons

    def figure(self, **kwargs) -> Figure:
        fig = r1c1sy1()
        for col in self.data:
            data = self.data[col].dropna().sort_index()
            unit = "KRW" if col[1] == "종가" else "%"
            fig.add_trace(
                secondary_y=False if col[1] == "종가" else True,
                trace=Scatter(
                    name=col[1],
                    x=data.index,
                    y=data,
                    visible=True if col[0] == '3M' else False,
                    showlegend=True,
                    yhoverformat=",d" if col[1] == "종가" else ".2f",
                    line={
                        "color": "royalblue" if col[1] == "종가" else "black",
                        "dash": "solid" if col[1] == "종가" else "dot"
                    },
                    hovertemplate=col[1] + ": %{y}" + unit + "<extra></extra>"
            ))

        fig.update_layout(
            title=f"{self.title} (3개월)",
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
        fig.update_yaxes(secondary_y=True, patch={"title": "외국인 비중 [%]"})
        fig.update_yaxes(secondary_y=False, patch={"title": "종가 [KRW]"})
        return fig
