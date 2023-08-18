from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from urllib.request import urlopen
import pandas as pd
import json



class products(baseDataFrameChart):
    def __init__(self, base:fetch):
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

        super().__init__(basis.drop(columns=['Sum']), **getattr(base, '_valid_prop'))
        self._base_ = base
        self._filename_ = 'Products'
        return

    def __call__(self, col:str='bar'):
        return self.bar(col)

    def recent(self) -> pd.Series:
        i = -1 if self.iloc[-1].astype(float).sum() > 10 else -2
        df = self.iloc[i].T.dropna().astype(float)
        df = df.drop(index=df[df < 0].index)
        df[df.index[i]] += (100 - df.sum())
        return df[df.values != 0]

    def pie(self) -> go.Pie:
        df = self.recent()
        return go.Pie(
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

    def figure(self) -> go.Figure:
        fig = go.Figure(
            data=[self.pie()],
            layout=go.Layout(
                title=f"<b>{self._base_.name}({self._base_.ticker})</b> Products",
                plot_bgcolor='white',
                legend=dict(
                    orientation="h",
                    xanchor="right",
                    yanchor="bottom",
                    x=0.96,
                    y=1
                ),
            )
        )
        return fig