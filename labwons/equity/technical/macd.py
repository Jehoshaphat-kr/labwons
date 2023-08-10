from typing import Union
from labwons.equity._deprecated import _calc
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


class macd(DataFrame):

    def __init__(self, base:_calc):
        COLUMNS = dict(
            trend_macd = 'macd',
            trend_macd_signal = 'signal',
            trend_macd_diff = 'diff',
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

    def trace(self, col:str) -> Union[go.Scatter, go.Bar]:
        basis = self[col].dropna()
        if col in ['macd', 'signal']:
            return go.Scatter(
                name=col.upper(),
                x=basis.index,
                y=basis,
                visible=True,
                showlegend=True,
                mode='lines',
                line=dict(
                    color='royalblue' if col == 'macd' else 'red',
                    dash='solid' if col == 'macd' else 'dash'
                ),
                xhoverformat="%Y/%m/%d",
                yhoverformat=".2f",
                hovertemplate=col.capitalize() + "<br>%{y} @%{x}<extra></extra>"
            )
        else:
            return go.Bar(
                name='DIFF',
                x=basis.index,
                y=basis,
                marker=dict(
                    color='lightgrey',
                ),
                xhoverformat='%Y/%m/%d',
                yhoverformat='.2f',
                hovertemplate='Diff<br>%{y} @%{x}<extra></extra>'
            )

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            row_width=[0.35, 0.15, 0.5],
            vertical_spacing=0.01
        )
        fig.add_traces(
            data=[
                self._base_.ohlcv('candle'),
                self._base_.ohlcv('volume'),
                self.trace('macd'),
                self.trace('signal'),
                self.trace('diff'),
            ],
            rows=[1, 2, 3, 3, 3],
            cols=[1, 1, 1, 1, 1]
        )
        fig.update_layout(
            title=f"{self._base_.name}({self._base_.ticker}) MACD",
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
                title='MACD [-]',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
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
            filename=f'{self._base_.path}/MACD.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return



