from labwons.asset.kr.stock.fetch import fetch
from labwons.common.charts import r2c1nsy
from pandas import DataFrame, Series
from plotly.graph_objects import Scatter, Figure
from typing import Union


class _data_(object):

    def __init__(self, src:fetch):
        self.data = self.__reform__(src.consensusPrice)
        self.title = f"{src.name}({src.ticker}): 주가 컨센서스"
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
        return data


class _line_(object):

    def __init__(self, data:_data_):
        self.data = data
        return

    def __call__(self, col:str, unit:str="", **kwargs):
        return self.__line__(col, unit, **kwargs)

    def __line__(self, col:str, unit:str="", **kwargs) -> Scatter:
        trace = Scatter(
            name=col,
            x=self.data.index,
            y=self.data[col],
            visible=True,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=",d",
            hovertemplate=col + ": %{y}" + unit + "<extra></extra>"
        )
        for key, value in kwargs.items():
            if hasattr(trace, key):
                setattr(trace, key, value)
        return trace

    @property
    def price(self) -> Scatter:
        return self("종가", "KRW")

    @property
    def consensus(self) -> Scatter:
        return self("컨센서스", "KRW")

    @property
    def gap(self) -> Scatter:
        return self("격차", "%", yhoverformat=".2f")


class consensus(_data_):

    def __init__(self, src:fetch):
        super().__init__(src)
        self.T = _line_(self)
        return

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r2c1nsy(**kwargs)
        fig.add_trace(row=1, col=1, trace=self.T.price)
        fig.add_trace(row=1, col=1, trace=self.T.consensus)
        fig.add_trace(row=2, col=1, trace=self.T.gap)
        fig.update_layout(
            title=self.title
        )
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
        # "051910" # LG Chem, Ltd.
        # "006400" # Samsung SDI Co., Ltd.
        # "068270" # Celltrion, Inc.
        "035720"  # Kakao Corp.
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

    comp = consensus(test)
    print(comp)
    comp()
