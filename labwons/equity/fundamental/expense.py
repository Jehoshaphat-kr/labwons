from labwons.equity.refine import _refine
from plotly import graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import pandas as pd


class expense(pd.DataFrame):
    def __init__(self, base:_refine):
        """
        Business Model Products
        :return:

        """
        url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Corp.asp?" \
              f"pGB=1&gicode=A{base.ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=102&stkGb=701"
        html = pd.read_html(url, header=0)

        sales_cost = html[4].set_index(keys=['항목'])
        sales_cost.index.name = None

        sg_n_a = html[5].set_index(keys=['항목'])
        sg_n_a.index.name = None

        r_n_d = html[8].set_index(keys=['회계연도'])
        r_n_d.index.name = None
        r_n_d = r_n_d[['R&D 투자 총액 / 매출액 비중.1', '무형자산 처리 / 매출액 비중.1', '당기비용 처리 / 매출액 비중.1']]
        r_n_d = r_n_d.rename(columns={
            'R&D 투자 총액 / 매출액 비중.1': 'R&D투자비중',
            '무형자산 처리 / 매출액 비중.1': '무형자산처리비중',
            '당기비용 처리 / 매출액 비중.1': '당기비용처리비중'
        })
        if '관련 데이터가 없습니다.' in r_n_d.index:
            r_n_d.drop(index=['관련 데이터가 없습니다.'], inplace=True)
        basis = pd.concat(objs=[sales_cost.T, sg_n_a.T, r_n_d], axis=1).sort_index(ascending=True).astype(float)

        super().__init__(
            index=basis.index,
            columns=basis.columns,
            data=basis.values
        )
        self._base_ = base
        return

    def __call__(self, col:str):
        return self.trace(col)

    def trace(self, col:str) -> go.Scatter:
        name = col.upper().replace('_', ' ')
        color = dict(close='royalblue', short_sell='brown', short_balance='red')[col]
        return go.Scatter(
            name=name,
            x=self.index,
            y=self[col],
            showlegend=True,
            visible='legendonly' if 'balance' in col else True,
            mode='lines',
            line=dict(
                color=color,
                dash='solid' if col == 'close' else 'dot'
            ),
            xhoverformat='%Y/%m/%d',
            yhoverformat=',d' if col == 'close' else '.2f',
            hovertemplate=name + '%{y}' + ('KRW' if col == 'close' else '%') + '<extra></extra>'
        )

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{'secondary_y': True}]]
        )
        fig.add_traces(
            data=[self.trace(c) for c in self.columns],
            rows=[1, 1, 1], cols=[1, 1, 1],
            secondary_ys=[False, True, True]
        )
        fig.update_layout(
            title=f"<b>{self._base_.name}({self._base_.ticker})</b> SHORT",
            plot_bgcolor='white',
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=1,
                y=1
            ),
            hovermode="x unified",
            xaxis=dict(
                title='날짜',
                tickformat="%Y/%m/%d",
                showticklabels=True,
                showgrid=True,
                gridcolor='lightgrey',
            ),
            yaxis=dict(
                title='[KRW]',
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis2=dict(
                title='[%]',
            ),
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
            filename=f'{self._base_.path}/SHORT.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return