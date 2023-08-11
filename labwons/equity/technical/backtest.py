from labwons.common.basis import baseDataFrameChart
from labwons.equity.technical.ohlcv import ohlcv
from plotly.subplots import make_subplots
from typing import Union
import plotly.graph_objects as go
import pandas as pd


class backtest(baseDataFrameChart):
    DURATIONS = ['1M', '3M', '6M', '1Y']
    _signaled = pd.DataFrame()
    def __init__(self, ohlcvt:ohlcv, **kwargs):
        base = ohlcvt[['close', 'low', 'high']].copy()
        objs = {}
        for label, win in [('1M', 21), ('3M', 63), ('6M', 126), ('1Y', 252)]:
            data = {'date': [], 'Return': [], 'Avg.Return': [], 'Max': [], 'Min': []}
            for n in range(len(base) - win):
                roll = base.iloc[n: n + win]
                data['date'].append(roll.index[0])
                data['Return'].append(round(100 * (roll['close'][-1] / roll['close'][0] - 1), 2))
                data['Avg.Return'].append(round(100 * (roll['close'] / roll['close'][0] - 1).mean(), 2))
                data['Max'].append(round(100 * (roll['high'].max() / roll['close'][0] - 1), 2))
                data['Min'].append(round(100 * (roll['low'].min() / roll['close'][0] - 1), 2))
            objs[label] = pd.DataFrame(data).set_index(keys='date')
        super().__init__(pd.concat(objs=objs, axis=1), **kwargs)
        self._signaled = pd.DataFrame()
        return

    def addSignal(self, signal:pd.Series) -> pd.DataFrame:
        answer = self.copy()
        self._signaled = answer.loc[signal.dropna().index]
        return self._signaled

    def performance(self, col:str, dataframe:pd.DataFrame=pd.DataFrame()):
        frame = (dataframe if not dataframe.empty else self._signaled.copy())[col]
        trace = go.Scatter(
            name=col,
            x=frame.index,
            y=frame['Return'],
            mode='markers',
            customdata=frame['Return'],
            text=frame['Max'],
            meta=frame['Min'],
            error_y=dict(
                type='data',
                symmetric=False,
                array=frame['Max'] - frame['Return'],
                arrayminus=frame['Return'] - frame['Min']
            ),
            showlegend=False,
            xhoverformat='%Y/%m/%d',
            yhoverformat='.2f',
            hovertemplate='%{x}<br>Return: %{customdata}% (%{text}% / %{meta}%)<extra></extra>'
        )
        return trace

    def box(self, col:tuple, dataframe:pd.DataFrame=pd.DataFrame()) -> go.Box:
        series = (dataframe if not dataframe.empty else self._signaled.copy())[col]
        trace = go.Box(
            name=col[1],
            x=[col[1]] * len(series),
            y=series,
            showlegend=True if col[0] == '1M' else False,
            legendgroup=col[1],
            marker=dict(
                color={
                    'Return': 'green',
                    'Avg.Return': 'royalblue',
                    'Max': 'indianred',
                    'Min': 'cyan'}[col[1]]
            )
        )
        return trace

    def figure(self, mode:str='box'):
        if mode == 'box':
            data = [self.box(col) for col in self._signaled]
            rows = [1 if col[0] in ['1M', '3M'] else 2 for col in self._signaled]
            cols = [1 if col[0] in ['1M', '6M'] else 2 for col in self._signaled]
        elif mode == 'line':
            data = [self.performance(col) for col in self.DURATIONS]
            rows = [1, 1, 2, 2]
            cols = [1, 2, 1, 2]
        else:
            raise KeyError
        fig = make_subplots(
            rows=2, cols=2,
            vertical_spacing=0.08, horizontal_spacing=0.04,
            y_title='[%]', x_title='Date',
            subplot_titles=self.DURATIONS
        )
        fig.add_traces(
            data=data,
            rows=rows,
            cols=cols
        )
        fig.update_xaxes(
            tickformat='%Y/%m/%d',
            rangeslider = dict(visible=False)
        )
        return fig