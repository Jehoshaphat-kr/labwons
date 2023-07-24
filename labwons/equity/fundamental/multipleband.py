from labwons.equity.refine import _refine
from plotly import graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
from urllib.request import urlopen
import pandas as pd
import numpy as np
import json


class multipleband(pd.DataFrame):
    def __init__(self, base:_refine):
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
        super().__init__(
            index=basis.index,
            columns=basis.columns,
            data=basis.values
        )
        self._base_ = base
        return

    def __call__(self, col1:str) -> list:
        df = self[col1]
        return [self.trace(col1, col2) for col2 in df.columns]

    def trace(self, col1:str, col2:str) -> go.Scatter:
        return go.Scatter(
            name=col2 if col2 == '수정주가' else f"{col1.upper()} Band",
            x=self.index,
            y=self[col1][col2].astype(float),
            showlegend=True if (col1, col2) == self.columns[-1] or (col1, col2) == self.columns[1] or col2 == '수정주가' else False,
            legendgroup=None if col2 == '수정주가' else col1,
            visible=True if col1 == 'per' else 'legendonly',
            mode='lines',
            line=dict(
                color='royalblue' if col2 == '수정주가' else None,
                dash='solid' if col2 == '수정주가' else 'dot'
            ),
            xhoverformat='%Y/%m/%d',
            yhoverformat=',d' if col2 == '수정주가' else '.2f',
            hovertemplate=col2 + '%{y}KRW @%{x}<extra></extra>'
        )

    def figure(self) -> go.Figure:
        data = [self.trace(col1, col2) for col1, col2 in self.columns if not (col1 == 'pbr' and col2 == '수정주가')]
        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title=f"<b>{self._base_.name}({self._base_.ticker})</b> Multiple Band",
                plot_bgcolor='white',
                margin=dict(r=0),
                legend=dict(
                    orientation="h",
                    xanchor="right",
                    yanchor="bottom",
                    x=0.98,
                    y=1.02
                ),
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

    def show(self):
        self.figure().show()
        return

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{self._base_.path}/MULTIPLE-BANDS.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return