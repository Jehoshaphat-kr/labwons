from nohji.util.chart import r1c1sy1
from nohji.asset.fundamental.shorts import data

from pandas import DataFrame, Series
from plotly.graph_objects import Figure, Scatter


class shorts:

    colors = {'종가': 'royalblue', '공매도비중': 'brown', '대차잔고비중': 'red'}

    def __init__(self, shortSell: DataFrame, shortBalance: DataFrame, meta: Series):
        if meta.country == "KOR":
            self.data = data.gen(shortSell, shortBalance)
        elif meta.country == "USA":
            self.data = data.gen(shortSell, shortBalance)
        else:
            raise AttributeError
        self.meta = meta
        self.title = f"{meta['name']}({meta.name}) : Shorts"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r1c1sy1()
        for col in self.data:
            secondary_y = False if col == "종가" else True
            fig.add_trace(
                secondary_y=secondary_y,
                trace=Scatter(
                    name=col,
                    x=self.data.index,
                    y=self.data[col],
                    visible="legendonly" if col == "대차잔고비중" else True,
                    showlegend=False if col == "종가" else True,
                    line={
                        "color":self.colors[col],
                        "dash":"solid" if col == "종가" else "dot"
                    },
                    yhoverformat=',d' if col == '종가' else '.2f',
                    hovertemplate=col + ': %{y}' + ('KRW' if col == '종가' else '%') + '<extra></extra>'
            ))

        fig.update_layout(title=f"{self.title}", **kwargs)
        fig.update_yaxes(title="종가 [KRW]", secondary_y=False)
        fig.update_yaxes(title="[%]", secondary_y=True)
        return fig
