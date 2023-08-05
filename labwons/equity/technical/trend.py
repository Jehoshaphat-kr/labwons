from labwons.equity.refine import _calc
from datetime import datetime, timedelta
from scipy.stats import linregress
from typing import Union
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import pandas as pd
import numpy as np


class trend(pd.DataFrame):
    def __init__(self, fetch:_calc):
        super().__init__()

        n = len(fetch.typical)
        self._fetch = fetch
        for i, name in [(0, 'A'), (int(n / 2), 'H'), (int(3 * n / 4), 'Q')]:
            self.add(fetch.typical.index[i], name=name)
        if n >= 3.5 * 262:
            self.add(fetch.typical.index[-1] - timedelta(3 * 365), name='3Y')
        if n >= 1.5 * 262:
            self.add(fetch.typical.index[-1] - timedelta(365), name='1Y')
        if n >= 262:
            self.add(fetch.typical.index[-1] - timedelta(183), name='6M')
        return

    def __call__(self, col:str):
        return self.trace(col)

    def _naming(self) -> str:
        n = 1
        while f"custom{str(n).zfill(2)}" in self.columns:
            n += 1
        return f"custom{str(n).zfill(2)}"

    def _time_format(self, start:Union[datetime, str], end:Union[datetime, str]=None) -> tuple:
        end = end if end else self._fetch.ohlcv.index[-1]
        if isinstance(end, str):
            end = datetime.strptime(end, "%Y%m%d")
        if isinstance(start, str):
            start = datetime.strptime(start, "%Y%m%d")
        return pd.Timestamp(start), pd.Timestamp(end)
        # _tf = pd.to_datetime([start, end])
        # return _tf[0], _tf[1]

    def _slice_by_date(self, start:Union[datetime, str], end:Union[datetime, str]=None) -> pd.Series:
        start, end = self._time_format(start, end)
        series = self._fetch.typical[
            (self._fetch.typical.index >= start.date()) & (self._fetch.typical.index <= end.date())
        ]
        series.index.name = 'date'
        series.name = 'data'
        return series.reset_index(level=0).copy()

    def _buttons(self) -> list:
        _buttons = list()
        for col in self.columns:
            dates = self[col].dropna().index
            count = (dates[-1] - dates[0]).days
            _buttons.append(dict(count=count, label=col, step="day", stepmode="backward"))
        return _buttons

    def add(self, start:Union[datetime, str], end:Union[datetime, str]=None, name:str=''):
        series = self._slice_by_date(start, end)
        xrange = (series['date'].diff()).dt.days.fillna(1).astype(int).cumsum()
        slope, intercept, _, __, ___ = linregress(x=xrange, y=series['data'])
        fitted = slope * xrange + intercept
        fitted.name = name if name else self._naming()
        fitted = pd.concat(objs=[series, fitted], axis=1)[['date', fitted.name]].set_index(keys='date')
        frm = pd.concat(objs=[self, fitted], axis=1)
        super().__init__(data=frm.values, index=frm.index, columns=frm.columns)
        return

    def flatten(self) -> pd.DataFrame:
        frm = pd.concat(objs=[self._fetch.typical, self], axis=1)
        objs = list()
        for col in self:
            series = 100 * (frm[frm.columns[0]] / frm[col] - 1)
            series.name = col
            objs.append(series)
        return pd.concat(objs=objs, axis=1)

    def trace(self, col:str, basis:pd.DataFrame=pd.DataFrame(), **kwargs) -> go.Scatter:
        if basis.empty:
            basis = self.copy()
        basis = basis[col].dropna()

        trace = go.Scatter(
            name=col,
            x=basis.index,
            y=basis,
            visible='legendonly',
            showlegend=True,
            mode='lines',
            line=dict(
                color='black',
                dash='dash',
                width=0.8
            ),
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate=col + "<br>%{y} " + self._fetch.unit + " @%{x}<extra></extra>"
        )
        for key in kwargs:
            if key in vars(go.Scatter).keys():
                setattr(trace, key, kwargs[key])
        return trace

    def bar(self, col:str, **kwargs) -> go.Bar:
        frm = pd.concat(objs=[self._fetch.typical, self[col]], axis=1)
        if self[col].min() <= 0:
            frm = frm - self[col].min() + 10
        ser = 100 * (frm[frm.columns[0]] / frm[frm.columns[1]] - 1).dropna()
        ser.name = col
        bar = go.Bar(
            name=col,
            x=ser.index,
            y=ser,
            visible=True,
            showlegend=False,
            marker=dict(
                color=['royalblue' if d <= 0 else 'red' for d in ser],
                opacity=1.0
            ),
            xhoverformat='%Y/%m/%d',
            yhoverformat='.2f',
            hovertemplate='%{x}<br>%{y}%<extra></extra>'
        )
        for key in kwargs:
            if key in vars(go.Bar):
                setattr(bar, key, kwargs[key])
        return bar

    def figure(self) -> go.Figure:
        return go.Figure(
            data=[self._fetch.typical()] + [self.trace(col) for col in self],
            layout=go.Layout(
                title=f"{self._fetch.name}({self._fetch.ticker}) Trend",
                plot_bgcolor="white",
                legend=dict(
                    orientation="h",
                    xanchor="right",
                    yanchor="bottom",
                    x=0.98,
                    y=1.02
                ),
                xaxis_rangeslider=dict(visible=False),
                xaxis_rangeselector=dict(
                    buttons=self._buttons()
                ),
                xaxis=dict(
                    title="Date",
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
                    title=f"[{self._fetch.unit}]",
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
        )

    def figure_flat(self, columns:list=None) -> go.Figure:
        columns = columns if columns else self.columns[:6]
        if len(columns) > 6:
            raise KeyError(f"The number of columns must be 6")

        fig = make_subplots(
            rows=3, cols=2,
            vertical_spacing=0.08, horizontal_spacing=0.04,
            y_title='[%]', x_title='Date',
            subplot_titles=columns
        )
        fig.add_traces(
            data=[self.bar(col) for col in columns],
            rows=[1, 1, 2, 2, 3, 3],
            cols=[1, 2, 1, 2, 1, 2]
        )
        fig.update_layout(
            title=f"{self._fetch.name}({self._fetch.ticker}) %Trend Diff.",
            plot_bgcolor="white",
        )
        fig.update_yaxes(
            dict(
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                zeroline=True,
                zerolinecolor='grey',
                zerolinewidth=0.8,
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            )
        )
        return fig

    # def figure(self, columns:list=None) -> go.Figure:
    #
    #     fig = self._fig_() if not columns else self._fig_flat(columns)
        # if base == 'price':
        #     kwargs = dict(
        #         data=[
        #             getattr(self._fetch, "typical")(),
        #             getattr(self._fetch, "ohlcv")("volume"),
        #         ] + [self.trace(col) for col in self.columns],
        #         rows=[1, 2] + [1] * len(self.columns),
        #         cols=[1, 1] + [1] * len(self.columns)
        #     )
        # elif base.lower().startswith('flat'):
        #     data = self.flatten()
        #     kwargs = dict(
        #         data=[
        #             getattr(self._fetch, "ohlcv")("volume"),
        #         ] + [
        #             self.trace(
        #                 data[col],
        #                 visible=True if not n else 'legendonly',
        #                 line=None
        #             ) for n, col in enumerate(data)
        #         ],
        #         rows=[2] + [1] * len(self.columns),
        #         cols=[1] + [1] * len(self.columns)
        #
        #     )
        # else:
        #     raise KeyError(f'Unknown data-key: {base}')
        # fig = make_subplots(
        #     rows=2,
        #     cols=1,
        #     shared_xaxes=True,
        #     row_width=[0.15, 0.85],
        #     vertical_spacing=0.01
        # )
        #
        # fig.add_traces(**kwargs)
        #     data=[
        #         getattr(self._fetch, "typical")(),
        #         getattr(self._fetch, "ohlcv")("volume"),
        #     ] + [self.trace(col) for col in self.columns],
        #     rows=[1, 2] + [1] * len(self.columns),
        #     cols=[1, 1] + [1] * len(self.columns)
        # )
        # fig.update_layout(
        #     title=f"{self._fetch.name}({self._fetch.ticker}) Trend",
        #     plot_bgcolor="white",
        #     legend=dict(
        #         orientation="h",
        #         xanchor="right",
        #         yanchor="bottom",
        #         x=0.98,
        #         y=1.02
        #     ),
        #     xaxis_rangeslider=dict(visible=False),
        #     xaxis_rangeselector=dict(
        #         buttons = self._buttons()
        #     ),
        #     xaxis=dict(
        #         title="Date",
        #         showgrid=True,
        #         gridwidth=0.5,
        #         gridcolor="lightgrey",
        #         showline=True,
        #         linewidth=1,
        #         linecolor="grey",
        #         mirror=False,
        #         autorange=True
        #     ),
        #     # xaxis2=dict(
        #     #     title="DATE",
        #     #     showgrid=True,
        #     #     gridwidth=0.5,
        #     #     gridcolor="lightgrey",
        #     #     showline=True,
        #     #     linewidth=1,
        #     #     linecolor="grey",
        #     #     mirror=False,
        #     #     autorange=True
        #     # ),
        #     yaxis=dict(
        #         title=f"[{self._fetch.unit}]",
        #         showgrid=True,
        #         gridwidth=0.5,
        #         gridcolor="lightgrey",
        #         showline=True,
        #         linewidth=1,
        #         linecolor="grey",
        #         mirror=False,
        #         autorange=True
        #     ),
        #     # yaxis2=dict(
        #     #     title=f"",
        #     #     showgrid=True,
        #     #     gridwidth=0.5,
        #     #     gridcolor="lightgrey",
        #     #     showline=True,
        #     #     linewidth=1,
        #     #     linecolor="grey",
        #     #     mirror=False,
        #     #     autorange=True
        #     # )
        # )
        # return fig

    def show(self, mode:str='unflat', columns:list=None):
        if mode == 'unflat':
            self.figure().show()
        else:
            self.figure_flat(columns).show()
        return

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{self._fetch.path}/TREND.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return

