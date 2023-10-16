from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.common.tools import int2won
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
import pandas as pd


class _performance(baseDataFrameChart):
    def __init__(self, statement:Any, name:str, subject:str, path:str):
        super(_performance, self).__init__(
            data=data,
            name=name,
            subject=subject,
            path=path
        )

        from datetime import datetime, timedelta
        from pykrx.stock import get_market_cap_by_date

        key = [_ for _ in ['매출액', '순영업수익', '이자수익', '보험료수익'] if _ in data.columns][0]
        salesExp = data[data.index.str.endswith(')')][[key, '영업이익']]

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

        basis = cap.join(earn, how='left')[['시가총액', key, '영업이익']]
        basis = pd.concat(objs=[basis, salesExp], axis=0).head(len(basis) + 1)
        return


class statement(baseDataFrameChart):
    default_columns = [
        "매출액", "영업이익", "영업이익(발표기준)", "당기순이익", "지배주주순이익", "비지배주주순이익",
        "자산총계", "부채총계", "자본총계", "지배주주지분", "비지배주주지분", "자본금",
        "부채비율", "유보율", "영업이익률", "지배주주순이익률",
        "ROA", "ROE", "EPS(원)", "BPS(원)", "DPS(원)", "PER", "PBR", "발행주식수", "배당수익률"
    ]
    _a = pd.DataFrame(columns=default_columns)
    _q = pd.DataFrame(columns=default_columns)

    def __init__(self, base:fetch):
        """
        Financial Highlight from Company Guide
        Valid only, and only if the given stock is open-traded in Korean market.

        Example. "LEENO (Ticker: 058470) from KOSPI"

                  매출액  영업이익  영업이익(발표기준)  당기순이익  지배주주순이익  비지배주주순이익    \
        기말
        2018/12     1504       575                575          486             486               NaN    \
        2019/12     1703       641                641          528             528               NaN    \
        2020/12     2013       779                779          554             554               NaN    \
        2021/12     2802      1171               1171         1038            1038               NaN    \
        2022/12     3224      1366               1366         1144            1144               NaN    \
        2023/12(E)   NaN       NaN                NaN          NaN             NaN               NaN    \

                  자산총계  부채총계  자본총계  지배주주지분  비지배주주지분  자본금  부채비율   유보율 \
        기말
        2018/12      2826       198       2628         2628              0.0      76      7.52  3397.27 \
        2019/12      3257       255       3002         3002              0.0      76      8.51  3869.61 \
        2020/12      3615       242       3373         3373              0.0      76      7.17  4357.24 \
        2021/12      4664       487       4177         4177              0.0      76     11.65  5411.70 \
        2022/12      5315       383       4932         4932              0.0      76      7.77  6402.10 \
        2023/12(E)    NaN       NaN        NaN          NaN              NaN     NaN       NaN      NaN \

                  영업이익률  지배주주순이익률    ROA    ROE  EPS(원)  BPS(원)  DPS(원)    PER   PBR  발행주식수  배당수익률
        기말
        2018/12        38.27             32.35  18.39  19.82     3191    17486     1100  14.74  2.69       15242        2.34
        2019/12        37.66             31.00  17.36  18.75     3463    19848     1200  18.57  3.24       15242        1.87
        2020/12        38.68             27.51  16.12  17.37     3633    22286     1500  37.16  6.06       15242        1.11
        2021/12        41.80             37.05  25.08  27.50     6810    27558     2500  29.12  7.20       15242        1.26
        2022/12        42.38             35.47  22.92  25.11     7503    32511     3000  20.72  4.78       15242        1.93
        2023/12(E)       NaN               NaN    NaN    NaN      NaN      NaN      NaN    NaN   NaN         NaN         NaN
        :return:
        """
        if base.country == 'KOR' and base.quoteType == 'EQUITY':
            url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?" \
                  f"pGB=1&gicode=A{base.ticker}&cID=&MenuYn=Y&ReportGB=D&NewMenuID=Y&stkGb=701"
            html = pd.read_html(url, header=0)
            self._a = self._reframe(
                html[14] if html[11].iloc[0].isnull().sum() > html[14].iloc[0].isnull().sum() else html[11]
            )
            self._q = self._reframe(
                html[15] if html[11].iloc[0].isnull().sum() > html[14].iloc[0].isnull().sum() else html[12]
            )

        super().__init__(
            data=self._a,
            name="FINANCIAL STATEMENT",
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            form=base.dtype,
            unit=base.unit,
        )
        return

    @staticmethod
    def _reframe(data: pd.DataFrame) -> pd.DataFrame:
        _data = data.set_index(keys=[data.columns[0]])
        _data.index.name = None
        if isinstance(_data.columns[0], tuple):
            _data.columns = _data.columns.droplevel()
        else:
            _data.columns = _data.iloc[0]
            _data = _data.drop(index=_data.index[0])
        _data = _data.T
        _data = _data.head(len(_data) - len([i for i in _data.index if i.endswith(')')]) + 1)
        _data.index.name = '기말'
        return _data

    @property
    def performance(self) -> _performance:
        return _performance(
            data=self,
            name='PERFORMANCE',
            subject=self.subject,
            path=self.path
        )

    # def _meta(self, col:str) -> list:
    #     idx = self.columns.tolist().index(col)
    #     if idx <= 11:
    #         return [int2won(x) for x in self[col]]
    #     elif idx <= 17 or idx == 24:
    #         return [f'{x}%' for x in self[col]]
    #     elif idx <= 20:
    #         return [f'{x}원' for x in self[col]]
    #     else:
    #         return [f'{x}' for x in self[col]]
    #
    # def figure(self) -> go.Figure:
    #     data = [
    #         self.lineTY(
    #             col,
    #             visible=False if n else True,
    #             showlegend=False,
    #             meta=self._meta(col),
    #             texttemplate='%{meta}',
    #             hovertemplate='%{meta}'
    #         )
    #         for n, col in enumerate(self)
    #     ]
    #     buttons = list()
    #     for n, tr in enumerate(data):
    #         visible = [False] * len(data)
    #         visible[n] = True
    #         buttons.append(
    #             dict(
    #                 label=tr.name,
    #                 method="update",
    #                 args=[{"visible": visible}]
    #             )
    #         )
    #     fig = go.Figure(
    #         data=data,
    #         layout=go.Layout(
    #             title=f"<b>{self.subject}</b> Financial Statement",
    #             plot_bgcolor='white',
    #             updatemenus=[
    #                 dict(
    #                     direction="down",
    #                     active=0,
    #                     xanchor='left', x=0.0,
    #                     yanchor='bottom', y=1.0,
    #                     buttons=buttons
    #                 )
    #             ],
    #             xaxis=dict(
    #                 title='기말',
    #                 showticklabels=True,
    #                 showgrid=False,
    #             ),
    #             yaxis=dict(
    #                 title='[억원, -, %]',
    #                 showgrid=True,
    #                 gridcolor='lightgrey'
    #             ),
    #         )
    #     )
    #     return fig
