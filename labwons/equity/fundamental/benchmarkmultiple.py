from labwons.equity.refine import _refine
from plotly import graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
from urllib.request import urlopen
import pandas as pd
import numpy as np
import json


class benchmarkmultiple(pd.DataFrame):
    def __init__(self, base:_refine):
        """
        Benchmark Multiple
        :return:
        """
        url = f"http://cdn.fnguide.com/SVO2/json/chart/01_04/chart_A{base.ticker}_D.json"
        data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        objs = dict()
        for label, index in (('PER', '02'), ('EV/EBITDA', '03'), ('ROE', '04')):
            header1 = pd.DataFrame(data[f'{index}_H'])[['ID', 'NAME']].set_index(keys='ID')
            header1['NAME'] = header1['NAME'].astype(str).str.replace("'", "20")
            header1 = header1.to_dict()['NAME']
            header1.update({'CD_NM': '이름'})

            inner1 = pd.DataFrame(data[index])[list(header1.keys())].rename(columns=header1).set_index(keys='이름')
            inner1.index.name = None
            for col in inner1.columns:
                inner1[col] = inner1[col].apply(lambda x: np.nan if x == '-' else x)
            objs[label] = inner1.T
        basis = pd.concat(objs=objs, axis=1).astype(float)
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