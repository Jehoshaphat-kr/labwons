from labwons.common.tools import int2won
from labwons.equity._deprecated import _calc
from datetime import datetime, timedelta
from pykrx.stock import get_market_cap_by_date
from plotly import graph_objects as go
from plotly.offline import plot
import pandas as pd


class statement(pd.DataFrame):
    def __init__(self, base:_calc, by:str= 'annual'):
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
            showlegend=False,
            visible=True if col == self.columns[0] else False,
            mode='lines+markers+text',
            meta=self._meta(col),
            texttemplate='%{meta}',
            hoverinfo='skip'
        )

    def figure(self) -> go.Figure:
        data = [self.trace(col) for col in self.columns]
        buttons = list()
        for n, tr in enumerate(data):
            visible = [False] * len(data)
            visible[n] = True
            buttons.append(
                dict(
                    label=tr.name,
                    method="update",
                    args=[{"visible": visible}]
                )
            )
        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title=f"<b>{self._base_.name}({self._base_.ticker})</b> Financial Statement",
                plot_bgcolor='white',
                updatemenus=[
                    dict(
                        # type="buttons",
                        direction="down",
                        active=0,
                        xanchor='left', x=0.0,
                        yanchor='bottom', y=1.0,
                        buttons=buttons
                    )
                ],
                xaxis=dict(
                    title='기말',
                    showticklabels=True,
                    showgrid=False,
                ),
                yaxis=dict(
                    title='[억원, -, %]',
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
            filename=f'{self._base_.path}/STATEMENT.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return