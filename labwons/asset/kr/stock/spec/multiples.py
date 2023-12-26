from labwons.asset.kr.stock.fetch import fetch
from labwons.common.charts import r2c2nsy
from pandas import concat, DataFrame, Series
from plotly.graph_objects import Scatter, Figure
from typing import Union, Iterable, Tuple


class _data_(object):

    def __init__(self, src:fetch):
        self.data = self.__reform__(src.benchmarkMultiples)
        self.title = f"<b>{src.name}({src.ticker})</b> : 벤치마크 배수 비교"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getattr__(self, item:str):
        if hasattr(self.data, item):
            return getattr(self.data, item)
        if not hasattr(self, item):
            raise AttributeError

    def __getitem__(self, item:Union[str, Iterable]):
        return self.data[item]

    def __iter__(self):
        return iter(self.data)

    @staticmethod
    def __reform__(data:Union[DataFrame, Series]) -> DataFrame:
        return data


class _line_(object):
    colors = ["royalblue", "orange", "green"]
    def __init__(self, data:_data_):
        self.data = data
        return

    def __call__(self, col:Tuple[str, str], **kwargs):
        return self.__line__(col, **kwargs)

    def __line__(self, col:Tuple[str, str], **kwargs) -> Scatter:
        data = self.data[col].dropna()
        yy, column = col
        name, ticker = tuple(column.split("_"))
        trace = Scatter(
            name=name,
            x=data.index,
            y=data,
            mode="lines",
            line={
                "dash": "solid" if ticker == self.data.ticker else "dash",
                "color": self.colors[self.data.columns.tolist().index(col) % self.nAsset]
            },
            connectgaps=True,
            visible=True if yy == "5Y" else False,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate=name.split("_")[0] + ": %{y}%<extra></extra>"
        )
        for key, value in kwargs.items():
            if hasattr(trace, key):
                setattr(trace, key, value)
        return trace


class returns(_data_):

    def __init__(self, src:fetch):
        super().__init__(src)
        self.T = _line_(self)
        return

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r2c2nsy(
            subplot_titles=[col[0] for n, col in enumerate(self) if not n % 3],
            vertical_spacing=0.1,
            horizontal_spacing=0.08,
            **kwargs
        )
        # for col in self.columns:
        #     fig.add_trace(trace=self.T(col))

        return fig


if __name__ == "__main__":

    test = fetch(
        # "005930" # SamsungElec
        # "000660" # SK hynix
        # "207940" # SAMSUNG BIOLOGICS
        # "005380" # HyundaiMtr
        # "005490"  # POSCO
        # "035420" # NAVER Corporation
        # "000270" # Kia Corporation
        "051910" # LG Chem, Ltd.
        # "006400" # Samsung SDI Co., Ltd.
        # "068270" # Celltrion, Inc.
        # "035720"  # Kakao Corp.
        # "028260" # Samsung C&T Corporation
        # "105560" # KB Financial Group Inc.
        # "012330" # Mobis
        # "055550" # Shinhan Financial Group Co., Ltd.
        # "066570" # LG Electronics Inc.
        # "032830" # Samsung Life Insurance Co., Ltd.
        # "096770" # SK Innovation Co., Ltd.
        # "003550" # LG Corp.
        # "015760" # Korea Electric Power Corporation
        # "017670" # SK Telecom Co.,Ltd
        # "316140" # Woori Financial Group Inc.

        # "359090"  # C&R Research
        # "042660"  # Daewoo Shipbuilding & Marine Engineering Co.,Ltd
        # "021080" # Atinum Investment
        # "130500" # GH Advanced Materials Inc.
        # "323280" # SHT-5 SPAC
    )

    comp = returns(test)
    print(comp)
    comp()
