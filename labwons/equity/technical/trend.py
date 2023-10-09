from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from datetime import datetime, timedelta
from scipy.stats import linregress
from typing import Union
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import pandas as pd


class trend(baseDataFrameChart):

    _base_ = None
    def __init__(self, base:fetch):
        """
        Trend line
        :param base : [_ohlcv] parent class "<class; ohlcv>"
        """

        objs = [self._regress(self._timeSlice(base.ohlcv.t, start), col) for col, start in self._timeSpan(base.ohlcv.t)]
        super().__init__(pd.concat(objs=objs, axis=1), **getattr(base, '_valid_prop'))
        self._filename_ = lambda x: f'TREND{"" if x == "unflat" else "_F"}'
        self._form_ = '.2f'
        self._base_ = base
        return

    def __call__(self, col:str):
        return self.line(col)

    @staticmethod
    def _timeSpan(series:pd.Series) -> list:
        sizeof, times = len(series), series.index
        # span = [('ALL', times[0])]
        span = []
        if sizeof >= 5 * 252 * 1.03:
            span.append(('5Y', times[-1] - timedelta(5 * 365)))
        if sizeof >= 3 * 252 * 1.03:
            span.append(('3Y', times[-1] - timedelta(3 * 365)))
        if sizeof >= 2 * 252 * 1.03:
            span.append(('2Y', times[-1] - timedelta(2 * 365)))
        if sizeof >= 1 * 252 * 1.03:
            span.append(('1Y', times[-1] - timedelta(365)))
        if sizeof >= 0.5 * 252 * 1.03:
            span.append(('6M', times[-1] - timedelta(183)))
        if sizeof >= 0.25 * 252 * 1.03:
            span.append(('3M', times[-1] - timedelta(91)))
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
        if not series.index.name == 'date':
            raise IndexError
        col = col if col else series.name
        series = series.reset_index(level=0)
        xrange = (series['date'].diff()).dt.days.fillna(1).astype(int).cumsum()

        slope, intercept, _, _, _ = linregress(x=xrange, y=series[series.columns[-1]])
        fitted = slope * xrange + intercept
        fitted.name = col
        return pd.concat(objs=[series, fitted], axis=1).set_index(keys='date')[col]

    def _naming(self) -> str:
        n = 1
        while f"custom{str(n).zfill(2)}" in self.columns:
            n += 1
        return f"custom{str(n).zfill(2)}"

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
            frm = pd.concat([self._base_.ohlcv.t, self[col]], axis=1).dropna()
            frm['sign'] = frm.apply(lambda row: -1 if row[self._base_.ohlcv.t.name] <= row[col] else 1, axis=1)
            residual = abs(frm[self._base_.ohlcv.t.name] - frm[col]).sum() / len(frm) # 평균 괴리 값
            objs[col] = frm['sign'] * abs(frm[self._base_.ohlcv.t.name] - frm[col]) / residual
        return pd.concat(objs=objs, axis=1)

    def strength(self) -> pd.Series:
        objs = dict()
        for col in self:
            frm = pd.concat([self._base_.ohlcv.t, self[col]], axis=1).dropna()
            base = frm[self._base_.ohlcv.t.name][0]
            objs[col] = (base + (frm[col][-1] - frm[col][0])) / base
        return pd.Series(data=objs)

    def gaps(self) -> pd.Series:
        data = self.flatten().iloc[-1]
        data.name = self._ticker_
        return data

    def backTest(self, window:int=252) -> pd.Series:
        date, data = [], []
        for n in range(0, len(self._base_.ohlcv.t) - window, 5):
            ser = self._base_.ohlcv.t[n : n + window]
            reg = self._regress(ser, col=str(n))
            fit = pd.concat([ser, reg], axis=1)
            if fit.empty:
                continue

            pr, td = fit[fit.columns[0]], fit[fit.columns[1]]
            basis = (pr - td) / (abs(pr - td).sum() / len(fit))
            factor = (basis[-3] / basis[-1]) * (pr[-2] / pr[-4])

            date.append(ser.index[-1])
            data.append(factor * basis[-1])
            # data['Residue'].append(res)
            # data['isUnderValued'].append(isUnderValued)
            # data['isDeValued'].append(isDeValued)
            # data['isRising'].append(isRising)
            # data['Signal'].append(pr[-1] * isUnderValued * isDeValued * isRising)
        return pd.Series(index=date, data=data, name='Score')

    def figure(self) -> go.Figure:
        data = [self._base_.ohlcv.t()]
        for col in self:
            trace = self.line(col)
            trace.visible = 'legendonly'
            trace.line = dict(color='black', dash='dash', width=0.8)
            data.append(trace)
        return go.Figure(
            data=data,
            layout=go.Layout(
                title=f"{self._base_.name}({self._base_.ticker}) Trend",
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
                    tickformat='%Y/%m/%d',
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
                    title=f"[{self._unit_}]",
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
            y_title='[x1 Average]', x_title='Date',
            subplot_titles=columns
        )
        fig.add_traces(
            data=data,
            rows=[1, 1, 2, 2, 3, 3][:len(columns)],
            cols=[1, 2, 1, 2, 1, 2][:len(columns)]
        )
        fig.update_layout(
            title=f"{self._base_.name}({self._base_.ticker}) %Trend Diff.",
            plot_bgcolor="white",
        )
        fig.update_xaxes(
            dict(
                tickformat='%Y/%m/%d',
            )
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
        filename = filename if filename else self._filename_(mode)
        plot(
            figure_or_data=fig,
            auto_open=False,
            filename=f'{self._path_}/{filename}.html'
        )
        return

