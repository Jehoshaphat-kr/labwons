from labwons.asset.kr.etf.fetch import fetch
from labwons.common.charts import r1c1nsy
from pandas import DataFrame, Series
from plotly.graph_objects import Bar, Figure
from typing import Union


class _data_(object):

    def __init__(self, src:fetch):
        self.data = self.__reform__(src.sectorWeights)
        self.title = f"{src.name}({src.ticker}): 섹터 구성"
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
        return data.iloc[::-1].replace("", 0.0).fillna(0.0)


class _line_(object):

    def __init__(self, data:_data_):
        self.data = data
        return

    def __call__(self, col:str, **kwargs) -> Bar:
        return self.__bar__(col, **kwargs)

    def __bar__(self, col:str, **kwargs) -> Bar:
        name = "Market" if col == "시장" else col
        trace = Bar(
            name=name,
            x=self.data[col],
            y=self.data.index,
            visible=True,
            showlegend=True,
            orientation='h',
            hovertemplate=name + ": %{x}%<extra></extra>",
        )
        for key, value in kwargs.items():
            if hasattr(trace, key):
                setattr(trace, key, value)
        return trace

    @property
    def etf(self) -> Bar:
        return self(self.data.columns[0], marker={"color":"#00CCFF", "opacity":0.9})

    @property
    def market(self) -> Bar:
        return self(self.data.columns[-1], marker={"color":"#98BF64", "opacity":0.9})



class sector(_data_):

    def __init__(self, src:fetch):
        super().__init__(src)
        self.T = _line_(self)
        return

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r1c1nsy(**kwargs)
        fig.add_trace(self.T.etf)
        fig.add_trace(self.T.market)
        fig.update_layout(
            title=self.title,
            hovermode="y unified"
        )
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
