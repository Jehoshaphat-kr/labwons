from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.common.service.tools import int2won
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
import pandas as pd


class profit(baseDataFrameChart):

    Q = pd.DataFrame()
    def __init__(self, base:fetch):
        """
        Performance
        :return:
        """
        src = getattr(base, '_fnguide')
        annualOverview = src.annualOverview
        quarterOverview = src.quarterOverview

        columns = annualOverview.columns.tolist()
        columns = columns[:columns.index('당기순이익') + 1]
        columns = [col for col in columns if not '(' in col and not col =='거래량'] + ['EPS(원)']
        annual = annualOverview[columns]
        quarter = quarterOverview[columns]
        self.Q = baseDataFrameChart(quarter)
        super().__init__(
            data=annual,
            name='FINANCIAL-PERFORMANCE',
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
                "label" : "Annual",
                "method" : "update",
                "args" : [
                    {"visible" : [True] * len(self.columns) + [False] * len(self.Q.columns)},
                    {"title" : f"<b>{self.subject}</b> : {self.name} (Annual)"}
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
        fig = Chart.r1c1sy1(x_title='기말')
        for n, obj in enumerate([self, self.Q]):
            for col in obj:
                if col.startswith('EPS'):
                    trace = obj(col, 'lineXY', form=',.1f', unit='원', visible=False if n else True)
                    secondary_y = True
                else:
                    trace = obj(
                        col,
                        'barXY',
                        visible=False if n else True,
                        marker=dict(
                            color="#9BC2E6" if col == self.columns[1] else "#A9D08E" if col == self.columns[2] else None,
                            opacity=0.85 if col == self.columns[0] else 1.0
                        ),
                        meta=[int2won(x) for x in obj[col].dropna()],
                        texttemplate="%{meta}원",
                        hovertemplate=col + ": %{meta}원<extra></extra>"
                    )
                    secondary_y = False
                fig.add_trace(secondary_y=secondary_y, trace=trace)
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
        fig.update_yaxes(secondary_y=True, patch={"title": "EPS [원]"})
        fig.update_yaxes(secondary_y=False, patch={"title": "[억원]"})
        return fig
