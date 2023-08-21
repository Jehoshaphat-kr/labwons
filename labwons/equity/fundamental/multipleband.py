from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from urllib.request import urlopen
import pandas as pd
import numpy as np
import json


class multipleband(baseDataFrameChart):
    def __init__(self, base:fetch):
        """
        Multiple Bands
        :return:

        """
        url = f"http://cdn.fnguide.com/SVO2/json/chart/01_06/chart_A{base.ticker}_D.json"
        src = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        per_header = pd.DataFrame(src['CHART_E'])[['ID', 'NAME']].set_index(keys='ID')
        pbr_header = pd.DataFrame(src['CHART_B'])[['ID', 'NAME']].set_index(keys='ID')
        per_header, pbr_header = per_header.to_dict()['NAME'], pbr_header.to_dict()['NAME']
        per_header.update({'GS_YM': 'date'})
        pbr_header.update({'GS_YM': 'date'})

        df = pd.DataFrame(src['CHART'])
        per = df[per_header.keys()].replace('-', np.nan).replace('', np.nan)
        pbr = df[pbr_header.keys()].replace('-', np.nan).replace('', np.nan)
        per['GS_YM'], pbr['GS_YM'] = pd.to_datetime(per['GS_YM']), pd.to_datetime(pbr['GS_YM'])
        basis = pd.concat(
            objs=dict(
                per=per.rename(columns=per_header).set_index(keys='date').astype(float),
                pbr=pbr.rename(columns=pbr_header).set_index(keys='date').astype(float)
            ),
            axis=1
        )
        super().__init__(basis, **getattr(base, '_valid_prop'))
        self._base_ = base
        self._filename_ = 'MultipleBand'
        return

    def figure(self) -> go.Figure:
        data = [
            self.line(
                col,
                name=col[1].replace('수정', ''),
                showlegend=False,
                legendgroup=None if col[1] == '수정주가' else col[0],
                visible=True if col[0] == 'per' else False,
                line=dict(
                    color='royalblue' if col[1] == '수정주가' else None,
                    dash='solid' if col[1] == '수정주가' else 'dash'
                ),
                yhoverformat=',d' if col[1] == '수정주가' else '.2f',
                hovertemplate='%{y}' + 'KRW'
            )
            for n, col in enumerate(self) if not col == ('pbr', '수정주가')
        ]
        buttons = [
            dict(
                label='PER BAND',
                method='update',
                args=[{'visible': [True, True, True, True, True, True, False, False, False, False, False]}]
            ),
            dict(
                label='PBR BAND',
                method='update',
                args=[{'visible': [True, False, False, False, False, False, True, True, True, True, True]}]
            )
        ]

        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title=f"<b>{self._base_.name}({self._base_.ticker})</b> Multiple Band",
                plot_bgcolor='white',
                margin=dict(r=0),
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    xanchor="right",
                    yanchor="bottom",
                    x=0.98,
                    y=1.02
                ),
                updatemenus=[
                    dict(
                        direction="down",
                        active=0,
                        xanchor='left', x=0.0,
                        yanchor='bottom', y=1.0,
                        buttons=buttons
                    )
                ],
                xaxis=dict(
                    title='Date',
                    showgrid=True,
                    gridcolor='lightgrey'
                ),
                yaxis=dict(
                    title='[KRW]',
                    showgrid=True,
                    gridcolor='lightgrey',
                )
            )
        )
        return fig
