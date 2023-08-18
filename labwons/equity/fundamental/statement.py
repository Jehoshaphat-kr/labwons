from labwons.common.basis import baseDataFrameChart
from labwons.common.tools import int2won
from plotly import graph_objects as go
import pandas as pd


class statement(baseDataFrameChart):
    def __init__(self, basis:pd.DataFrame, **kwargs):
        """
        Statement
        :return:
        """
        n = len(basis) - len([i for i in basis.index if i.endswith(')')])
        basis = basis.head(n + 1)
        basis.index.name = '기말'
        super().__init__(basis, **kwargs)
        for k in kwargs:
            if k in self._prop_:
                self._prop_[k] = kwargs[k]
        return

    def __call__(self, col:str, **kwargs):
        return self.linemarker(col, **kwargs)

    def _meta(self, col:str) -> list:
        idx = self.columns.tolist().index(col)
        if idx <= 11:
            return [int2won(x) for x in self[col]]
        elif idx <= 17 or idx == 24:
            return [f'{x}%' for x in self[col]]
        elif idx <= 20:
            return [f'{x}원' for x in self[col]]
        else:
            return [f'{x}' for x in self[col]]

    def figure(self) -> go.Figure:
        data = [
            self.linemarker(
                col,
                visible=False if n else True,
                showlegend=False,
                meta=self._meta(col),
                texttemplate='%{meta}',
                hovertemplate='%{meta}'
            )
            for n, col in enumerate(self)
        ]
        buttons = list()
        for n, tr in enumerate(data):
            visible = [False] * len(data)
            visible[n] = True
            buttons.append(
                dict(
                    label=tr.name,
                    method="update",
                    args=[{"visible": visible}]
                )
            )
        fig = go.Figure(
            data=data,
            layout=go.Layout(
                title=f"<b>{self._dataName_}({self._ticker_})</b> Financial Statement",
                plot_bgcolor='white',
                updatemenus=[
                    dict(
                        # type="buttons",
                        direction="down",
                        active=0,
                        xanchor='left', x=0.0,
                        yanchor='bottom', y=1.0,
                        buttons=buttons
                    )
                ],
                xaxis=dict(
                    title='기말',
                    showticklabels=True,
                    showgrid=False,
                ),
                yaxis=dict(
                    title='[억원, -, %]',
                    showgrid=True,
                    gridcolor='lightgrey'
                ),
            )
        )
        return fig
