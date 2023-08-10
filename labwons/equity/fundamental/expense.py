from labwons.equity._deprecated import _calc
from plotly import graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import pandas as pd


class expense(pd.DataFrame):
    def __init__(self, base:_calc):
        """
        Expenses
        :return:
        """
        _columns = {
            'R&D 투자 총액 / 매출액 비중.1': 'R&D투자비중',
            '무형자산 처리 / 매출액 비중.1': '무형자산처리비중',
            '당기비용 처리 / 매출액 비중.1': '당기비용처리비중'
        }
        url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Corp.asp?" \
              f"pGB=1&gicode=A{base.ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=102&stkGb=701"
        html = pd.read_html(url, header=0)

        rnd = html[8].set_index(keys=['회계연도'])["R&D 투자 총액 / 매출액 비중.1"]
        rnd.name = 'R&D투자비중'
        if '관련 데이터가 없습니다.' in rnd.index:
            rnd.drop(index=['관련 데이터가 없습니다.'], inplace=True)
        basis = pd.concat(
            objs=[
                base.calcStatement()['영업이익률'],
                html[4].set_index(keys=['항목']).T, # 매출원가율
                html[5].set_index(keys=['항목']).T, # 판관비
                rnd
            ],
            axis=1
        ).sort_index(ascending=True).astype(float)
        basis.index.name = '기말'
        if len(basis.iloc[0].dropna()) <= 1:
            basis = basis.drop(index=basis.index[0]).drop(index=[i for i in basis.index if '(' in i][1:])
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
        return go.Scatter(
            name=col,
            x=self.index,
            y=self[col].astype(float),
            showlegend=True,
            visible=True,
            mode='lines+markers+text',
            textposition="bottom center",
            texttemplate="%{y:.2f}%",
            hovertemplate='%{x}: %{y:.2f}%<extra></extra>'
        )

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=["Profit Rate", "Sales Cost Rate", "Sales and Management Cost Rate", "R&D Investment Rate"],
            x_title="기말",
            y_title="[%]",
        )
        fig.add_traces(
            data=[
                self.trace(col="영업이익률"),
                self.trace(col="매출원가율"),
                self.trace(col="판관비율"),
                self.trace(col="R&D투자비중")
            ],
            rows=[1, 1, 2, 2],
            cols=[1, 2, 1, 2]
        )
        fig.update_layout(
            title=f"<b>{self._base_.name}({self._base_.ticker})</b> Profit Rate and Expenses",
            plot_bgcolor='white',
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=1,
                y=1.04
            ),
        )
        fig.update_yaxes(
            dict(
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinewidth=0.5,
                zerolinecolor='lightgrey'
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
            filename=f'{self._base_.path}/EXPENSES.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return