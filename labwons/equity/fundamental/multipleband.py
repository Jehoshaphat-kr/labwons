from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
import pandas as pd


class multipleband(baseDataFrameChart):

    PBR = pd.DataFrame()
    def __init__(self, base:fetch):
        """
        Multiple Bands
        :return:

        """
        src = getattr(base, '_serv')
        self.PBR = baseDataFrameChart(src.pbrBand)
        super().__init__(
            data=src.perBand,
            name='MULTIPLE-BAND',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='KRW',
            ref=base
        )
        return

    @property
    def buttons(self) -> list:
        return [
            dict(
                label='PER BAND',
                method='update',
                args=[
                    {'visible': [True, True, True, True, True, True, False, False, False, False, False, False]},
                    {"title": f"<b>{self.subject}</b> : {self.name} (PER)"}
                ]
            ),
            dict(
                label='PBR BAND',
                method='update',
                args=[
                    {'visible': [False, False, False, False, False, False, True, True, True, True, True, True]},
                    {"title": f"<b>{self.subject}</b> : {self.name} (PBR)"}
                ]
            )
        ]

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r1c1nsy()
        for n, obj in enumerate([self, self.PBR]):
            for col in obj:
                fig.add_trace(obj(
                    col, "lineTY", False,
                    showlegend=False,
                    visible=False if n else True,
                    line=dict(
                        color='black' if col == '종가' else None,
                        dash='solid' if col == '종가' else 'dash'
                    ),
                    yhoverformat=',d' if col == '종가' else '.2f',
                    unit='KRW'
                ))

        fig.update_layout(
            title=f"<b>{self.subject}</b> : {self.name} (PER)",
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
        fig.update_xaxes(title="DATE", rangeselector=None)
        fig.update_yaxes(title="[KRW]")
        return fig
