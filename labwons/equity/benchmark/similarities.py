from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from datetime import timedelta
import plotly.graph_objects as go
import pandas as pd


class similarities(baseDataFrameChart):
    colors = [
        'royalblue',
        'green',
        'magenta',
        'brown',
        'purple',
        'navy'
    ]

    def __init__(self, base: fetch):
        super(similarities, self).__init__(
            data=getattr(base, '_naver').similarities,
            name="BENCHMARK - Returns",
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            form='.2f',
            unit='%',
            ref=base
        )
        return

    @staticmethod
    def _buttonVisibility(col:str, data:list):
        visible = list()
        for trace in data:
            visible.append(True if trace.meta == col else False)
        return visible

    def _bars(self, col:str) -> list:
        series = self[col].apply(lambda x: float(x) if '.' in x else int(x))
        color = ['royalblue' if v < 0 else 'red' for v in series] if col == '등락률' else self.colors
        unit = '원' if '억' in col or '원' in col else '배' if '배' in col else '%'
        return [
            go.Bar(
                name=self.loc[ticker, '종목명'],
                x=[self.loc[ticker, '종목명']],
                y=[series[ticker]],
                showlegend=True,
                visible=True if col == '등락률' else False,
                marker=dict(
                    color=color[n],
                    opacity=0.9
                ),
                text=[int2won(series[ticker]) if '억' in col else series[ticker]],
                texttemplate='%{text}' + unit,
                hoverinfo='skip',
                meta=col,
            ) for n, ticker in enumerate(self.index)
        ]

    def figure(self) -> go.Figure:
        loop = [col for col in self if not col in ["종목명", "현재가"]]
        data = list()
        for col in loop:
            data += self._bars(col)
        menu = dict(
            # type='buttons',
            direction='down',
            active=0,
            xanchor='left', x=0.0,
            yanchor='bottom', y=1.0,
            buttons=[
                dict(label=col, method='update', args=[{'visible': self._buttonVisibility(col, data)}]) for col in loop
            ]
        )
        layout = go.Layout(
            title=f"<b>{self.iloc[0, 0]}({self.index[0]})</b> SIMILARITIES(Q)",
            plot_bgcolor='white',
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=1,
                y=1.04
            ),
            updatemenus=[menu],
            yaxis=dict(
                title='[원, %, 배]',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=1.0
            ),
        )
        fig = go.Figure(
            data=data,
            layout=layout
        )
        return fig