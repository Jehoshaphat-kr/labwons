from labwons.asset.kr.etf.fetch import fetch
from labwons.common.charts import r1c1nsy
from pandas import concat, DataFrame, Series
from plotly.graph_objects import Pie, Figure
from typing import Union


class _data_(object):

    def __init__(self, src:fetch):
        self.data = self.__reform__(src.components)
        self.title = f"{src.name}({src.ticker}): 구성 상위 비중 12 종목"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getattr__(self, item:str):
        if hasattr(self.data, item):
            return getattr(self.data, item)
        if not hasattr(self, item):
            raise AttributeError

    def __getitem__(self, item:str):
        return self.data[item]

    @staticmethod
    def __reform__(data:Union[DataFrame, Series]):
        data = data[data.비중 >= 0.1].copy()
        if len(data) > 12:
            data = data.head(12)

        total = data["비중"].sum()
        if total < 100:
            adder = DataFrame(index=["000000"], data=[{"이름": "기타", "비중": 100 - total}])
            data = concat(objs=[data, adder], axis=0)
        return data


class _line_(object):

    def __init__(self, data:_data_):
        self.data = data
        return

    def __call__(self, **kwargs):
        return self.__pie__(**kwargs)

    def __pie__(self, **kwargs) -> Pie:
        trace = Pie(
            labels=self.data.이름,
            values=self.data.비중,
            meta=self.data.index,
            textinfo='label+percent',
            insidetextorientation='radial',
            hovertemplate="%{label}(%{meta})<br>%{percent}<extra></extra>"
        )
        for key, value in kwargs.items():
            if hasattr(trace, key):
                setattr(trace, key, value)
        return trace

    @property
    def pie(self) -> Pie:
        return self()


class components(_data_):

    def __init__(self, src:fetch):
        super().__init__(src)
        self.T = _line_(self)
        return

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r1c1nsy(**kwargs)
        fig.add_trace(self.T.pie)
        fig.update_layout(
            title=self.title,
            legend=None
        )
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
