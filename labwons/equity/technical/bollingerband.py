from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


class bollingerband(baseDataFrameChart):
    def __init__(self, base:fetch):
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

    def figure(self, **kwargs) -> go.Figure:
        fig = make_subplots(
            rows=4,
            cols=1,
            shared_xaxes=True,
            row_width=[0.12, 0.12, 0.1, 0.66],
            vertical_spacing=0.01
        )
        fig.add_traces(
            data=[
                self._base_.ohlcv('candle'),
                self._base_.ohlcv('volume'),
                self.line('middle'),
                self.line(
                    'upperband',
                    name='x2 Band',
                    line=dict(dash='dash', color='maroon'),
                    legendgroup='_band'
                ),
                self.line(
                    'uppertrend',
                    name='x1 Band',
                    line=dict(dash='dot', color='lightgreen'),
                    legendgroup='_trend'
                ),
                self.line(
                    'lowertrend',
                    showlegend=False,
                    line=dict(dash='dot', color='lightgreen'),
                    legendgroup='_trend'
                ),
                self.line(
                    'lowerband',
                    showlegend=False,
                    line=dict(dash='dash', color='maroon'),
                    legendgroup='_band'
                ),
                self.line(
                    'width',
                    hovertemplate="Width<br>%{y}% @%{x}<extra></extra>"
                ),
                self.line(
                    'pctb',
                    hovertemplate="%B<br>%{y} @%{x}<extra></extra>"
                )
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
                tickformat="%Y/%m/%d",
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
        for k, v in kwargs.items():
            if k in vars(go.Layout):
                fig.update_layout({k:v})
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()
        return
