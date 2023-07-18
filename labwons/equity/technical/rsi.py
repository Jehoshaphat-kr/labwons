from labwons.common.config import PATH
from labwons.equity.refine import _refine
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from pandas import DataFrame
import numpy as np
import warnings

warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in scalar divide"
)
warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in cast"
)


class rsi(DataFrame):

    def __init__(self, base:_refine):
        COLUMNS = dict(
            momentum_rsi = 'rsi',
            momentum_stoch = 'stoch-osc',
            momentum_stoch_signal = 'stoch-osc-sig',
            momentum_stoch_rsi = 'stoch-rsi',
            momentum_stoch_rsi_k = 'stoch-rsi-k',
            momentum_stoch_rsi_d = 'stoch-rsi-d'
        )
        baseData = base.calcTA()[COLUMNS.keys()].rename(columns=COLUMNS)
        super().__init__(
            index=baseData.index,
            columns=baseData.columns,
            data=baseData.values
        )
        self._base_ = base
        return

    def __call__(self, col:str) -> go.Scatter:
        return self.trace(col)

    def trace(self, col:str) -> go.Scatter:
        basis = self[col].dropna()
        unit = '%' if col == 'rsi' else ''
        return go.Scatter(
            name=col.upper(),
            x=basis.index,
            y=basis,
            visible=True,
            showlegend=True,
            mode='lines',
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate=col + "<br>%{y} " + unit + " @%{x}<extra></extra>"
        )

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=5,
            cols=1,
            shared_xaxes=True,
            row_width=[0.15, 0.15, 0.15, 0.1, 0.45],
            vertical_spacing=0.01
        )
        fig.add_traces(
            data=[
                self._base_.ohlcv('candle'),
                self._base_.ohlcv('volume'),
                self.trace('rsi'),
                self.trace('stoch-osc'),
                self.trace('stoch-osc-sig'),
                self.trace('stoch-rsi'),
                self.trace('stoch-rsi-k'),
                self.trace('stoch-rsi-d'),
            ],
            rows=[1, 2, 3, 4, 4, 5, 5, 5],
            cols=[1, 1, 1, 1, 1, 1, 1, 1]
        )
        fig.add_hrect(y0=70, y1=100, line_width=0, fillcolor='red', opacity=0.2, row=3, col=1)
        fig.add_hrect(y0=0, y1=30, line_width=0, fillcolor='green', opacity=0.2, row=3, col=1)
        fig.add_hrect(y0=80, y1=100, line_width=0, fillcolor='red', opacity=0.2, row=4, col=1)
        fig.add_hrect(y0=0, y1=20, line_width=0, fillcolor='green', opacity=0.2, row=4, col=1)
        fig.add_hrect(y0=0.8, y1=1.0, line_width=0, fillcolor='red', opacity=0.2, row=5, col=1)
        fig.add_hrect(y0=0, y1=0.2, line_width=0, fillcolor='green', opacity=0.2, row=5, col=1)
        fig.update_layout(
            title=f"{self._base_.name}({self._base_.ticker}) RSI Family",
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
            filename=f'{self._base_.path}/RSI.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return



