from typing import Union
from labwons.equity.equity import Equity
from labwons.indicator.indicator import Indicator
from plotly import graph_objects as go
from plotly.subplots import make_subplots as subplots


class paper(object):
    xaxis = dict(
        title='Date',
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=0.5,
        zeroline=True,
        zerolinecolor='lightgrey',
        zerolinewidth=0.5
    )
    yaxis = dict(
        showgrid=True,
        gridcolor='lightgrey',
        gridwidth=0.5,
        zeroline=True,
        zerolinecolor='lightgrey',
        zerolinewidth=0.5
    )
    layout = go.Layout(
        plot_bgcolor='white',
        xaxis_rangeslider=dict(visible=False),
        xaxis=xaxis,
        yaxis=yaxis
    )
    _layout_prop = vars(go.Layout)
    def figure1x1(self, **kwargs) -> go.Figure:
        fig = go.Figure(layout=self.layout)
        for k in kwargs:
            if k in self._layout_prop:
                fig.update_layout({k:kwargs[k]})
        return fig

    def figure1x1s(self, **kwargs) -> go.Figure:
        fig = subplots(
            rows=1, cols=1,
            shared_xaxes=True, specs=[[dict(secondary_y=True)]]
        )
        fig.layout = self.layout
        for k in kwargs:
            if k in self._layout_prop:
                fig.update_layout({k:kwargs[k]})
        return fig

# Alias
Paper = paper()