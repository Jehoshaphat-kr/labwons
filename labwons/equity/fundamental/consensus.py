from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from urllib.request import urlopen
import pandas as pd
import numpy as np
import json



class consensus(baseDataFrameChart):
    def __init__(self, base:fetch):
        """
        Time-Series Consensus
        :return:
                   evaluate consensus   close    gap
        date
        2022-07-22     4.00    210000  133300 -36.52
        2022-07-25     4.00    210000  132400 -36.95
        2022-07-26     4.00    190000  132300 -30.37
        ...             ...       ...     ...    ...
        2023-07-19     4.00    168000  160500  -4.46
        2023-07-20     4.00    168000  159700  -4.94
        2023-07-21     4.00    176000  161600  -8.18
        """
        url = f"http://cdn.fnguide.com/SVO2/json/chart/01_02/chart_A{base.ticker}.json"
        raw = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        basis = pd.DataFrame(raw['CHART'])
        basis = basis.rename(columns={'TRD_DT': 'date', 'VAL1': 'evaluate', 'VAL2': 'consensus', 'VAL3': 'close'})
        basis = basis.set_index(keys='date')
        basis.index = pd.to_datetime(basis.index)
        basis['consensus'] = basis['consensus'].apply(lambda x: int(x) if x else np.nan)
        basis['close'] = basis['close'].astype(int)
        basis['gap'] = round(100 * (basis['close'] / basis['consensus'] - 1), 2)
        super().__init__(frame=basis, **getattr(base, '_valid_prop'))
        self._base_ = base
        self._filename_ = 'Consensus'
        return

    def __call__(self, col:str, **kwargs):
        return self.line(col, **kwargs)

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            row_width=[0.2, 0.8],
            vertical_spacing=0.01
        )
        fig.add_traces(
            data=[
                self(
                    'close',
                    name='Close',
                    hovertemplate='Close: %{y:,d}KRW<extra></extra>'
                ),
                self(
                    'consensus',
                    name='Consen',
                    line=dict(dash='dot', color='black'),
                    hovertemplate='Consen: %{y:,d}KRW<extra></extra>'
                ),
                self(
                    'gap',
                    name='%Gap',
                    hovertemplate='Gap: %{y:.2f}%<extra></extra>'
                )
            ],
            rows=[1, 1, 2],
            cols=[1, 1, 1]
        )
        fig.update_layout(
            title=f"<b>{self._base_.name}({self._base_.ticker})</b> CONSENSUS",
            plot_bgcolor='white',
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=1,
                y=1.04
            ),
            hovermode="x unified",
            xaxis=dict(
                title="",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            xaxis2=dict(
                title="DATE",
                tickformat='%Y/%m/%d',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            yaxis=dict(
                title='[KRW]',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            yaxis2 = dict(
                title='[%]',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            )

        )
        return fig
