from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from datetime import timedelta
import plotly.graph_objects as go
import pandas as pd


class performance(baseDataFrameChart):

    settings = None
    steps = [5, 3, 2, 1, 0.5]
    def __init__(self, slots:dict, settings:dict):
        self.settings = settings
        base = list(slots.values())[0]
        close = pd.concat(objs={e.name: e.ohlcv.c for e in slots.values()}, axis=1)
        objs = {}
        for yy in self.steps:
            col = f"{yy}Y" if isinstance(yy, int) else f"{int(yy * 12)}M"
            date = close.index[-1] - timedelta(int(yy * 365))
            data = close[close.index >= date].dropna()
            objs[col] = 100 * ((data.pct_change().fillna(0) + 1).cumprod() - 1)

        super(performance, self).__init__(
            data=pd.concat(objs=objs, axis=1),
            name="RETURNS",
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            form='.2f',
            unit='%',
            ref=base
        )
        return

    @property
    def sliders(self) -> list:
        steps = []
        for n, yy in enumerate(self.steps):
            label = f"{yy}Y" if isinstance(yy, int) else f"{int(yy * 12)}M"
            visible = [True if col[0] == label else False for col in self]
            steps.append(dict(
                method="update",
                label=label,
                args=[
                    dict(visible=visible),
                    dict(title=f"<b>{self.subject}</b> : Relative Returns - {label}")
                ]
            ))
        slider = [dict(active=0, currentvalue=dict(prefix="Period: "), pad=dict(t=50), steps=steps)]
        return slider

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r1c1nsy()
        for n, col in enumerate(self):
            fig.add_trace(self(
                col=col, name=col[1],
                visible=True if n < (len(self.columns) / len(self.steps)) else False,
                line=dict(
                    color=self.settings["color"][col[1]],
                    dash='solid'
                )
            ))
        fig.update_layout(
            title=f"<b>{self.subject}</b> :  Relative Returns - {self.columns[0][0]}",
            sliders=self.sliders,
            **kwargs
        )
        fig.update_xaxes(rangeselector=None)
        fig.update_yaxes(title="수익률 [%]", zerolinewidth=1.8)
        return fig

