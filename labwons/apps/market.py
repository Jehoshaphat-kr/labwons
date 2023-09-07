"""
This app is recommended to run on .ipynb file
"""
from labwons.common.metadata.metadata import MetaData
from labwons.equity.equity import Equity
from typing import Union, Tuple, List
from datetime import datetime
from pykrx import stock
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time


class Market(pd.DataFrame):
    _slot_ = {}
    _proc_ = True
    _tqdm_ = None
    def __init__(
        self,
        tickers:Union[Tuple, List, pd.Series, pd.Index],
        env:str='.ipynb',
        proc:bool=True,
        **kwargs
    ):
        loop = enumerate(tickers)
        if proc:
            if env.endswith('ipynb'):
                from tqdm.notebook import tqdm
            elif env.endswith('py'):
                from tqdm import tqdm
            else:
                raise ImportError('Unknown Environment!')
            self._tqdm_ = tqdm
            loop = enumerate(tqdm(tickers, desc='initialize...'))

        for n, t in loop:
            self._slot_[t] = Equity(t, **kwargs)
            if not n % 20:
                time.sleep(0.5)

        self._proc_ = proc
        meta = MetaData[MetaData.index.isin(tickers)][[
            'name', 'quoteType', 'market', 'korName'
        ]].copy()
        meta = meta[meta['market'] == 'KOR']
        caps = stock.get_market_cap_by_ticker(datetime.today().strftime("%Y%m%d"))[
            ['종가', '시가총액']
        ].rename(columns=dict(종가='close', 시가총액='marketCap'))
        meta = meta.join(caps, how='left')

        super().__init__(data=meta.values, index=meta.index, columns=meta.columns)
        return

    @staticmethod
    def _get_prop(__obj, __prop:str):
        props = __prop.split('.')
        for _prop in props:
            if not hasattr(__obj, _prop):
                raise AttributeError(f'No Such attribute: {__prop}')
            __obj = getattr(__obj, _prop)
        return __obj

    @staticmethod
    def normDist(series:pd.Series) -> pd.Series:
        m = series.mean()
        s = series.std()
        norm =  np.exp(-((series - m) ** 2) / (2 * s ** 2)) / (s * np.sqrt(2 * np.pi))
        return pd.Series(index=norm, data=series.values)

    def append(self, prop:str, column:str=''):
        operand = ''
        for optype in ['.iloc', '.loc', '.iat', '.at', '[']:
            if optype in prop:
                operand = optype
                break

        index = eval(prop[prop.find('[') + 1:prop.find(']')]) if operand else ''
        prop = prop[:prop.find('(')] if ')' in prop else prop
        loop = self._tqdm_(self._slot_.items()) if self._proc_ else self._slot_.items()
        data = []
        for ticker, slot in loop:
            if self._proc_:
                loop.set_description(desc=f'{ticker}... ')

            _data = self._get_prop(slot, prop)
            if len(slot.ohlcv) < 126:
                data.append(np.nan)
                continue
            if callable(_data):
                _data = _data()
            if operand:
                _data = _data[index] if operand == '[' else getattr(_data, operand[1:])[index]
            if isinstance(_data, pd.DataFrame) or isinstance(_data, pd.Series):
                raise TypeError(f'Append new market data must be 1x1 single data format, Not dataframe or series')
            data.append(_data)
        self[column if column else prop] = data
        return

    def scatter(self, x:str, y:str):
        fig = make_subplots(
            rows=2, cols=2,
            row_width=[0.12, 0.88],
            column_width=[0.05, 0.95],
            shared_xaxes='columns',
            shared_yaxes='rows',
            vertical_spacing=0,
            horizontal_spacing=0
        )
        self['size'] = np.log2(self['marketCap'].astype(float))
        self['size'] = (self['size'] - 6) / (30 - 6)
        fig.add_trace(
            row=1, col=2,
            trace=go.Scatter(
                x=self[x].astype(float), y=self[y].astype(float),
                mode='markers',
                marker=dict(
                    size=self['size'],
                    symbol='circle',
                    line=dict(width=0),
                    opacity=0.9
                ),
                showlegend=False,
                meta=self['name'] + '(' + self.index + ')',
                hovertemplate='%{meta}<br>x: %{x}<br>y: %{y}<extra></extra>'
            )
        )
        ynorm = self.normDist(self[y])
        fig.add_trace(
            row=1, col=1,
            trace=go.Scatter(
                x=ynorm.index,
                y=ynorm,
                mode='markers',
                showlegend=False,
                hovertemplate=y + ': %{y}<extra></extra>'
            )
        )
        xnorm = self.normDist(self[x])
        fig.add_trace(
            row=2, col=2,
            trace=go.Scatter(
                x=xnorm,
                y=xnorm.index,
                mode='markers',
                showlegend=False,
                hovertemplate=x +': %{x}<extra></extra>'
            )
        )
        fig.add_vline(x=self[x].mean(), row=1, col=2, line_width=0.5, line_dash="dash", line_color="black")
        fig.add_hline(y=self[y].mean(), row=1, col=2, line_width=0.5, line_dash="dash", line_color="black")
        fig.update_layout(
            title=f'Scatter x: {x} / y: {y}',
            plot_bgcolor='white',
            yaxis=dict(
                title=f'{y}',
                autorange=True,
                showticklabels=True,
                showgrid=True,
                gridcolor='lightgrey',
                gridwidth=0.5,
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.5,
            ),
            xaxis2=dict(
                autorange=True,
                showgrid=True,
                gridcolor='lightgrey',
                gridwidth=0.5,
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.5,
                showline=True,
                linewidth=1,
                linecolor='grey',
                mirror=False
            ),
            yaxis2=dict(
                autorange=True,
                showgrid=True,
                gridcolor='lightgrey',
                gridwidth=0.5,
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.5,
                linewidth=1,
                linecolor='grey',
                mirror=False
            ),
            xaxis4=dict(
                title=f'{x}',
                showticklabels=True,
                showgrid=True,
                gridcolor='lightgrey',
                gridwidth=0.5,
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.5,
                autorange=True,
            ),
        )
        return fig


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)

    indices = MetaData[MetaData['industry'] == 'WI26 반도체'].head(10)
    bubble = Market(indices.index, env='.py', proc=True)
    # print(bubble)
    # bubble = Market(['005930'], proc=False)
    # print(bubble)
    bubble.append('trend.strength()["3M"]', column='trendStrength3M')
    bubble.append('trend.gaps()["1Y"]', column='trendGap1Y')
    print(bubble)
    bubble.scatter(x='trendStrength3M', y='trendGap1Y').show()
