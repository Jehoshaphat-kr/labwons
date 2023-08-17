from typing import Union
from labwons.common.basis import baseDataFrameChart
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
        COLUMNS = dict(
            trend_macd = 'macd',
            trend_macd_signal = 'signal',
            trend_macd_diff = 'diff',
        )
        super().__init__(frame=base.ta[COLUMNS.keys()].rename(columns=COLUMNS), **getattr(base, '_valid_prop'))
        self._base_ = base
        self._unit_ = ''
        self._form_ = '.2f'
        self._filename_ = 'MACD'
        return

    def __call__(self, col:str) -> go.Scatter:
        return self.bar(col) if col == 'diff' else self.line(col)

    # def trace(self, col:str) -> Union[go.Scatter, go.Bar]:
    #     basis = self[col].dropna()
    #     if col in ['macd', 'signal']:
    #         return go.Scatter(
    #             name=col.upper(),
    #             x=basis.index,
    #             y=basis,
    #             visible=True,
    #             showlegend=True,
    #             mode='lines',
    #             line=dict(
    #                 color='royalblue' if col == 'macd' else 'red',
    #                 dash='solid' if col == 'macd' else 'dash'
    #             ),
    #             xhoverformat="%Y/%m/%d",
    #             yhoverformat=".2f",
    #             hovertemplate=col.capitalize() + "<br>%{y} @%{x}<extra></extra>"
    #         )
    #     else:
    #         return go.Bar(
    #             name='DIFF',
    #             x=basis.index,
    #             y=basis,
    #             marker=dict(
    #                 color='lightgrey',
    #             ),
    #             xhoverformat='%Y/%m/%d',
    #             yhoverformat='.2f',
    #             hovertemplate='Diff<br>%{y} @%{x}<extra></extra>'
    #         )

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
                self.line('macd', line=dict(color='royalblue')),
                self.line('signal', line=dict(color='red', dash='dash')),
                self.bar('diff', marker=dict(color='grey', opacity=0.8)),
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

