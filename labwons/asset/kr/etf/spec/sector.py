from labwons.asset.kr.etf.fetch import fetch
from pandas import concat, DataFrame
from plotly.graph_objects import Bar, Figure


class sector(object):

    class _trace:
        def __init__(self, data:DataFrame):
            self.data = data
            return

        def __bar__(self, col:str) -> Bar:
            return Bar(
                name=col,
                x=self.data[col],
                y=self.data.index,
                visible=True,
                showlegend=True,
                orientation='h',
                hovertemplate=col + "/%{y}: %{x}%<extra></extra>"
            )
        @property
        def market(self) -> Bar:
            return self.__bar__(self.data.columns[-1])

        @property
        def etf(self) -> Bar:
            return self.__bar__(self.data.columns[0])


    def __init__(self, src:fetch):
        self.src = src
        self.data = src.sectorWeights.iloc[::-1].replace("", 0.0).fillna(0.0)
        self.trace = self._trace(self.data)
        return

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getattr__(self, item:str):
        if hasattr(self.data, item):
            return getattr(self.data, item)
        if item in dir(self):
            raise AttributeError

    def __getitem__(self, item:str):
        return self.data[item]

    def figure(self, **kwargs) -> Figure:
        fig = Figure(data=[self.trace.etf, self.trace.market])
        fig.update_layout(
            title=f"{self.src.name}({self.src.ticker}): 섹터 구성",
            plot_bgcolor="white",
            legend={
                "orientation": "h",
                "xanchor": "right",
                "x": 1.0,
                "yanchor": "bottom",
                "y": 1.0,
            },
        )
        fig.update_xaxes(
            showgrid=True,
            gridcolor="lightgrey",
            zeroline=True,
            zerolinewidth=1.0,
            zerolinecolor="grey"
        )
        for key, val in kwargs.items():
            if hasattr(fig, key):
                setattr(fig, key, val)
        return fig


if __name__ == "__main__":


    test = fetch(
        # '102780'  # KODEX 삼성그룹
        # '114800' # KODEX 인버스
        '069500'  # KODEX 200
    )

    comp = sector(test)
    print(comp)
    comp()
