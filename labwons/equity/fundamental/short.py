from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from urllib.request import urlopen
import pandas as pd
import json


class short(baseDataFrameChart):
    def __init__(self, base:fetch):
        """
        Business Model Products
        :return:

        """
        url = f"http://cdn.fnguide.com/SVO2/json/chart/11_01/chart_A{base.ticker}_SELL1Y.json"
        data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        _short = pd.DataFrame(data['CHART']).rename(
            columns={'TRD_DT': 'date', 'VAL': 'Short Sell', 'ADJ_PRC': 'Close'}
        ).set_index(keys='date')
        _short.index = pd.to_datetime(_short.index)
        _short['Short Sell'] = _short['Short Sell'].astype(float)
        _short['Close'] = _short['Close'].astype(int)

        url = f"http://cdn.fnguide.com/SVO2/json/chart/11_01/chart_A{base.ticker}_BALANCE1Y.json"
        data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        _balance = pd.DataFrame(data['CHART']).rename(
            columns={'TRD_DT': 'date', 'BALANCE_RT': 'Short Balance'}
        ).set_index(keys='date')
        _balance.index = pd.to_datetime(_balance.index)
        _balance['Short Balance'] = _balance['Short Balance'].astype(float)

        basis = _short.join(_balance['Short Balance'], how='left')[['Close', 'Short Sell', 'Short Balance']]
        super().__init__(basis, **getattr(base, '_valid_prop'))
        self._base_ = base
        self._filename_ = 'Short'
        return

    def __call__(self, col:str, **kwargs):
        return self.line(col, **kwargs)

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{'secondary_y': True}]]
        )
        fig.add_traces(
            data=[
                self.line(
                    col,
                    visible='legendonly' if col == 'Short Sell' else True,
                    line=dict(
                        color={'Close': 'royalblue', 'Short Sell': 'brown', 'Short Balance': 'red'}[col],
                        dash='solid' if col == 'Close' else 'dot'
                    ),
                    yhoverformat=',d' if col == 'Close' else '.2f',
                    hovertemplate=col + ': %{y}' + ('KRW' if col == 'Close' else '%') + '<extra></extra>'
                )
                for col in self
            ],
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
