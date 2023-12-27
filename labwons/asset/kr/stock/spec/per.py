from labwons.asset.kr.stock.fetch import fetch
from labwons.common.charts import r1c1sy1
from pandas import DataFrame
from plotly.graph_objects import Scatter, Figure
from typing import Union, Iterable


class _data_(object):

    def __init__(self, src:fetch):
        self.data = self.__reform__(
            src.currentPrice,
            src.snapShot,
            src.multiplesTrailing,
            src.multiplesOutstanding,
            src.abstract
        )
        self.title = f"<b>{src.name}({src.ticker})</b> : PER"
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
    def __reform__(*args) -> DataFrame:
        curr, snapshot, trailing, outstanding, abstract = tuple(args)
        prev = snapshot.previousClose
        trailingEps, estimatedEps = trailing[["trailingEps", "estimateEps"]]
        fiscalEps, forwardEps = prev / outstanding[["fiscalPE", "forwardPE"]]
        sectorPE = outstanding.sectorPE
        abstractEps = abstract.iloc[:-1]["EPS(원)"].dropna()
        averageEps, nEps = abstractEps.mean(), len(abstractEps)

        index = ["최근 결산연도", f"{nEps}개년 평균", "4분기 합산", "당해 추정", "12개월 추정", "섹터 평균"]
        data = DataFrame(index=index)
        data["EPS"] = [fiscalEps, averageEps, trailingEps, estimatedEps, forwardEps, None]
        data["현재가"] = curr
        data["PER"] = data["현재가"] / data["EPS"]
        data.iloc[-1, -1] = sectorPE
        return data


class _line_(object):
    colors = {'종가': 'royalblue', '공매도비중': 'brown', '대차잔고비중': 'red'}
    def __init__(self, data:_data_):
        self.data = data
        return

    def __call__(self, col:str, unit:str="", **kwargs):
        return self.__line__(col, unit, **kwargs)

    def __line__(self, col:str, unit:str="", **kwargs) -> Scatter:
        data = self.data[col].dropna()
        trace = Scatter(
            name=col,
            x=data.index,
            y=data,
            mode="lines",
            line={
                "dash": "dot" if col.endswith("비중") else "solid",
                "color": self.colors[col]
            },
            connectgaps=True,
            visible="legendonly" if col.startswith("대차잔고") else True,
            showlegend=True,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f" if col.endswith("비중") else ",d",
            hovertemplate=col + ": %{y}" + unit + "<extra></extra>"
        )
        for key, value in kwargs.items():
            if hasattr(trace, key):
                setattr(trace, key, value)
        return trace

class per(_data_):

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
            secondary_y = True if col.endswith("비중") else False
            unit = "%" if col.endswith("비중") else "KRW"
            fig.add_trace(row=1, col=1, secondary_y=secondary_y, trace=self.T(col, unit))
        fig.update_layout(title=f"{self.title}")
        fig.update_yaxes(secondary_y=True, patch={"title": "비중 [%]"})
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

    comp = per(test)
    print(comp)
    # comp()
