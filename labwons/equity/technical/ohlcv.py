from labwons.common.basis import baseDataFrameChart, baseSeriesChart
from labwons.common.chart import Chart
from plotly import graph_objects as go
from pandas import DataFrame

class ohlcv(baseDataFrameChart):

    fig = None
    def __init__(self, base:DataFrame, **kwargs):
        super().__init__(
            data = base,
            name = "OHLCV",
            subject = f"{kwargs['name']}({kwargs['ticker']})",
            path = kwargs['path'],
            form = kwargs['dtype'],
            unit = kwargs['unit']
        )
        self.fig = None
        return

    def __call__(self, **kwargs) -> go.Candlestick:
        return self.candleStick(**kwargs)

    @property
    def o(self) -> baseSeriesChart:
        return baseSeriesChart(
            data=self['open'],
            name=f"{self.subject}(O)",
            subject=self.subject,
            path=self.path,
            form=self.form,
            unit=self.unit
        )

    @property
    def h(self) -> baseSeriesChart:
        return baseSeriesChart(
            data=self['high'],
            name=f"{self.subject}(H)",
            subject=self.subject,
            path=self.path,
            form=self.form,
            unit=self.unit
        )

    @property
    def l(self) -> baseSeriesChart:
        return baseSeriesChart(
            data=self['low'],
            name=f"{self.subject}(L)",
            subject=self.subject,
            path=self.path,
            form=self.form,
            unit=self.unit
        )

    @property
    def c(self) -> baseSeriesChart:
        return baseSeriesChart(
            data=self['close'],
            name=f"{self.subject}(C)",
            subject=self.subject,
            path=self.path,
            form=self.form,
            unit=self.unit
        )

    @property
    def v(self) -> baseSeriesChart:
        return baseSeriesChart(
            data=self['volume'],
            name=f"{self.subject}(V)",
            subject=self.subject,
            path=self.path,
            form=',d',
            unit=''
        )

    @property
    def t(self) -> baseSeriesChart:
        return baseSeriesChart(
            data=(self['low'] + self['high'] + self['close']) / 3,
            name=f"{self.subject}(T)",
            subject=self.subject,
            path=self.path,
            form=",.1f",
            unit=self.unit
        )

    def figure(self) -> go.Figure:
        if not self.fig:
            self.fig = Chart.r2c1nsy()
            self.fig.add_trace(row=1, col=1, trace=self())
            self.fig.add_trace(row=1, col=1, trace=self.t('lineTY', name='TP', visible='legendonly'))
            self.fig.add_trace(row=2, col=1, trace=self.v('barTY', name='거래량', showlegend=False))
            self.fig.update_layout(
                title=f"<b>{self.subject}</b> : {self.name}",
                yaxis_title=f"[{self.unit}]",
                yaxis2_title="Vol."
            )
        return self.fig

