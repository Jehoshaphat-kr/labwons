from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.common.service.tools import int2won
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
import pandas as pd


class consensusprofit(baseDataFrameChart):
    colors = {
        "매출실적" : "#9BC2E6",
        "매출전망" : "#BDD7EE",
        "영업이익실적" : "#A9D08E",
        "영업이익전망" : "#C6E0B4"
    }
    Q = pd.DataFrame()
    def __init__(self, base: fetch):
        self.Q = baseDataFrameChart(getattr(base, '_fnguide').consensusQuarterProfit)
        super().__init__(
            data=getattr(base, '_serv').consensusAnnualProfit,
            name='CONSENSUS - PROFIT',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='KRW',
            ref=base
        )
        return

    @property
    def buttons(self) -> list:
        buttons = [
            {
                "label": "Annual",
                "method": "update",
                "args": [
                    {"visible": [True] * len(self.columns) + [False] * len(self.Q.columns)},
                    {"title": f"<b>{self.subject}</b> : {self.name} (Annual)"}
                ]
            },
            {
                "label": "Quarter",
                "method": "update",
                "args": [
                    {"visible": [False] * len(self.columns) + [True] * len(self.Q.columns)},
                    {"title": f"<b>{self.subject}</b> : {self.name} (Quarter)"}
                ]
            }
        ]
        return buttons

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r1c1nsy()
        for n, obj in enumerate([self, self.Q]):
            for col in obj:
                trace = obj(
                    col,
                    'barXY',
                    visible=False if n else True,
                    marker=dict(color=self.colors[col]),
                    meta=[int2won(x) for x in obj[col].dropna()],
                    texttemplate="%{meta}원",
                    hovertemplate=col + ": %{meta}원<extra></extra>"
                )
                fig.add_trace(trace=trace)
        fig.update_layout(
            title=f"<b>{self.subject}</b> : {self.name} (Annual)",
            updatemenus=[
                dict(
                    direction="down",
                    active=0,
                    xanchor='left', x=0.005,
                    yanchor='bottom', y=0.99,
                    buttons=self.buttons
                )
            ],
            **kwargs
        )
        fig.update_xaxes(title="기말")
        fig.update_yaxes(title="[억원]")
        return fig