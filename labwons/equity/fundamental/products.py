from labwons.common.config import COLORS
from labwons.equity.refine import _refine
from typing import Union
from plotly import graph_objects as go
from plotly.offline import plot
from urllib.request import urlopen
import pandas as pd
import json



class products(pd.DataFrame):
    def __init__(self, base:_refine):
        """
        Business Model Products
        :return:
                    IM 반도체     CE     DP  기타(계)
        기말
        2019/12  46.56  28.19  19.43  13.48     -7.66
        2020/12  42.05  30.77  20.34  12.92     -6.08
        2021/12  39.07  33.68  19.97  11.34     -4.06
        """
        url = f"http://cdn.fnguide.com/SVO2//json/chart/02/chart_A{base.ticker}_01_N.json"
        src = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'), strict=False)
        header = pd.DataFrame(src['chart_H'])[['ID', 'NAME']].set_index(keys='ID').to_dict()['NAME']
        header.update({'PRODUCT_DATE': '기말'})
        basis = pd.DataFrame(src['chart']).rename(columns=header).set_index(keys='기말')
        basis = basis.drop(columns=[c for c in basis.columns if basis[c].astype(float).sum() == 0])

        i = basis.columns[-1]
        basis['Sum'] = basis.astype(float).sum(axis=1)
        basis = basis[(90 <= basis.Sum) & (basis.Sum < 110)].astype(float)
        basis[i] = basis[i] - (basis.Sum - 100)
        basis = basis.drop(columns=['Sum'])

        super().__init__(
            index=basis.index,
            columns=basis.columns,
            data=basis.values
        )
        self._base_ = base
        return

    def __call__(self, mode:str='bar'):
        return self.trace(mode)

    def recent(self) -> pd.Series:
        i = -1 if self.iloc[-1].astype(float).sum() > 10 else -2
        df = self.iloc[i].T.dropna().astype(float)
        df = df.drop(index=df[df < 0].index)
        df[df.index[i]] += (100 - df.sum())
        return df[df.values != 0]

    def trace(self, mode:str='bar') -> Union[list, go.Bar, go.Pie]:
        if mode == 'bar':
            return [
                go.Bar(
                    name=f"{c}",
                    x=self.index,
                    y=self[c],
                    showlegend=True,
                    legendgroup=c,
                    visible=True,
                    marker=dict(
                        color=COLORS[n]
                    ),
                    opacity=0.9,
                    textposition="inside",
                    texttemplate=c + "<br>%{y:.2f}%",
                    hovertemplate=c + "<br>%{y:.2f}%<extra></extra>"
                ) for n, c in enumerate(self.columns)
            ]
        else:
            df = self.recent()
            return [
                go.Pie(
                    labels=df.index,
                    values=df,
                    showlegend=True,
                    visible=True,
                    automargin=True,
                    opacity=0.9,
                    textfont=dict(
                        color='white'
                    ),
                    textinfo='label+percent',
                    insidetextorientation='radial',
                    hoverinfo='label+percent',
                )
            ]


    def figure(self) -> go.Figure:
        fig = go.Figure(
            data=self.trace(),
            layout=go.Layout(
                title=f"<b>{self._base_.name}({self._base_.ticker})</b> Products",
                plot_bgcolor='white',
                barmode='stack',
                legend=dict(
                    orientation="h",
                    xanchor="right",
                    yanchor="bottom",
                    x=0.96,
                    y=1
                ),
                xaxis=dict(
                    title='기말'
                ),
                yaxis=dict(
                    title='비율 [%]',
                    showgrid=True,
                    gridcolor='lightgrey',
                    zeroline=True,
                    zerolinecolor='lightgrey'
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
            filename=f'{self._base_.path}/PRODUCTS.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return