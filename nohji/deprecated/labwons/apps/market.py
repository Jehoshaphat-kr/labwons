from nohji.deprecated.labwons.common.tools import normalDistribution
from nohji.deprecated.labwons.equity import Equity
from typing import Iterable
from tqdm.notebook import tqdm_notebook
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class Market(pd.DataFrame):
    _equity_ = {}
    progressBar = True

    def __init__(self, tickers:Iterable, **kwargs):
        """
        :param tickers : [str]
        :param kwargs  : [Any] Arguments for <class: Equity>
        """
        self.progressBar = kwargs['progress'] if 'progress' in kwargs else True
        data = MetaData.KRSTOCKwMultiples[MetaData.KRSTOCKwMultiples.index.isin(tickers)].copy()
        super().__init__(
            data=data.values,
            index=data.index,
            columns=data.columns
        )
        self.drop(inplace=True, index=self[self['marketCap'].isna()].index)
        self['size'] = 20 * self['marketCap'] / self['marketCap'].max()

        loop = self.__loop__()
        for ticker in loop:
            if self.progressBar:
                loop.set_description(f"Initialize {ticker} ... ")
            self._equity_[ticker] = Equity(ticker, **kwargs)

        for prop in [
            "previousForeignRate",
            "dividendYield",
            "beta",
            "trailingPE",
            "forwardPE",
            "priceToBook",
            "fiftyTwoWeekHighRatio",
            "fiftyTwoWeekLowRatio",
            "targetPriceRatio"
        ]:
            self.append(prop)
        return

    def __call__(self, ticker:str) -> Equity:
        return self._slot_[ticker]

    def __loop__(self, group:Iterable=None):
        if not group:
            group = self.index
        if self.progressBar:
            return tqdm_notebook(group)
        else:
            return group

    def append(self, property_name:str, new_column:str='', index:str=''):
        new_column = property_name if not new_column else new_column
        if new_column in self:
            return
        data = []
        loop = self.__loop__()
        for ticker in loop:
            if self.progressBar:
                loop.set_description(f'Updating {new_column} {ticker} ... ')

            inst = getattr(self._equity_[ticker], property_name)
            if isinstance(inst, pd.Series):
                data.append(inst[index])
            elif callable(inst):
                data.append(inst())
            else:
                data.append(inst)
        self[new_column] = data
        return


    # def __slot__(self):
    #     tickers = [ticker for ticker in self.index if not ticker in self._slot_]
    #     if not tickers:
    #         return
    #
    #     __loop__ = self.__loop__(tickers)
    #     for n, ticker in enumerate(__loop__):
    #         if self.processbar:
    #             __loop__.set_description(f"Initializing ...  {ticker}")
    #         if ticker in self._slot_:
    #             continue
    #         self._slot_[ticker] = Equity(ticker, **self._kwargs_)
    #         if not n % 20:
    #             time.sleep(0.5)
    #     return

    # @staticmethod
    # def __prop__(__obj, __prop:str):
    #     props = __prop.split('.')
    #     for _prop in props:
    #         if not hasattr(__obj, _prop):
    #             raise AttributeError(f'No Such attribute: {__prop}')
    #         __obj = getattr(__obj, _prop)
    #     return __obj

    # def append(self, prop:str, column:str=''):
    #     self.__slot__()
    #
    #     operand = ''
    #     for optype in ['.iloc', '.loc', '.iat', '.at', '[']:
    #         if optype in prop:
    #             operand = optype
    #             break
    #
    #     index = eval(prop[prop.find('[') + 1:prop.find(']')]) if operand else ''
    #     prop = prop[:prop.find('(')] if ')' in prop else prop
    #     data = []
    #     __loop__ = self.__loop__()
    #     for n, ticker in enumerate(__loop__):
    #         if self.processbar:
    #             __loop__.set_description(desc=f'{prop} ... {ticker}')
    #         if len(self._slot_[ticker].ohlcv) < 126:
    #             data.append(np.nan)
    #             continue
    #         _data = self.__prop__(self._slot_[ticker], prop)
    #         if callable(_data):
    #             _data = _data()
    #         if operand:
    #             _data = _data[index] if operand == '[' else getattr(_data, operand[1:])[index]
    #         if isinstance(_data, pd.DataFrame) or isinstance(_data, pd.Series):
    #             raise TypeError(f'Append new market data must be 1x1 single data format, Not dataframe or series')
    #         data.append(_data)
    #         if not n % 20:
    #             time.sleep(0.5)
    #     self[column if column else prop] = data
    #     return

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
        self['size'] = 20 * self['size'] / self['size'].max()
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
                hovertemplate='%{meta}<br>' + x + ': %{x}<br>' + y + ': %{y}<extra></extra>'
            )
        )

        ynorm = normalDistribution(self[y].astype(float))
        fig.add_trace(
            row=1, col=1,
            trace=go.Scatter(
                x=ynorm,
                y=ynorm.index,
                mode='markers',
                showlegend=False,
                meta=self['name'] + '(' + self.index + ')',
                hovertemplate='%{meta}: %{y}<extra></extra>'
            )
        )
        xnorm = normalDistribution(self[x].astype(float))
        fig.add_trace(
            row=2, col=2,
            trace=go.Scatter(
                x=xnorm.index,
                y=xnorm,
                mode='markers',
                showlegend=False,
                meta=self['name'] + '(' + self.index + ')',
                hovertemplate='%{meta}: %{x}<extra></extra>'
            )
        )
        fig.add_vline(x=self[x].mean(), row=1, col=2, line_width=0.5, line_dash="dash", line_color="black")
        fig.add_hline(y=self[y].mean(), row=1, col=2, line_width=0.5, line_dash="dash", line_color="black")
        fig.update_layout(
            # title=f'Scatter x: {x} / y: {y}',
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
    # indices = MetaData[MetaData['industry'] == 'WI26 반도체']
    # indices = ['AAPL', '']

    bubble = Market(indices.index, progress=False)
    print(bubble)

    # bubble.append('trend.strength()["3M"]', column='trendStrength3M')
    # bubble.append('trend.gaps()["1Y"]', column='trendGap1Y')
    # print(bubble)

    # bubble.scatter(x='trendStrength3M', y='trendGap1Y').show()
    # bubble.scatter(x='PBR', y='PER').show()
