from labwons.equity.refine import _refine
from datetime import datetime, timedelta
from pykrx.stock import get_market_cap_by_date
from plotly import graph_objects as go
from plotly.offline import plot
from urllib.request import urlopen
import pandas as pd
import numpy as np
import json


class performance(pd.DataFrame):
    def __init__(self, base:_refine, by:str='annual'):
        """
        Performance
        :return:

        """
        sales = base.calcStatement(by=by)
        sales.index.name = '기말'
        key = [_ for _ in ['매출액', '순영업수익', '이자수익', '보험료수익'] if _ in sales.columns][0]

        salesExp = sales[sales.index.str.endswith(')')][[key, '영업이익', '당기순이익']]
        print(salesExp)
        for i_e in salesExp.index:
            print(i_e)
            print(salesExp.loc[i_e])
            print(all(salesExp.loc[i_e].tolist()))


        cap = get_market_cap_by_date(
            fromdate=(datetime.today() - timedelta(365 * 5)).strftime("%Y%m%d"),
            todate=datetime.today().strftime("%Y%m%d"),
            freq='y',
            ticker=base.ticker
        )
        if cap.empty:
            cap = pd.DataFrame(columns=['시가총액'])
        cap['시가총액'] = round(cap['시가총액'] / 100000000, 1).astype(int)
        cap.index = cap.index.strftime("%Y/%m")
        cap['기말'] = cap.index[:-1].tolist() + [f"{cap.index[-1][:4]}/현재"]
        cap = cap.set_index(keys='기말')
        basis = cap.join(sales, how='left')[['시가총액', key, '영업이익', '당기순이익']]

        if not salesExp.empty:
            basis = pd.concat(objs=[basis, salesExp], axis=0)
        super().__init__(
            index=basis.index,
            columns=basis.columns,
            data=basis.values
        )
        self._base_ = base
        return

    def __call__(self, col1:str, col2:str):
        return self.trace(col1, col2)

    def trace(self, col1:str, col2:str) -> go.Bar:
        index = self.columns.tolist().index((col1, col2))
        color = ['royalblue', 'brown', 'green'][index % 3]
        return go.Bar(
            name=col1.upper(),
            x=self.index,
            y=self[col1][col2],
            showlegend=True if index in [0, 3, 6] else False,
            legendgroup=col1,
            visible=True if col1 == 'PER' else 'legendonly',
            texttemplate=col2 + '<br>%{y}' + ('%' if col1 == 'ROE' else ''),
            marker=dict(
                color=color,
                opacity=0.8
            ),
            yhoverformat='.2f',
            hovertemplate=col2 + '<br>%{y}<extra></extra>'
        )

    def figure(self) -> go.Figure:
        data = [self.trace(col1, col2) for col1, col2 in self.columns]
        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title=f"<b>{self._base_.name}({self._base_.ticker})</b> Benchmark Multiple",
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
            filename=f'{self._base_.path}/BENCHMARK-MULTIPLE.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return