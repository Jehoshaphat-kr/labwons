from labwons.common.basis import baseDataFrameChart
from labwons.equity.ohlcv import _ohlcv
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


class bollingerband(baseDataFrameChart):
    def __init__(self, base:_ohlcv):
        frm = pd.DataFrame()
        frm['typical'] = base.ohlcv.t.copy()
        frm['middle'] = base.ohlcv.t.rolling(window=20).mean()
        frm['stdev'] = base.ohlcv.t.rolling(window=20).std()
        frm['upperband'] = frm.middle + 2 * frm.stdev
        frm['lowerband'] = frm.middle - 2 * frm.stdev
        frm['uppertrend'] = frm.middle + frm.stdev
        frm['lowertrend'] = frm.middle - frm.stdev
        frm['width'] = 100 * (4 * frm.stdev) / frm.middle
        frm['pctb'] = (
                (frm.typical - frm.lowerband) / (frm.upperband - frm.lowerband)
        ).where(frm.upperband != frm.lowerband, np.nan)

        super(bollingerband, self).__init__(frame=frm, **getattr(base, '_valid_prop'))
        self._base_ = base
        self._form_ = '.2f'
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
