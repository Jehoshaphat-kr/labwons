from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in scalar divide"
)
warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in cast"
)


class macd(baseDataFrameChart):

    def __init__(self, base:fetch):
        sampler = dict(
            trend_macd = 'macd',
            trend_macd_signal = 'signal',
            trend_macd_diff = 'diff',
        )
        super().__init__(
            data=base.ta[sampler.keys()].rename(columns=sampler),
            name="MACD",
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            form='.2f',
            unit=base.unit,
            ref=base
        )
        return

    def figure(self) -> go.Figure:
        fig = Chart.r3c1sy2()
        fig.add_trace(row=1, col=1, trace=self.ref.ohlcv())
        fig.add_trace(row=2, col=1, trace=self.ref.ohlcv.v('barTY', name='Vol.', showlegend=False, marker={"color": "grey"}))
        fig.add_trace(row=3, col=1, trace=self('macd', name='MACD'))
        fig.add_trace(row=3, col=1, trace=self('signal', name='Signal', line=dict(dash='dash')))
        fig.add_trace(row=3, col=1, trace=self('diff', 'barTY', name='Diff'), secondary_y=True)

        fig.update_layout(title=f"<b>{self.subject}</b> : {self.name}")
        fig.update_yaxes(row=1, col=1, patch={"title": f"[{self.unit}]"})
        fig.update_yaxes(row=2, col=1, patch={"title": f"Vol."})
        fig.update_yaxes(row=3, col=1, patch={"title": f"MACD [-]"})
        fig.update_yaxes(row=3, col=1, patch={"title": f"DIFF [-]"}, secondary_y=True)
        return fig

