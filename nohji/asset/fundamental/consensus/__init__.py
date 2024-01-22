from nohji.util.chart import r2c1nsy

from pandas import DataFrame, Series
from plotly.graph_objects import Figure, Scatter


class consensus:

    def __init__(self, consen:DataFrame, meta: Series):
        if meta.country == "KOR":
            self.data = consen.copy()
        elif meta.country == "USA":
            self.data = consen.copy()
        else:
            raise AttributeError
        self.meta = meta
        self.title = f"{meta['name']}({meta.name}) : Consensus"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r2c1nsy()
        fig.add_trace(
            row=1, col=1,
            trace=Scatter(
                name="종가",
                x=self.data.index,
                y=self.data["종가"],
                visible=True,
                showlegend=True,
                yhoverformat=",d",
                hovertemplate="종가: %{y}KRW<extra></extra>"
        ))
        fig.add_trace(
            row=1, col=1,
            trace=Scatter(
                name='컨센서스',
                x=self.data.index,
                y=self.data['컨센서스'],
                visible=True,
                showlegend=True,
                yhoverformat=",d",
                line={
                    "dash":'dot',
                    "color":'black'
                },
                hovertemplate="컨센서스: %{y}KRW<extra></extra>"
        ))
        fig.add_trace(
            row=2, col=1,
            trace=Scatter(
                name='격차',
                x=self.data.index,
                y=self.data["격차"],
                visible=True,
                showlegend=True,
                yhoverformat=".2f",
                hovertemplate="격차: %{y}%<extra></extra>"
        ))

        fig.update_layout(title=self.title, **kwargs)
        fig.update_xaxes(rangeselector=None)
        fig.update_yaxes(row=1, col=1, title='[KRW]')
        fig.update_yaxes(row=2, col=1, title='격차 [%]', zerolinewidth=2.0)
        return fig
