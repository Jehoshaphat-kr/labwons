from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.common.tools import int2won
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
import pandas as pd


class soundness(baseDataFrameChart):

    factors = ["시가총액", "자본총계", "부채총계", "자산총계", "영업이익", "부채비율"]
    colors = {
        "시가총액": "#BDCDCD",
        "자본총계": "lightgreen",
        "부채총계": "red",
        "영업이익": "royalblue"
    }
    Q = pd.DataFrame()
    def __init__(self, base:fetch):
        """
        Soundness
        :return:
        """
        annual = base.annualStatement[self.factors]
        self.Q = baseDataFrameChart(base.quarterStatement[self.factors])
        super().__init__(
            data=annual,
            name='FINANCIAL-SOUNDNESS',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='%',
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

    def figure(self) -> go.Figure:
        fig = Chart.r1c1sy1(x_title='기말')
        # for n, obj in enumerate([self, self.Q]):
        for n, obj in enumerate([self]):
            visible = False if n else True
            for col in self.factors:
                secondary_y = False
                if col.endswith('율'):
                    trace = obj(col, 'lineXY', form=',.2f', unit='%', visible=visible, hovertemplate=col + ": %{y}%<extra></extra>")
                    secondary_y = True
                elif col.startswith("자산"):
                    trace = obj(
                        col, 'barXY',
                        y=[0] * len(self[col].dropna()),
                        showlegend=False,
                        base=None,
                        width=0.4,
                        offset=0.0,
                        meta=[int2won(x) for x in self[col].dropna()],
                        texttemplate = "총 자산: %{meta}원",
                        textposition = "outside",
                        hoverinfo='none',
                        hovertemplate=None,
                    )
                else:
                    trace = obj(
                        col, 'barXY',
                        base=0 if col == "시가총액" else None,
                        width=0.4,
                        offset=-0.4 if col == "시가총액" else 0.0,
                        visible=False if n else 'legendonly' if col == '영업이익' else True,
                        marker=dict(
                            color=self.colors[col],
                            opacity=0.8 if col == '영업이익' else 0.9
                        ),
                        meta=[int2won(x) for x in self[col].dropna()],
                        texttemplate="%{meta}원",
                        hovertemplate=col + ": %{meta}원<extra></extra>"
                    )
                fig.add_trace(secondary_y=secondary_y, trace=trace)

        fig.update_layout(
            title=f"<b>{self.subject}</b> : {self.name} (Annual)",
            barmode='stack',
            # updatemenus=[
            #     dict(
            #         direction="down",
            #         active=0,
            #         xanchor='left', x=0.0,
            #         yanchor='bottom', y=1.0,
            #         buttons=self.buttons
            #     )
            # ],
        )
        fig.update_yaxes(secondary_y=True, patch={"title": "부채율 [%]"})
        fig.update_yaxes(secondary_y=False, patch={"title": "[억원]"})
        return fig
