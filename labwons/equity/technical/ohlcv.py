from labwons.common.basis import baseDataFrameChart, baseSeriesChart
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
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            row_width=[0.15, 0.85],
            vertical_spacing=0.01
        )
        fig.add_traces(data=[self('candle'), self('bar')], rows=[1, 2], cols=[1, 1])
        fig.update_layout(
            title=f"{self._dataName_}({self._ticker_}) {self._filename_}",
            plot_bgcolor="white",
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=0.98,
                y=1.02
            ),
            # legend=dict(tracegroupgap=5),
            xaxis_rangeslider=dict(visible=False),
            xaxis_rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=2, label="3Y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            xaxis=dict(
                title="",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            xaxis2=dict(
                title="DATE",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            yaxis=dict(
                title=f"[{self._unit_}]",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            yaxis2=dict(
                title=f"",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            )
        )
        return fig
