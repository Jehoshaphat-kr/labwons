from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from datetime import timedelta
import plotly.graph_objects as go
import pandas as pd


class benchmark(baseDataFrameChart):
    _base_ = None
    def __init__(self, base: fetch):
        objs = dict()
        for col in base.ohlcv:
            objs[(col, base.name)] = base.ohlcv[col]
            objs[(col, base.benchmarkName)] = base.benchmark[col]
        frame = pd.concat(objs=objs, axis=1)

        days = self._days_far(frame, [('3M', 92), ('6M', 183), ('1Y', 365), ('3Y', 1095), ('5Y', 1825)])
        objs = {tag: (frame[cond]['close'].pct_change().fillna(0) + 1).cumprod() - 1 for cond, tag, _ in days}
        super().__init__(100 * pd.concat(objs=objs, axis=1), **getattr(base, '_valid_prop'))

        self._base_ = base
        self._form_ = '.2f'
        self._unit_ = '%'
        self._filename_ = 'Benchmark Relative Returns'
        return

    @staticmethod
    def _days_far(series:pd.Series or pd.DataFrame, days:list) -> list:
        return [(series.index >= (series.index[-1] - timedelta(day)), tag, day) for tag, day in days]

    @property
    def _sliders(self) -> list:
        steps = []
        for n, col in enumerate(self):
            if n % 2:
                continue
            step = dict(
                method='update',
                label=col[0],
                args=[
                    dict(visible=[True if (i == n) or (i == n+1) else False for i in range(len(self.columns))]),
                    # dict(title=f"{self._base_.name}({self._base_.ticker}) Relative Returns: {label}")
                ]
            )
            steps.append(step)
        slider = [dict(active=0, currentvalue=dict(prefix="비교 기간: "), pad=dict(t=50), steps=steps)]
        return slider

    def figure(self) -> go.Figure:
        data = [
            self.line(
                col,
                visible=True if col[0] == '3M' else False,
                line=dict(
                    color='royalblue' if col[1] == self._base_.name else 'black',
                    dash='solid' if col[1] == self._base_.name else 'dot'
                ),
                hovertemplate=col[1] + '<br>%{y}' + self._unit_ + '@%{x}<extra></extra>'
            ) for col in self
        ]

        fig = go.Figure(data=data)
        fig.update_layout(
            # title=f"{self._base_.name}({self._base_.ticker}) Relative Returns",
            plot_bgcolor="white",
            sliders=self._sliders,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=0.98,
                y=1.02
            ),
            xaxis_rangeslider=dict(visible=False),
            xaxis=dict(
                title="DATE",
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
                title=f"[%]",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                zeroline=True,
                zerolinecolor="grey",
                zerolinewidth=1.0,
                mirror=False,
                autorange=True
            )
        )
        return fig
