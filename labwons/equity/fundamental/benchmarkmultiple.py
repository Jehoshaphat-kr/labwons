from labwons.equity.refine import _refine
from plotly import graph_objects as go
from plotly.offline import plot
from urllib.request import urlopen
import pandas as pd
import numpy as np
import json


class benchmarkmultiple(pd.DataFrame):
    def __init__(self, base:_refine):
        """
        Benchmark Multiple
        :return:
                                        PER                     EV/EBITDA                           ROE
               LEENO  KOSDAQ-IT&H/W  KOSDAQ  LEENO  KOSDAQ-IT&H/W  KOSDAQ  LEENO  KOSDAQ-IT&H/W  KOSDAQ
        2021   29.12          28.08   35.68  23.35          15.23  16.88   27.50           9.51    7.32
        2022   20.72          19.88   41.02  15.73           9.40  12.19   25.11           7.77    3.94
        2023E    NaN          20.94   26.89    NaN           9.93  13.48     NaN          11.61   11.65
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