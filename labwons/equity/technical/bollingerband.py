from labwons.common.config import PATH
from labwons.equity.refine import _calc
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from pandas import DataFrame
import numpy as np


class bollingerband(DataFrame):
    def __init__(self, base:_calc):
        baseData = base.getOhlcv()
        typical = (baseData.high + baseData.low + baseData.close) / 3
        baseData['typical'] = typical
        baseData['middle'] = typical.rolling(window=20).mean()
        baseData['stdev'] = typical.rolling(window=20).std()
        baseData['upperband'] = baseData.middle + 2 * baseData.stdev
        baseData['uppertrend'] = baseData.middle + baseData.stdev
        baseData['lowertrend'] = baseData.middle - baseData.stdev
        baseData['lowerband'] = baseData.middle - 2 * baseData.stdev
        baseData['width'] = 100 * (4 * baseData.stdev) / baseData.middle
        baseData['pctb'] = (
                (baseData.typical - baseData.lowerband) / (baseData.upperband - baseData.lowerband)
        ).where(baseData.upperband != baseData.lowerband, np.nan)
        super().__init__(
            index=baseData.index,
            columns=baseData.columns,
            data=baseData.values
        )
        self._base_ = base
        return

    def __call__(self, col:str):
        return self.trace(col)

    def trace(self, col:str) -> go.Scatter:
        basis = self[col].dropna()
        unit = '%' if col == 'width' else '' if col == 'pctb' else self._base_.unit
        trace = go.Scatter(
            name=col,
            x=basis.index,
            y=basis,
            visible=True,
            showlegend=True,
            mode='lines',
            xhoverformat='%Y/%m/%d',
            yhoverformat='.2f',
            hovertemplate=col + "<br>%{y}" + unit + " @%{x}<extra></extra>"
        )
        if col.endswith('band'):
            trace.name = 'x2 Band'
            trace.line = dict(dash='dash', color='magenta')
            trace.showlegend = True if col.startswith('upper') else False
            trace.legendgroup = '_band'
        if col.endswith('trend'):
            trace.name = 'x1 Trend'
            trace.line = dict(dash='dot', color='maroon')
            trace.showlegend = True if col.startswith('upper') else False
            trace.legendgroup = f'_trend'
        return trace

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=4,
            cols=1,
            shared_xaxes=True,
            row_width=[0.2, 0.2, 0.1, 0.5],
            vertical_spacing=0.01
        )
        fig.add_traces(
            data=[
                self._base_.ohlcv('candle'),
                self._base_.ohlcv('volume'),
                self.trace('middle'),
                self.trace('upperband'),
                self.trace('uppertrend'),
                self.trace('lowertrend'),
                self.trace('lowerband'),
                self.trace('width'),
                self.trace('pctb')
            ],
            rows=[1, 2, 1, 1, 1, 1, 1, 3, 4],
            cols=[1, 1, 1, 1, 1, 1, 1, 1, 1]
        )
        fig.update_layout(
            title=f"{self._base_.name}({self._base_.ticker}) Bollinger-Band",
            plot_bgcolor="white",
            legend=dict(tracegroupgap=5),
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
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            xaxis3=dict(
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            xaxis4=dict(
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
                title=f"[{self._base_.unit}]",
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
            ),
            yaxis3=dict(
                title='[%]',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            yaxis4=dict(
                title='[%b]',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.5,
                mirror=False,
                autorange=True
            ),
        )
        return fig

    def show(self):
        self.figure().show()
        return

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{self._base_.path}/B-BAND.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return
