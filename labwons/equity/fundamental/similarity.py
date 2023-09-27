from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from urllib.request import urlopen
import pandas as pd
import numpy as np
import json


class similarity(pd.DataFrame):
    colors = [
        'royalblue',
        'green',
        'magenta',
        'brown',
        'purple',
        'navy'
    ]
    def __init__(self, simMatrix:pd.DataFrame):
        super().__init__(
            index=simMatrix.index,
            columns=simMatrix.columns,
            data=simMatrix.values
        )
        self.index.name = '종목코드'
        return

    def __call__(self, *args, **kwargs):
        return

    def _bars(self, col:str) -> list:
        series = self[col].astype(int if '억' in col or '원' in col else float)
        color = ['royalblue' if v < 0 else 'red' for v in series] if col == '등락률' else self.colors
        return [
            go.Bar(
                name=self.loc[ticker, '종목명'],
                x=[self.loc[ticker, '종목명']],
                y=[series[ticker]],
                showlegend=True,
                visible=True,
                marker=dict(
                    color=color[n],
                    opacity=0.9
                ),
                hovertemplate='%{y}',
                meta=col,
            ) for n, ticker in enumerate(self.index)
        ]

    def figure(self, col:str) -> go.Figure:
        layout = go.Layout(
            title=f"<b>{self.iloc[0, 0]}({self.index[0]})</b> SIMILARITIES",
            plot_bgcolor='white',
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=1,
                y=1.04
            ),
            yaxis=dict(
                title='[억원, 원, %, 배]',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=1.0
            ),
        )
        fig = go.Figure(
            data=self._bars(col),
            layout=layout
        )
        return fig