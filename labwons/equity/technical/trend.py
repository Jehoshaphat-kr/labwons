from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from datetime import timedelta
from scipy.stats import linregress
from plotly import graph_objects as go
import pandas as pd
import numpy as np


class _disparate(baseDataFrameChart):

    def __init__(self, data:pd.DataFrame, subject:str, path:str):
        objs = {}
        cols = data.columns.tolist()
        for col in cols[1:]:
            both = data[[cols[0], col]].dropna()
            if data.empty:
                objs[col] = pd.Series(name=col, dtype=float)
                continue
            objs[col] = (both[cols[0]] - both[col]) / (abs(both[cols[0]] - both[col]).sum() / len(both))

        super(_disparate, self).__init__(
            data=pd.concat(objs=objs, axis=1),
            name="TREND-DISPARATE",
            subject=subject,
            path=path,
            form='.4f',
            unit='',
        )
        return

    def figure(self) -> go.Figure:
        fig = Chart.r2c3nsy(subplot_titles=self.columns)
        for name, row, col in (('A', 1, 1), ('5Y', 1, 2), ('2Y', 1, 3), ('1Y', 2, 1), ('6M', 2, 2), ('3M', 2, 3)):
            if self[name].dropna().empty:
                fig.add_annotation(row=row, col=col, x=0.5, y=0.5, text="<b>No Data</b>", showarrow=False)
            else:
                fig.add_trace(row=row, col=col, trace=self(name, 'barTY', showlegend=False, marker={"color":'grey'}))
        fig.update_layout(title=f"<b>{self.subject}</b> : {self.name}")
        fig.update_yaxes(autorange=False, range=[1.1 * self.min().min(), 1.1 * self.max().max()])
        return fig


class trend(baseDataFrameChart):

    underlying = None
    def __init__(self, base:fetch):
        self.underlying = tp = base.ohlcv.t.copy()
        objs = [tp, self.reg(tp, 'A')]
        for yy in [5, 2, 1, 0.5, 0.25]:
            col = f"{yy}Y" if isinstance(yy, int) else f"{int(yy * 12)}M"
            date = tp.index[-1] - timedelta(int(yy * 365))
            data = pd.Series(name=col, index=tp.index) if tp.index[0] > date else self.reg(tp[tp.index >= date], col)
            objs.append(data)

        super().__init__(
            data=pd.concat(objs=objs, axis=1),
            name="TREND",
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            form='.1f',
            unit=base.unit,
            ref=base
        )
        return

    @staticmethod
    def reg(series:pd.Series, col:str='') -> pd.Series:
        if not series.index.name == 'date':
            raise IndexError
        col = col if col else series.name
        series = series.reset_index(level=0)
        xrange = (series['date'].diff()).dt.days.fillna(1).astype(int).cumsum()

        slope, intercept, _, _, _ = linregress(x=xrange, y=series[series.columns[-1]])
        fitted = slope * xrange + intercept
        fitted.name = col
        return pd.concat(objs=[series, fitted], axis=1).set_index(keys='date')[col]

    @property
    def intensity(self) -> pd.Series:
        objs = {}
        cols = self.columns.tolist()
        for col in cols[1:]:
            both = self[[cols[0], col]].dropna()
            if both.empty:
                objs[col] = np.nan
                continue
            objs[col] = (both[cols[0]][0] + both[col][-1] - both[col][0]) / both[cols[0]][0] - 1
        return pd.Series(data=objs, dtype=float)

    @property
    def disparate(self) -> baseDataFrameChart:
        return _disparate(data=self.copy(), subject=self.subject, path=self.path)

    def figure(self) -> go.Figure:
        fig = self.ref.ohlcv.figure()
        for col in self.columns[1:]:
            kwargs = dict(
                col=col,
                visible='legendonly',
                line=dict(
                    color='black',
                    dash='dash',
                    width=0.8
                )
            )
            fig.add_trace(row=1, col=1, trace=self(**kwargs))

        fig.update_layout(title=f"<b>{self.subject}</b> : {self.name}")
        fig.update_xaxes(row=1, col=1, patch={
            "rangeselector": {
                "buttons": [
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=2, label="2Y", step="year", stepmode="backward"),
                    dict(count=5, label="5Y", step="year", stepmode="backward"),
                    dict(step="all")
                ]
            }
        })
        return fig
