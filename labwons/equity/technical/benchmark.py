from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from datetime import timedelta
import plotly.graph_objects as go
import pandas as pd


class benchmark(baseDataFrameChart):

    def __init__(self, base: fetch):
        close = pd.concat(objs={base.name: base.ohlcv.c, base.benchmarkName: base.benchmark.close}, axis=1)
        objs = {}
        for yy in [5, 3, 2, 1, 0.5]:
            col = f"{yy}Y" if isinstance(yy, int) else f"{int(yy * 12)}M"
            date = close.index[-1] - timedelta(int(yy * 365))
            data = close[close.index >= date].dropna()
            objs[col] = 100 * ((data.pct_change().fillna(0) + 1).cumprod() - 1)

        super(benchmark, self).__init__(
            data=pd.concat(objs=objs, axis=1),
            name="BENCHMARK",
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
        for n, col in enumerate(self):
            if n % 2: continue
            step = dict(
                method='update',
                label=col[0],
                args=[
                    dict(visible=[True if i in [n, n + 1] else False for i in range(len(self.columns))]),
                    dict(title=f"<b>{self.subject}</b> :  Relative Returns - {col[0]}")
                ]
            )
            steps.append(step)
        slider = [dict(active=0, currentvalue=dict(prefix="Period: "), pad=dict(t=50), steps=steps)]
        return slider

    def figure(self) -> go.Figure:
        fig = Chart.r1c1nsy()
        for col in self:
            fig.add_trace(self(
                col=col, name=col[1],
                visible=True if col in self.columns[:2] else False,
                line=dict(
                    color='royalblue' if col[1] == self.ref.name else 'grey',
                    dash='solid'
                )
            ))
        fig.update_layout(
            title=f"<b>{self.subject}</b> :  Relative Returns - {self.columns[0][0]}",
            sliders=self.sliders
        )
        fig.update_xaxes(rangeselector=None)
        return fig

