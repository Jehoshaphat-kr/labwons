from labwons.asset.kr.stock.fetch import fetch
from labwons.common.charts import r1c1sy1
from pandas import DataFrame, Series
from plotly.graph_objects import Scatter, Figure
from typing import Union, Iterable, Tuple


class _data_(object):

    def __init__(self, src:fetch):
        self.data = self.__reform__(src.foreignRate)
        self.title = f"<b>{src.name}({src.ticker})</b> : 외국인 비중"
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

    @staticmethod
    def __reform__(data:Union[DataFrame, Series]):
        return data


class _line_(object):

    def __init__(self, data:_data_):
        self.data = data
        return

    def __call__(self, col:Tuple[str, str], unit:str="", **kwargs):
        return self.__line__(col, unit, **kwargs)

    def __line__(self, col:Tuple[str, str], unit:str="", **kwargs) -> Scatter:
        data = self.data[col].dropna()
        trace = Scatter(
            name=col[1],
            x=data.index,
            y=data,
            mode="lines",
            line={
                "dash": "dot" if col[1] == "비중" else "solid",
                "color": "black" if col[1] == "비중" else "royalblue"
            },
            connectgaps=True,
            visible=True if col[0] == "3M" else False,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f" if col[1] == "비중" else ",d",
            hovertemplate=col[1] + ": %{y}" + unit + "<extra></extra>"
        )
        for key, value in kwargs.items():
            if hasattr(trace, key):
                setattr(trace, key, value)
        return trace

    @property
    def buttons(self) -> list:
        buttons = [
            {
                "label": "3개월",
                "method": "update",
                "args": [
                    {"visible": [True, True, False, False, False, False]},
                    {"title": f"{self.data.title} (3개월)"}
                ]
            },
            {
                "label": "1년",
                "method": "update",
                "args": [
                    {"visible": [False, False, True, True, False, False]},
                    {"title": f"{self.data.title} (1년)"}
                ]
            },
            {
                "label": "3년",
                "method": "update",
                "args": [
                    {"visible": [False, False, False, False, True, True]},
                    {"title": f"{self.data.title} (3년)"}
                ]
            }
        ]
        return buttons


class foreignRate(_data_):

    def __init__(self, src:fetch):
        super().__init__(src)
        self.T = _line_(self)
        return

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r1c1sy1(**kwargs)
        for col in self.columns:
            secondary_y = True if col[1] == "비중" else False
            unit = "%" if col[1] == "비중" else "KRW"
            fig.add_trace(row=1, col=1, secondary_y=secondary_y, trace=self.T(col, unit))
        fig.update_layout(
            title=f"{self.title} (3개월)",
            updatemenus=[
                dict(
                    direction="down",
                    active=0,
                    xanchor='left', x=0.005,
                    yanchor='bottom', y=0.99,
                    buttons=self.T.buttons
                )
            ],
        )
        fig.update_yaxes(secondary_y=True, patch={"title": "외국인 비중 [%]"})
        fig.update_yaxes(secondary_y=False, patch={"title": "종가 [KRW]"})
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

    comp = foreignRate(test)
    print(comp)
    comp()
