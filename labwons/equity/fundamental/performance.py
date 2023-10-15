from labwons.common.tools import int2won
from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from datetime import datetime, timedelta
from pykrx.stock import get_market_cap_by_date
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import pandas as pd


class performance(baseDataFrameChart):
    def __init__(self, base:fetch):
        """
        Performance

        :return:
        """
        if not (base.country == 'KOR' and base.quoteType == 'EQUITY'):
            raise AttributeError(f'No Performance data for {base.ticker} in {base.country}')
        annual = getattr(base, "_annualstatement")
        quarter = getattr(base, "_quarterstatement")

        columns = annual.columns.tolist()
        columns = columns[:columns.index('당기순이익') + 1]
        columns = [col for col in columns if not '(' in col]
        annual = annual[columns]
        quarter = quarter[columns]

        cap = get_market_cap_by_date(
            fromdate=(datetime.today() - timedelta(365 * 5)).strftime("%Y%m%d"),
            todate=datetime.today().strftime("%Y%m%d"),
            freq='m',
            ticker=base.ticker
        )['시가총액']
        if cap.empty:
            cap = pd.DataFrame(columns=['시가총액'])
        annual_cap = cap[
            cap.index.astype(str).str.contains('12') | \
            (cap.index == cap.index[-1])
        ].copy() / 100000000
        annual_cap.index = annual_cap.index.strftime("%Y/%m")
        annual_cap.index = annual_cap.index[:-1].tolist() + [f"{annual_cap.index[-1][:4]}/현재"]

        quarter_cap = cap[
            cap.index.astype(str).str.contains('03') | \
            cap.index.astype(str).str.contains('06') | \
            cap.index.astype(str).str.contains('09') | \
            cap.index.astype(str).str.contains('12') | \
            (cap.index == cap.index[-1])
        ].copy() / 100000000
        quarter_cap.index = quarter_cap.index.strftime("%Y/%m")
        quarter_cap.index = quarter_cap.index[:-1].tolist() + [f"{quarter_cap.index[-1][:4]}/현재"]

        annual = annual.join(other=annual_cap, how='left')
        quarter = quarter.join(other=quarter_cap, how='left')
        print(annual)
        print(quarter)


        # sales = [_ for _ in ['매출액', '순영업수익', '이자수익', '보험료수익'] if _ in annual.columns][0]
        # salesExp = earn[earn.index.str.endswith(')')][[key, '영업이익']]
        #
        # cap = get_market_cap_by_date(
        #     fromdate=(datetime.today() - timedelta(365 * 5)).strftime("%Y%m%d"),
        #     todate=datetime.today().strftime("%Y%m%d"),
        #     freq='y',
        #     ticker=base.ticker
        # )
        # if cap.empty:
        #     cap = pd.DataFrame(columns=['시가총액'])
        # cap['시가총액'] = round(cap['시가총액'] / 100000000, 1).astype(int)
        # cap.index = cap.index.strftime("%Y/%m")
        # cap['기말'] = cap.index[:-1].tolist() + [f"{cap.index[-1][:4]}/현재"]
        # cap = cap.set_index(keys='기말')
        #
        # basis = cap.join(earn, how='left')[['시가총액', key, '영업이익']]
        # basis = pd.concat(objs=[basis, salesExp], axis=0).head(len(basis) + 1)

        super().__init__(
            data=annual,
            name='PERFORMACNE',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='KRW',
            ref=base
        )
        return

    def figure(self) -> go.Figure:
        data = [
            self.bar(
                col,
                drop=False,
                showlegend=True,
                meta=self[col].apply(int2won),
                texttemplate='%{meta}',
                marker=dict(opacity=0.9),
                hovertemplate='%{meta}'
            ) for col in self
        ] + [
            self._base_.statement(
                'EPS(원)',
                line=dict(color='black', dash='dash', width=0.8),
                marker=dict(color='black'),
                texttemplate="%{y:,d}",
                hovertemplate='%{y:,d}원<extra>EPS</extra>'
            )
        ]
        fig = make_subplots(
            rows=1, cols=1,
            x_title='기말',
            specs=[[{'secondary_y': True}]]
        )
        fig.add_traces(
            data=data,
            rows=[1] * len(data),
            cols=[1] * len(data),
            secondary_ys=[False] * (len(data) - 1) + [True]
        )

        fig.update_layout(
            title=f"<b>{self._base_.name}({self._base_.ticker})</b> Earnings",
            plot_bgcolor='white',
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=0.96,
                y=1
            ),
            xaxis=dict(
                showticklabels=True,
                showgrid=False,
            ),
            yaxis=dict(
                title='실적 [억원]',
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis2=dict(
                title='EPS [원]'
            )
        )
        return fig
