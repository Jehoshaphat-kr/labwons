from nohji.asset.fetch import fetch
from nohji.util.chart import r1c1nsy

from plotly.graph_objects import Figure, Scatter


class multipleBand:

    def __init__(self, _fetch:fetch):
        if _fetch.meta.country == "KOR":
            self.data = fetch.fnguide.multipleBand
        elif _fetch.meta.country == "USA":
            self.data = fetch.fnguide.multipleBand
        else:
            raise AttributeError
        self.title = f"{_fetch.meta['name']}({_fetch.meta.name}) : Multiple Band"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    @property
    def buttons(self) -> list:
        return [
            dict(
                label='PER BAND',
                method='update',
                args=[
                    {'visible': [True, True, True, True, True, True, False, False, False, False, False, False]},
                    {"title": f"{self.title} (PER)"}
                ]
            ),
            dict(
                label='PBR BAND',
                method='update',
                args=[
                    {'visible': [False, False, False, False, False, False, True, True, True, True, True, True]},
                    {"title": f"{self.title} (PBR)"}
                ]
            )
        ]

    def figure(self, **kwargs) -> Figure:
        fig = r1c1nsy(x_title='기말')
        for n, obj in enumerate([self.data["PER"], self.data["PBR"]]):
            for col in obj:
                fig.add_trace(
                    trace = Scatter(
                        name=col,
                        x=obj.index,
                        y=obj[col],
                        showlegend=False,
                        visible=False if n else True,
                        line={
                            "color": "black" if col == "종가" else None,
                            "dash": "solid" if col == "종가" else 'dash'
                        },
                        yhoverformat=",d" if col == "종가" else ".2f",
                        hovertemplate=col + ": %{y}KRW<extra></extra>"
                ))

        fig.update_layout(
            title=f"{self.title} (PER)",
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
        fig.update_xaxes(title="DATE", rangeselector=None)
        fig.update_yaxes(title="[KRW]")
        return fig
