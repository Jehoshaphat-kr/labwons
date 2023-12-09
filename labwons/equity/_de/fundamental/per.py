from labwons.common.basis import baseSeriesChart
from labwons.common.chart import Chart
from labwons.equity._de.fetch import fetch
from plotly import graph_objects as go
import pandas as pd


class per(baseSeriesChart):

    _meta = {
        "current": "현재가 / (최근 결산 EPS)",
        "trailing": "현재가 / (최근 4분기 EPS 합)",
        "5Y average": "최근 5개년 결산 PER 평균",
        "forward": "현재가 / (당해 추정 EPS)",
        "12M forward": "현재가 / (12개월 선행 EPS)",
        "sector": "(전일자 시가총액 합) / (최근 결산 당기순이익 합)",
    }

    def __init__(self, base:fetch):
        naver, fnguide = getattr(base, '_naver'), getattr(base, '_fnguide')

        price = base.ohlcv.c.values[-1]
        previousClose = fnguide.previousClose
        data = pd.Series({
            "current": price * fnguide.trailingPE / previousClose,
            "trailing": naver.trailingPE,
            "5Y average": fnguide.annualOverview["PER"].values[:-1].mean(),
            "forward": naver.estimatePE,
            "12M forward": price * fnguide.forwardPE / previousClose,
            "sector": fnguide.sectorPE
        })
        data.fillna(0.0, inplace=True)
        # if base.language == "kor":
        #     pass

        super().__init__(
            data=data,
            name='PERs',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='',
            ref=base
        )
        return

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r1c1nsy()
        fig.add_trace(
            self(
                mode='barXY', drop=False,
                meta=list(self._meta.values()),
                marker=dict(
                    opacity=0.9,
                ),
                texttemplate="%{y:.2f}",
                hovertemplate="%{meta}<extra></extra>"
            )
        )
        annotation = [
            dict(x=x, y=1.0, text="<b>적자</b>", showarrow=False, font=dict(size=14)) for x in self.index if not self[x]
        ]
        fig.update_layout(
            title=f"<b>{self.subject}</b>: {self.name}",
            hovermode="closest",
            annotations=annotation,
            **kwargs
        )
        fig.update_yaxes(title="PER")
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()