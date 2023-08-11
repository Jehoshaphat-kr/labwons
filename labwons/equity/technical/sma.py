from labwons.common.basis import baseDataFrameChart
from labwons.equity.technical.ohlcv import ohlcv
from plotly import graph_objects as go
import pandas as pd

class sma(baseDataFrameChart):

    _ohlcvt_ = None
    _goldenCross_ = None
    def __init__(self, ohlcvt:ohlcv, **kwargs):
        DEFAULT_WINDOWS = [5, 10, 20, 60, 120, 200]
        DEFAULT_FRAME = pd.concat(objs={f'MA{w}D': self.add(ohlcvt.t, w) for w in DEFAULT_WINDOWS}, axis=1)

        super().__init__(frame=DEFAULT_FRAME, **kwargs)
        self._filename_ = 'SMA'
        self._ohlcvt_ = ohlcvt
        self._goldenCross_ = pd.DataFrame()
        return

    def __call__(self, col:str, **kwargs) -> go.Scatter:
        return self.line(
            col,
            visible='legendonly',
            line=dict(dash='dot', width=1.0)
        )

    @staticmethod
    def add(series:pd.Series, window:int) -> pd.Series:
        return series.rolling(window).mean()

    @property
    def goldenCross(self) -> pd.DataFrame:
        if self._goldenCross_.empty:
            df = pd.concat(
                objs={
                    's': self['MA5D'] - self['MA20D'],
                    'm': self['MA20D'] - self['MA60D'],
                    'l': self['MA60D'] - self['MA120D']
                }, axis=1
            )

            prev, short, mid, long = [], [], [], []
            for n, (date, s, m, l) in enumerate(df.itertuples()):
                if not n:
                    prev = [s, m, l]
                    continue

                if s * prev[0] < 0 < s:
                    short.append(date)
                if m * prev[1] < 0 < m:
                    mid.append(date)
                if l * prev[2] < 0 < l:
                    long.append(date)
                prev = [s, m, l]

            objs = {self._ohlcvt_.t.name: self._ohlcvt_.t.copy()}
            for dates, label in ((short, 'short'), (mid, 'mid'), (long, 'long')):
                objs[f'{label}Term'] = pd.Series(index=dates, data=[1] * len(dates))
            gc = pd.concat(objs=objs, axis=1)
            for label in gc.columns[1:]:
                gc[label] = gc[gc.columns[0]] * gc[label]
            self._goldenCross_ = gc.drop(columns=[self._ohlcvt_.t.name])
        return self._goldenCross_

    def figure(self, goldenCross:bool=True) -> go.Figure:
        fig = self._ohlcvt_.figure()
        fig.add_traces(
            data=[self(col) for col in self],
            rows=[1] * len(self.columns),
            cols=[1] * len(self.columns)
        )
        if goldenCross:
            data = self.goldenCross().copy()
            fig.add_traces(
                data=[self.scatter(col, data, marker=dict(symbol='triangle-up')) for col in data],
                rows=[1] * len(data.columns),
                cols=[1] * len(data.columns)
            )
        return fig