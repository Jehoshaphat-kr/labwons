from labwons.common.basis import baseDataFrameChart, baseSeriesChart
from labwons.common.chart import Chart
from typing import Union
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from pandas import DataFrame

class ohlcv(baseDataFrameChart):

    def __init__(self, base:DataFrame, **kwargs):
        super().__init__(frame=base, **kwargs)
        self._prop_['filename'] = 'OHLCV'
        return

    def __call__(self, key:str='candle', **kwargs) -> Union[go.Scatter, go.Bar]:
        if key.lower() in ['candle', 'ohlc', 'price']:
            trace = self.candle()
        elif key.lower() in ['volume', 'bar']:
            trace = self.bar('volume')
            trace.showlegend = False
            trace.marker = dict(
                color = self['volume'].pct_change().apply(lambda x: 'royalblue' if x <= 0 else 'red')
            )
        else:
            raise KeyError(f"Unknown parameter: {key}")
        return trace

    @property
    def o(self) -> baseSeriesChart:
        attrib = self._prop_.copy()
        attrib['name'] = f"{self._dataName_}(O)"
        return baseSeriesChart(self['open'], **attrib)

    @property
    def h(self) -> baseSeriesChart:
        attrib = self._prop_.copy()
        attrib['name'] = f"{self._dataName_}(H)"
        return baseSeriesChart(self['high'], **attrib)

    @property
    def l(self) -> baseSeriesChart:
        attrib = self._prop_.copy()
        attrib['name'] = f"{self._dataName_}(L)"
        return baseSeriesChart(self['low'], **attrib)

    @property
    def c(self) -> baseSeriesChart:
        attrib = self._prop_.copy()
        attrib['name'] = f"{self._dataName_}(C)"
        return baseSeriesChart(self['close'], **attrib)

    @property
    def v(self) -> baseSeriesChart:
        attrib = self._prop_.copy()
        attrib['name'] = f"{self._dataName_} Vol"
        attrib['form'] = ',d'
        return baseSeriesChart(self['volume'].astype(int), **attrib)

    @property
    def t(self) -> baseSeriesChart:
        attrib = self._prop_.copy()
        attrib['name'] = f"{self._dataName_}(T)"
        attrib['form'] = ".2f"
        return baseSeriesChart((self['low'] + self['high'] + self['close']) / 3, **attrib)

    def figure(self) -> go.Figure:
        fig = Chart.r2c1nsy
        fig.add_trace(self('price'), row=1, col=1)
        fig.add_trace(self('volume'), row=2, col=1)
        fig.update_layout(
            title=f"{self._dataName_}({self._ticker_}) {self._filename_}",
            yaxis_title=f"[{self._unit_}]",
            yaxis2_title="[Vol]"
        )
        return fig

