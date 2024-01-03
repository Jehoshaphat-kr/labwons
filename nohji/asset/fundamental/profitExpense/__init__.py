from nohji.asset.fetch import fetch
from nohji.util.brush import int2won
from nohji.util.chart import r1c2nsy

from plotly.graph_objects import Bar, Figure, Pie


class products:

    def __init__(self, _fetch:fetch):
        if _fetch.meta.country == "KOR":
            self.data = _fetch.fnguide.products
        elif _fetch.meta.country == "USA":
            self.data = _fetch.fnguide.products
        else:
            raise AttributeError
        self.title = f"{_fetch.meta['name']}({_fetch.meta.name}) : 상품"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r1c2nsy(specs=[[{"type": 'bar'}, {"type": "pie"}]], subplot_titles=["연간", "최근"])
        for col in self.data:
            trace = Bar(
                name=col,
                x=self.data.index,
                y=self.data[col],
                visible=True,
                showlegend=False,
                marker={
                    "opacity":0.85
                },
            )
            fig.add_trace(row=1, col=1, trace=trace)
        fig.add_trace(
            row=1, col=2,
            trace=Pie(
                labels=self.data.iloc[-1].index,
                values=self.data.iloc[-1],
                showlegend=False,
                visible=True,
                automargin=True,
                opacity=0.85,
                textfont=dict(color='white'),
                textinfo='label+percent',
                insidetextorientation='radial',
                hoverinfo='label+percent',
            )
        )
        fig.update_layout(
            title=f"{self.title}",
            barmode="stack",

            **kwargs
        )
        fig.update_xaxes(row=1, col=1, patch={"title": "기말"})
        fig.update_yaxes(row=1, col=1, patch={"title": "비중 [%]"})
        return fig
