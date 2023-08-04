from labwons.equity.refine import _calc
from plotly import graph_objects as go
from plotly.offline import plot
from urllib.request import urlopen
import pandas as pd
import numpy as np
import json



class consensus(pd.DataFrame):
    def __init__(self, base:_calc):
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
        super().__init__(
            index=basis.index,
            columns=basis.columns,
            data=basis.values
        )
        self._base_ = base
        return

    def __call__(self, mode:str='bar'):
        return self.trace(mode)

    def trace(self, col:str) -> go.Scatter:
        name = 'CLOSE' if col == 'close' else 'CONSEN'
        color = 'royalblue' if col == 'close' else 'black'
        dash = 'solid' if col == 'close' else 'dot'
        meta = self['gap'] if col == 'consensus' else None
        template = name + ': %{y}KRW'
        return go.Scatter(
            name=name,
            x=self.index,
            y=self[col],
            visible=True,
            showlegend=True,
            mode='lines',
            line=dict(
                color=color,
                dash=dash,
            ),
            meta=meta,
            xhoverformat='%Y/%m/%d',
            yhoverformat='.2f' if col == 'consensus' else ',d',
            hovertemplate=template + ('(%{meta}%)' if col == 'consensus' else '') + '<extra></extra>'
        )

    def figure(self) -> go.Figure:
        fig = go.Figure(
            data=[self.trace('close'), self.trace('consensus')],
            layout=go.Layout(
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
                    title='날짜',
                    showticklabels=True,
                    showgrid=True,
                    gridcolor='lightgrey',
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
            filename=f'{self._base_.path}/CONSENSUS.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return