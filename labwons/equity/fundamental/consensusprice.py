from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go


class consensusprice(baseDataFrameChart):

    def __init__(self, base: fetch):
        super().__init__(
            data=getattr(base, '_fnguide').consensus,
            name='CONSENSUS - PRICE',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='KRW',
            ref=base
        )
        return

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r2c1nsy()
        fig.add_trace(row=1, col=1, trace=self('종가', form=',d'))
        fig.add_trace(row=1, col=1, trace=self('컨센서스', form=',d', line=dict(dash='dot', color='black')))
        fig.add_trace(row=2, col=1, trace=self('격차', unit='%'))

        fig.update_layout(title=f"<b>{self.subject}</b> : {self.name}", **kwargs)
        fig.update_xaxes(rangeselector=None)
        fig.update_yaxes(row=1, col=1, title='[KRW]')
        fig.update_yaxes(row=2, col=1, title='격차 [%]', zerolinewidth=1.8)
        return fig
