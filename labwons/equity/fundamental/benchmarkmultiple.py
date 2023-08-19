from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from urllib.request import urlopen
import pandas as pd
import numpy as np
import json


class benchmarkmultiple(baseDataFrameChart):
    def __init__(self, base:fetch):
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

        super().__init__(pd.concat(objs=objs, axis=1).astype(float), **getattr(base, '_valid_prop'))
        self._base_ = base
        self._filename_ = 'Benchmark Multiples'
        return

    def figure(self) -> go.Figure:
        data = [
            self.bar(
                col,
                name=col[0],
                showlegend=False if n % 3 else True,
                legendgroup=col[0],
                visible=True if col[0] == 'PER' else 'legendonly',
                texttemplate=col[1] + "<br>%{y}" + ("%" if col[0] == 'ROE' else ''),
                marker=dict(
                    color=['lightgreen', 'lightpink', 'lightblue'][n % 3],
                    opacity=0.9
                ),
                yhoverformat='.2f',
                hovertemplate='%{y}' + ("%" if col[0] == 'ROE' else '') + '<extra>' + col[1] + '</extra>'
            ) for n, col in enumerate(self)
        ]
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
