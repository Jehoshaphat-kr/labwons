from labwons.asset.kr.etf.fetch import fetch
from pandas import concat, DataFrame
from plotly.graph_objects import Pie, Figure


class components(object):

    def __init__(self, src:fetch):
        self.src = src
        data = src.components
        data = data[data.비중 >= 0.1].copy()
        if len(data) > 12:
            data = data.head(12)

        total = data["비중"].sum()
        if total < 100:
            adder = DataFrame(index=["000000"], data=[{"이름":"기타", "비중":100-total}])
            data = concat(objs=[data, adder], axis=0)
        self.data = data
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

    @property
    def trace(self) -> Pie:
        return Pie(
            labels=self.data.이름,
            values=self.data.비중,
            meta=self.data.index,
            textinfo='label+percent',
            insidetextorientation='radial',
            hovertemplate="%{label}(%{meta})<br>%{percent}<extra></extra>"
        )

    def figure(self, **kwargs) -> Figure:
        fig = Figure()
        fig.add_trace(trace=self.trace)
        fig.update_layout(title=f"{self.src.name}({self.src.ticker}): 구성 상위 비중 12 종목")
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

    comp = components(test)
    print(comp)
    comp()
