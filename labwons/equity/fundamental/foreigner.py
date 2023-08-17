from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from urllib.request import urlopen
import pandas as pd
import json


class foreigner(baseDataFrameChart):
    def __init__(self, base:fetch):
        objs = dict()
        for dt in ['3M', '1Y', '3Y']:
            url = f"http://cdn.fnguide.com/SVO2/json/chart/01_01/chart_A{base.ticker}_{dt}.json"
            data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
            frm = pd.DataFrame(data["CHART"])[['TRD_DT', 'J_PRC', 'FRG_RT']]
            frm = frm.rename(columns={'TRD_DT': 'date', 'J_PRC': 'close', 'FRG_RT': 'rate'}).set_index(keys='date')
            frm.index = pd.to_datetime(frm.index)
            frm = frm.replace('', '0.0')
            frm['close'] = frm['close'].astype(int)
            frm['rate'] = frm['rate'].astype(float)
            objs[dt] = frm

        super().__init__(frame=pd.concat(objs=objs, axis=1), **getattr(base, '_valid_prop'))
        self._base_ = base
        self._filename_ = 'ForeignRate'
        return

    def __call__(self, col:str or tuple):
        return

    # def trace(self, c1:str, c2:str) -> go.Scatter:
    #     return go.Scatter(
    #         name=c2.upper(),
    #         x=self[c1][c2].dropna().index,
    #         y=self[c1][c2].dropna(),
    #         showlegend=True,
    #         visible=True if c1 == '3M' else False,
    #         mode='lines',
    #         line=dict(
    #             color='royalblue' if 'close' in c2 else 'black',
    #             dash='solid' if 'close' in c2 else 'dot'
    #         ),
    #         xhoverformat="%Y/%m/%d",
    #         yhoverformat=',d' if 'close' in c2 else '.2f',
    #         hovertemplate='%{y}' + ('KRW' if 'close' == c2 else '%') + '<extra></extra>'
    #     )

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=1, cols=1,
            x_title='날짜',
            specs=[[{'secondary_y': True}]]
        )
        fig.add_traces(
            data=[
                self.line(
                    col,
                    visible=True if col[0] == '3M' else False,
                    line=dict(
                        color='royalblue' if col[1] == 'close' else 'black',
                        dash='solid' if col[1] == 'close' else 'dot',
                    ),
                    yhoverformat=',d' if col[1] == 'close' else '.2f',
                    unit='KRW' if col[1] == 'close' else '%'
                )
                for col in self
            ],
            rows=[1, 1, 1, 1, 1, 1],
            cols=[1, 1, 1, 1, 1, 1],
            secondary_ys=[False, True, False, True, False, True]
        )
        fig.update_layout(
            title=f"{self._base_.name}({self._base_.ticker}) Foreign Rate",
            plot_bgcolor='white',
            margin=dict(r=0),
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=0.96,
                y=1
            ),
            hovermode="x unified",
            xaxis=dict(
                tickformat="%Y/%m/%d",
                showticklabels=True,
                showgrid=True,
                gridcolor='lightgrey',
            ),
            yaxis=dict(
                title='[원]',
                showgrid=True,
                gridcolor='lightgrey',
            ),
            yaxis2=dict(
                title='[%]'
            ),
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    active=0,
                    xanchor='left', x=0.0,
                    yanchor='bottom', y=1.0,
                    buttons=list([
                        dict(
                            label="3개월",
                            method="update",
                            args=[{"visible": [True, True, False, False, False, False]}]
                        ),
                        dict(
                            label="1년",
                            method="update",
                            args=[{"visible": [False, False, True, True, False, False]}]
                        ),
                        dict(
                            label="3년",
                            method="update",
                            args=[{"visible": [False, False, False, False, True, True]}]
                        ),
                    ]),
                )
            ]

        )
        return fig
