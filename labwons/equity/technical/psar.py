from labwons.equity.refine import _refine
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from pandas import DataFrame
import numpy as np


class psar(DataFrame):
    __upsides = list()
    __downsides = list()
    def __init__(self, base:_refine):
        COLUMNS = dict(
            trend_psar_up='up',
            trend_psar_down='down',
            trend_psar_up_indicator='*up',
            trend_psar_down_indicator='*down'
        )
        baseData = base.calcTA()[COLUMNS.keys()].rename(columns=COLUMNS)
        super().__init__(
            index=baseData.index,
            columns=baseData.columns,
            data=baseData.values
        )
        self['*up'] = (self['*up'] * self['up']).replace(0.0, np.nan)
        self['*down'] = (self['*down'] * self['down']).replace(0.0, np.nan)
        self._base_ = base
        return

    def __call__(self, col:str):
        return self.trace(col)

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

    # psar = test.ohlcv.join(test.psar, how='left')
    # psar.index.name = 'date'
    # psar.reset_index(inplace=True)
    # mask_up = psar.Down.isna()
    # mask_dn = psar.Up.isna()
    #
    # filt_dn = psar[mask_dn]
    # groups_dn = filt_dn.groupby((mask_dn != mask_dn.shift()).cumsum())
    # for n, (g, v) in enumerate(groups_dn):
    # if n == len(groups_dn) - 1:
    #         last = v.copy()

    def trace(self, col:str) -> go.Scatter:
        basis = self[col].dropna()
        return go.Scatter(
            name=col.upper(),
            x=basis.index,
            y=basis,
            visible=True,
            showlegend=True,
            mode='markers',
            marker=dict(
                symbol="205" if col == '*up' else "206" if col == '*down' else "101",
                color='red' if col == '*up' else 'blue' if col == '*down' else 'green',
                size=10 if col.startswith('*') else 8
            ),
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate=col + "<br>%{y} " + self._base_.unit + " @%{x}<extra></extra>"
        )

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
                self.trace('up'),
                self.trace('down'),
                self.trace('*up'),
                self.trace('*down'),
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

    def show(self):
        self.figure().show()
        return

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{self._base_.path}/PSAR.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return

