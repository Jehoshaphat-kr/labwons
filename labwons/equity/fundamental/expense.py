from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.common.service.tools import int2won
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
import pandas as pd


class expense(baseDataFrameChart):
    colors = {
        "매출액": "#9BC2E6",
        "매출원가": "#9BC2E6",
        "판매비와관리비": "#9BC2E6",
        "영업이익": "#9BC2E6",
        "금융수익": "#9BC2E6",
        "금융원가": "#9BC2E6",
        "기타수익": "#9BC2E6",
        "기타비용": "#9BC2E6",
    #     "매출실적" : "#9BC2E6",
    #     "매출전망" : "#BDD7EE",
    #     "영업이익실적" : "#A9D08E",
    #     "영업이익전망" : "#C6E0B4"
    }

    def __init__(self, base: fetch):
        super().__init__(
            data=getattr(base, '_fnguide').annualProfitLoss[[self.colors.values()]],
            name='PROFIT EXPENSES',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='KRW',
            ref=base
        )
        self["원가비율"] = 100 * self["매출원가"] / self["매출액"]
        self["판관비율"] = 100 * self["판관비율"] / self["매출액"]
        self["영업이익율"] = 100 * self["영업이익"] / self["매출액"]
        return

    def figure(self) -> go.Figure:
        fig = Chart.r1c2nsy()

        return fig
