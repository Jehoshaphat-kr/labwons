from labwons.common.tools import int2won
from labwons.equity.refine import _refine
from datetime import datetime, timedelta
from pykrx.stock import get_market_cap_by_date
from plotly import graph_objects as go
from plotly.offline import plot
import pandas as pd


class statement(pd.DataFrame):
    def __init__(self, base:_refine, by:str='annual'):
        """
        Statement
        :return:
        """
        basis = base.calcStatement(by=by)
        n = len(basis) - len([i for i in basis.index if i.endswith(')')])
        basis = basis.head(n + 1)
        basis.index.name = '기말'
        super().__init__(
            index=basis.index,
            columns=basis.columns,
            data=basis.values
        )
        self._base_ = base
        return

    def __call__(self, col:str):
        return self.trace(col)

    def _meta(self, col:str) -> list:
        idx = self.columns.tolist().index(col)
        if idx <= 11:
            return [int2won(x) for x in self[col]]
        elif idx <= 17 or idx == 24:
            return [f'{x}%' for x in self[col]]
        elif idx <= 20:
            return [f'{x}원' for x in self[col]]
        else:
            return [f'{x}' for x in self[col]]

    def trace(self, col:str) -> go.Scatter:
        return go.Scatter(
            name=col,
            x=self.index,
            y=self[col],
            showlegend=True,
            visible=True,
            mode='lines+markers+text',
            meta=self._meta(col),
            texttemplate='%{meta}',
            marker=dict(
                opacity=0.8
            ),
            hovertemplate=col + '<br>%{meta}<extra></extra>'
        )

    def figure(self) -> go.Figure:
        data = [self.trace(col) for col in self.columns]
        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title=f"<b>{self._base_.name}({self._base_.ticker})</b> Performance",
                plot_bgcolor='white',
                legend=dict(
                    orientation="h",
                    xanchor="right",
                    yanchor="bottom",
                    x=1,
                    y=1
                ),
                xaxis=dict(
                    title='기말',
                    showticklabels=True,
                    showgrid=False,
                ),
                yaxis=dict(
                    title='[-, %]',
                    showgrid=True,
                    gridcolor='lightgrey'
                ),
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
            filename=f'{self._base_.path}/PERFORMANCE.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return