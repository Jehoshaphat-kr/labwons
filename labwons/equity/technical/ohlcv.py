from labwons.common.basis import baseDataFrameChart, baseSeriesChart
from labwons.common.chart import Chart
from plotly import graph_objects as go
from pandas import DataFrame


class ohlcv(baseDataFrameChart):

    def __init__(self, base:DataFrame, **kwargs):
        super().__init__(
            data = base,
            name = "OHLCV",
            subject = f"{kwargs['name']}({kwargs['ticker']})",
            path = kwargs['path'],
            form = kwargs['form'],
            unit = kwargs['currency']
        )
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
        fig = Chart.r2c1nsy()
        fig.add_trace(row=1, col=1, trace=self())
        fig.add_trace(row=1, col=1, trace=self.t(name='TP', visible='legendonly', line={"color": "royalblue"}))
        fig.add_trace(row=2, col=1, trace=self.v('barTY', name='Vol.', showlegend=False, marker={"color": "grey"}))
        fig.update_layout(title=f"<b>{self.subject}</b> : {self.name}")
        fig.update_yaxes(row=1, col=1, patch={"title" : f"[{self.unit}]"})
        fig.update_yaxes(row=2, col=1, patch={"title" : "Vol."})
        fig.update_xaxes(patch={"autorange" : False, "range" : [self.index[0], self.index[-1]]})
        return fig

    @property
    def continuousDays(self):
        data = self.t.values
        cntr = 1
        while data[-(cntr + 1)] == data[-cntr]:
            cntr += 1
        sign = -1 if data[-(cntr + 1)] > data[-cntr] else 1
        while True:
            _sign = -1 if data[-(cntr + 2)] > data[-(cntr + 1)] else 1
            if _sign == sign:
                cntr += 1
            else:
                break
        return sign * cntr
