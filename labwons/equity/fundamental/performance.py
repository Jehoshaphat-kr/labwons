from labwons.common.tools import int2won
from labwons.equity._deprecated import _calc
from datetime import datetime, timedelta
from pykrx.stock import get_market_cap_by_date
from plotly import graph_objects as go
from plotly.offline import plot
import pandas as pd


class performance(pd.DataFrame):
    def __init__(self, base:_calc, by:str= 'annual'):
        """
        Performance
        :return:

        """
        sales = base.calcStatement(by=by)
        sales.index.name = '기말'
        key = [_ for _ in ['매출액', '순영업수익', '이자수익', '보험료수익'] if _ in sales.columns][0]
        salesExp = sales[sales.index.str.endswith(')')][[key, '영업이익', '당기순이익']]

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
        basis = pd.concat(objs=[basis, salesExp], axis=0).head(len(basis) + 1)
        super().__init__(
            index=basis.index,
            columns=basis.columns,
            data=basis.values
        )
        self._base_ = base
        return

    def __call__(self, col:str):
        return self.trace(col)

    def trace(self, col:str) -> go.Bar:
        return go.Bar(
            name=col,
            x=self.index,
            y=self[col],
            showlegend=True,
            visible=True,
            meta=[int2won(x) for x in self[col]],
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