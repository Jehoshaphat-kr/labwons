from labwons.common.basis import baseDataFrameChart, baseSeriesChart
from datetime import datetime, timedelta
from scipy.stats import linregress
from typing import Union
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import pandas as pd
import numpy as np


class trend(baseDataFrameChart):

    def __init__(self, typical:baseSeriesChart, **kwargs):
        """
        Trend line
        :param typical : [Series]
        :param kwargs  : [dict]
        """
        objs = [self._regress(self._timeSlice(typical, start), col) for col, start in self._timeSpan(typical)]
        super().__init__(pd.concat(objs=objs, axis=1), **kwargs)

        self._typ = typical
        for k in kwargs:
            if k in self._attr_:
                self._attr_[k] = kwargs[k]
        return

    def __call__(self, col:str):
        return self.line(col)

    @staticmethod
    def _timeSpan(series:pd.Series) -> list:
        sizeof, times = len(series), series.index
        span = [('ALL', times[0])]
        if sizeof >= 10 * 262 * 1.03:
            span.append(('10Y', times[-1] - timedelta(10 * 365)))
        if sizeof >= 5 * 262 * 1.03:
            span.append(('5Y', times[-1] - timedelta(5 * 365)))
        if sizeof >= 3 * 262 * 1.03:
            span.append(('3Y', times[-1] - timedelta(3 * 365)))
        if sizeof >= 1 * 262 * 1.03:
            span.append(('1Y', times[-1] - timedelta(365)))
        if sizeof >= 0.5 * 262 * 1.03:
            span.append(('6M', times[-1] - timedelta(183)))
        return span

    @staticmethod
    def _timeSlice(series:pd.Series, start:Union[str, int], end:Union[str, int]='') -> pd.Series:
        if isinstance(start, str):
            start = pd.Timestamp(datetime.strptime(start, "%Y%m%d"))
        elif isinstance(start, int):
            start = series.index[start]
        elif isinstance(start, datetime) or isinstance(start, pd.Timestamp):
            pass
        else:
            raise KeyError

        end = end if end else series.index[-1]
        if isinstance(end, str):
            end = pd.Timestamp(datetime.strptime(end, "%Y%m%d"))
        elif isinstance(end, int):
            end = series.index[end]
        elif isinstance(end, datetime) or isinstance(end, pd.Timestamp):
            pass
        else:
            raise KeyError
        return series[(series.index >= start) & (series.index <= end)].copy()

    @staticmethod
    def _regress(series:pd.Series, col:str='') -> pd.Series:
        col = col if col else series.name
        series = series.reset_index(level=0)
        xrange = (series['date'].diff()).dt.days.fillna(1).astype(int).cumsum()

        slope, intercept, _, _, _ = linregress(x=xrange, y=series[series.columns[-1]])
        fitted = slope * xrange + intercept
        fitted.name = col
        return pd.concat(objs=[series, fitted], axis=1)[['date', col]].set_index(keys='date')

    def _buttons(self) -> list:
        _buttons = list()
        for col in self.columns:
            dates = self[col].dropna().index
            count = (dates[-1] - dates[0]).days
            _buttons.append(dict(count=count, label=col, step="day", stepmode="backward"))
        return _buttons

    def flatten(self) -> pd.DataFrame:
        objs = dict()
        for col in self:
            frm = pd.concat([self._typ, self[col]], axis=1).dropna()
            residual = abs(frm[self._typ.name] - frm[col]).sum() / len(frm)
            objs[col] = 100 * abs(frm[self._typ.name] - frm[col]) / residual
            print(col, residual)
            # objs[col] = frm.apply(lambda r: np.nan if r[col] <= 0 else 100 * (r[self._typ.name]/r[col] - 1), axis=1)
        return pd.concat(objs=objs, axis=1)

    def append(self, start:Union[str, int], end:Union[str, int]=''):
        pass

    def _naming(self) -> str:
        n = 1
        while f"custom{str(n).zfill(2)}" in self.columns:
            n += 1
        return f"custom{str(n).zfill(2)}"

    def figure(self) -> go.Figure:
        data = [self._typ()]
        for col in self:
            trace = self.line(col)
            trace.visible = 'legendonly'
            trace.line = dict(color='black', dash='dash', width=0.8)
            data.append(trace)
        return go.Figure(
            data=data,
            layout=go.Layout(
                title=f"{self._attr_['name']}({self._attr_['ticker']}) Trend",
                plot_bgcolor="white",
                legend=dict(
                    orientation="h",
                    xanchor="right",
                    yanchor="bottom",
                    x=0.98,
                    y=1.02
                ),
                xaxis_rangeslider=dict(visible=False),
                xaxis_rangeselector=dict(buttons=self._buttons()),
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
                    title=f"[{self._attr_['unit']}]",
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
        frm = self.flatten().copy()
        columns = columns if columns else frm.columns[:6]
        if len(columns) > 6:
            raise KeyError(f"The number of columns must be 6")

        data = list()
        for col in columns:
            bar = self.bar(col, frm)
            bar.marker = dict(
                color=['royalblue' if v <= 0 else 'red' for v in frm[col].dropna()],
                opacity=0.9
            )
            data.append(bar)

        fig = make_subplots(
            rows=3, cols=2,
            vertical_spacing=0.08, horizontal_spacing=0.04,
            y_title='[%]', x_title='Date',
            subplot_titles=columns
        )
        fig.add_traces(
            data=data,
            rows=[1, 1, 2, 2, 3, 3][:len(columns)],
            cols=[1, 2, 1, 2, 1, 2][:len(columns)]
        )
        fig.update_layout(
            title=f"{self._attr_['name']}({self._attr_['ticker']}) %Trend Diff.",
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

    def save(self, mode:str='unflat', columns:list=None, filename:str=''):
        fig = self.figure() if mode == 'unflat' else self.figure_flat(columns)
        filename = filename if filename else f'TREND{"" if mode == "unflat" else "_F"}'
        plot(
            figure_or_data=fig,
            auto_open=False,
            filename=f'{self._attr_["path"]}/{filename}.html'
        )
        return

