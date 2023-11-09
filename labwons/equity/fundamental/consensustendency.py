from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.common.service.tools import int2won
from labwons.equity.fetch import fetch
import pandas as pd


class consensustendency(baseDataFrameChart):
    colors = {
        "매출실적" : "#9BC2E6",
        "매출전망" : "#BDD7EE",
        "영업이익실적" : "#A9D08E",
        "영업이익전망" : "#C6E0B4"
    }
    N = pd.DataFrame()
    def __init__(self, base: fetch):
        self.N = baseDataFrameChart(getattr(base, '_fnguide').consensusNextYear)
        super().__init__(
            data=getattr(base, '_serv').consensusThisYear,
            name='CONSENSUS - TENDENCY',
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
                "label": "당해 연말 기준",
                "method": "update",
                "args": [
                    {"visible": [True] * len(self.columns) + [False] * len(self.N.columns)},
                    {"title": f"<b>{self.subject}</b> : {self.name} (당해 연말 기준)"}
                ]
            },
            {
                "label": "내년 연말 기준",
                "method": "update",
                "args": [
                    {"visible": [False] * len(self.columns) + [True] * len(self.N.columns)},
                    {"title": f"<b>{self.subject}</b> : {self.name} (내년 연말 기준)"}
                ]
            }
        ]
        return buttons

    def figure(self, col:str='매출', **kwargs):
        cols = [c for c in self if c.startswith(col)]
        if not cols:
            raise KeyError(f"Not Found {col} in columns, Possible column = ['매출', '영업이익', 'EPS', 'PER']")

        fig = Chart.r1c1nsy()
        for n, obj in enumerate([self, self.N]):
            for c in cols:
                trace = obj(
                    c, 'lineTY',
                    visible=False if n else True,
                    line=dict(dash='dot' if c.endswith(')') else 'solid'),
                    meta=[int2won(x) for x in obj[c].dropna()] if col in ['매출', '영업이익'] else None,
                    texttemplate="%{meta}원" if col in ['매출', '영업이익'] else None,
                    hovertemplate=c + ": %{meta}원<extra></extra>"
                )
                fig.add_trace(trace=trace)
        fig.update_layout(
            title=f"<b>{self.subject}</b> : {self.name} (당해 연말 기준)",
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
        fig.update_xaxes(title="전망 일자")
        fig.update_yaxes(title="[억원]" if col in ['매출', '영업이익'] else '[%]')
        return fig

    def show(self, col:str='매출'):
        self.figure(col).show()
        return