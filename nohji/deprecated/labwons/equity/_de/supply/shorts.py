from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from nohji.deprecated.labwons.equity import fetch
from plotly import graph_objects as go


class shorts(baseDataFrameChart):
    colors = {'종가': 'royalblue', '공매도비중': 'brown', '대차잔고비중': 'red'}
    def __init__(self, base:fetch):
        data = getattr(base, '_fnguide').shortRatio.join(
            other=getattr(base, '_fnguide').shortBalance.drop(columns=["종가"]),
            how="left"
        )[list(self.colors.keys())]
        super().__init__(
            data=data,
            name='SHORT RATIO & BALANCE',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='KRW',
            ref=base
        )
        return

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r1c1sy1()
        for col in self:
            secondary_y = False if col == "종가" else True
            fig.add_trace(
                secondary_y=secondary_y,
                trace=self(
                    col, "lineTY", False,
                    visible="legendonly" if col == "대차잔고비중" else True,
                    showlegend=False if col == "종가" else True,
                    line=dict(
                        color=self.colors[col],
                        dash="solid" if col == "종가" else "dot"
                    ),
                    yhoverformat=',d' if col == '종가' else '.2f',
                    hovertemplate=col + ': %{y}' + ('KRW' if col == '종가' else '%') + '<extra></extra>'
                )
            )

        fig.update_layout(
            title=f"<b>{self.subject})</b> : {self.name}",
            **kwargs
        )
        fig.update_yaxes(title="종가 [KRW]", secondary_y=False)
        fig.update_yaxes(title="[%]", secondary_y=True)
        return fig
