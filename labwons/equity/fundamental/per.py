from labwons.common.basis import baseSeriesChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
import pandas as pd


class per(baseSeriesChart):

    _meta = {
        "currentPE": "현재가 / (최근 결산 EPS)",
        "trailingPE": "현재가 / (최근 4분기 EPS 합)",
        "averagePE": "최근 5개년 결산 PER 평균",
        "forwardPE": "현재가 / (당해 추정 EPS)",
        "12MforwardPE": "현재가 / (12개월 선행 EPS)",
        "sectorPE": "(전일자 시가총액 합) / (최근 결산 당기순이익 합)",
        "totalAverage": "전체 평균"
    }
    def __init__(self, base:fetch):
        naver, fnguide = getattr(base, '_naver'), getattr(base, '_fnguide')

        price = base.ohlcv.c.values[-1]
        previousClose = fnguide.previousClose
        data = pd.Series({
            "currentPE": price * fnguide.trailingPE / previousClose,
            "trailingPE": naver.trailingPE,
            "averagePE": fnguide.annualOverview["PER"].values[:-1].mean(),
            "forwardPE": naver.estimatePE,
            "12MforwardPE": price * fnguide.forwardPE / previousClose,
            "sectorPE": fnguide.sectorPE
        })
        data["totalAverage"] = data.mean()
        # if base.language == "kor":
        #     pass

        super().__init__(
            data=data,
            name='PER',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='',
            ref=base
        )
        return

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r1c1nsy()
        fig.add_trace(self(mode='barXY'))
        return fig