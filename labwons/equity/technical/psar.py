from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from plotly.subplots import make_subplots

import numpy as np


class psar(baseDataFrameChart):
    __upsides = list()
    __downsides = list()
    def __init__(self, base:fetch):
        COLUMNS = dict(
            trend_psar_up='up',
            trend_psar_down='down',
            trend_psar_up_indicator='*up',
            trend_psar_down_indicator='*down'
        )
        super().__init__(frame=base.ta[COLUMNS.keys()].rename(columns=COLUMNS), **getattr(base, '_valid_prop'))

        self['*up'] = (self['*up'] * self['up']).replace(0.0, np.nan)
        self['*down'] = (self['*down'] * self['down']).replace(0.0, np.nan)
        self._base_ = base
        self._unit_ = 'KRW'
        self._form_ = '.2f'
        self._filename_ = 'PSAR'
        return

    @property
    def upsides(self) -> list:
        if not self.__upsides:
            copy = self.copy().reset_index()
            mask = copy['down'].isna()
            self.__upsides = [
                val.set_index(keys='date') for g, val in copy[mask].groupby((mask != mask.shift()).cumsum())
            ]
        return self.__upsides

    @property
    def downsides(self) -> list:
        if not self.__downsides:
            copy = self.copy().reset_index()
            mask = copy['up'].isna()
            self.__downsides = [
                val.set_index(keys='date') for g, val in copy[mask].groupby((mask != mask.shift()).cumsum())
            ]
        return self.__downsides

    # def trace(self, col:str) -> go.Scatter:
    #     basis = self[col].dropna()
    #     return go.Scatter(
    #         name=col.upper(),
    #         x=basis.index,
    #         y=basis,
    #         visible=True,
    #         showlegend=True,
    #         mode='markers',
    #         marker=dict(
    #             symbol="205" if col == '*up' else "206" if col == '*down' else "101",
    #             color='red' if col == '*up' else 'blue' if col == '*down' else 'green',
    #             size=10 if col.startswith('*') else 8
    #         ),
    #         xhoverformat="%Y/%m/%d",
    #         yhoverformat=".2f",
    #         hovertemplate=col + "<br>%{y} " + self._base_.unit + " @%{x}<extra></extra>"
    #     )

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            row_width=[0.15, 0.85],
            vertical_spacing=0.01
        )
        fig.add_traces(
            data=[
                self._base_.ohlcv('candle'),
                self._base_.ohlcv('volume'),
                self.scatter('up', marker=dict(symbol="circle-open", color="green", size=6)),
                self.scatter('down', marker=dict(symbol="circle-open", color="green", size=6)),
                self.scatter('*up', marker=dict(symbol="triangle-up", color="red", size=8)),
                self.scatter('*down', marker=dict(symbol="triangle-down", color="blue", size=8)),
            ],
            rows=[1, 2, 1, 1, 1, 1],
            cols=[1, 1, 1, 1, 1, 1]
        )
        fig.update_layout(
            title=f"{self._base_.name}({self._base_.ticker}) PSAR",
            plot_bgcolor="white",
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
            )
        )
        return fig

