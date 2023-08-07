from labwons.equity.ohlcv import _ohlcv
from datetime import datetime, timedelta
from scipy.stats import linregress
from typing import Union
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import pandas as pd


class _trend(pd.DataFrame):
    def __init__(self, fetch:_ohlcv):
        super().__init__()

        self._ohlcv = fetch
        self._typ = typ = fetch.typical.copy()
        n, objs = len(typ), list()
        for i, name in [(0, 'A'), (int(n / 2), 'H'), (int(3 * n / 4), 'Q')]:
            objs.append(self.add(typ.index[i], name=name))
        if n >= 3.5 * 262:
            objs.append(self.add(typ.index[-1] - timedelta(3 * 365), name='3Y'))
        if n >= 1.5 * 262:
            objs.append(self.add(typ.index[-1] - timedelta(365), name='1Y'))
        if n >= 262:
            objs.append(self.add(typ.index[-1] - timedelta(183), name='6M'))
        frm = pd.concat(objs=objs, axis=1)
        super().__init__(data=frm.values, index=frm.index, columns=frm.columns)
        return

    def __call__(self, col:str):
        return self.trace(col)

    def _naming(self) -> str:
        n = 1
        while f"custom{str(n).zfill(2)}" in self.columns:
            n += 1
        return f"custom{str(n).zfill(2)}"

    def _time_format(self, start:Union[datetime, str], end:Union[datetime, str]=None) -> tuple:
        end = end if end else self._ohlcv.ohlcv.index[-1]
        if isinstance(end, str):
            end = datetime.strptime(end, "%Y%m%d")
        if isinstance(start, str):
            start = datetime.strptime(start, "%Y%m%d")
        return pd.Timestamp(start), pd.Timestamp(end)

    def _slice_by_date(self, start:Union[datetime, str], end:Union[datetime, str]=None) -> pd.Series:
        start, end = self._time_format(start, end)
        series = self._typ[
            (self._typ.index >= start) & (self._typ.index <= end)
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

    def add(self, start:Union[datetime, str], end:Union[datetime, str]=None, name:str='') -> pd.Series:
        series = self._slice_by_date(start, end)
        xrange = (series['date'].diff()).dt.days.fillna(1).astype(int).cumsum()
        slope, intercept, _, __, ___ = linregress(x=xrange, y=series['data'])
        fitted = slope * xrange + intercept
        fitted.name = name if name else self._naming()
        fitted = pd.concat(objs=[series, fitted], axis=1)[['date', fitted.name]].set_index(keys='date')
        return fitted

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
            hovertemplate=col + "<br>%{y} " + self._ohlcv.unit + " @%{x}<extra></extra>"
        )
        for key in kwargs:
            if key in vars(go.Scatter).keys():
                setattr(trace, key, kwargs[key])
        return trace

    def bar(self, col:str, **kwargs) -> go.Bar:
        frm = pd.concat(objs=[self._typ, self[col]], axis=1)
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
            data=[self._ohlcv.typical()] + [self.trace(col) for col in self],
            layout=go.Layout(
                title=f"{self._ohlcv.name}({self._ohlcv.ticker}) Trend",
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
                    title=f"[{self._ohlcv.unit}]",
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
            rows=[1, 1, 2, 2, 3, 3][:len(columns)],
            cols=[1, 2, 1, 2, 1, 2][:len(columns)]
        )
        fig.update_layout(
            title=f"{self._ohlcv.name}({self._ohlcv.ticker}) %Trend Diff.",
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
            filename=f'{self._ohlcv.path}/TREND.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return

