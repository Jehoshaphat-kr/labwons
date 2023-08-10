from labwons.common.config import PATH, COLORS
from labwons.equity._deprecated import _calc
from datetime import timedelta
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import random


def _days_far(series:pd.Series or pd.DataFrame, days:list) -> list:
    return [(series.index >= (series.index[-1] - timedelta(day)), tag, day) for tag, day in days]


class benchmark(pd.DataFrame):

    def __init__(self, base:_calc):
        """
        Relative return in given period (3M / 6M / 1Y / 2Y / 3Y / 5Y), start normalized with 0%
        :return:
                                    3M                  6M                  1Y                  3Y                  5Y
                    SK hynix     KODEX  SK hynix     KODEX  SK hynix     KODEX  SK hynix     KODEX  SK hynix     KODEX
        date
        2018-06-28       NaN       NaN       NaN       NaN       NaN       NaN       NaN       NaN  0.000000  0.000000
        2018-06-29       NaN       NaN       NaN       NaN       NaN       NaN       NaN       NaN  0.026347  0.009952
        2018-07-02       NaN       NaN       NaN       NaN       NaN       NaN       NaN       NaN  0.002395 -0.025224
        2018-07-03       NaN       NaN       NaN       NaN       NaN       NaN       NaN       NaN  0.031138 -0.004719
        2018-07-04       NaN       NaN       NaN       NaN       NaN       NaN       NaN       NaN  0.017964 -0.004075
        ...              ...       ...       ...       ...       ...       ...       ...       ...       ...       ...
        2023-06-21  0.346199  0.175589  0.494805  0.391603  0.211579  0.122402  0.376794  0.308945  0.378443  0.362232
        2023-06-22  0.333333  0.169480  0.480519  0.384373  0.200000  0.116570  0.363636  0.302143  0.365269  0.355154
        2023-06-23  0.328655  0.171701  0.475325  0.387002  0.195789  0.118691  0.358852  0.304617  0.360479  0.357728
        2023-06-26  0.327485  0.188731  0.474026  0.407161  0.194737  0.134950  0.357656  0.323578  0.359281  0.377461
        2023-06-27  0.321637  0.182623  0.467532  0.399930  0.189474  0.129118  0.351675  0.316777  0.353293  0.370383
        """
        data = base.calcBenchmark().copy()
        days = _days_far(data, [('3M', 92), ('6M', 183), ('1Y', 365), ('3Y', 1095), ('5Y', 1825)])
        objs = {tag: (data[cond]['close'].pct_change().fillna(0) + 1).cumprod() - 1 for cond, tag, _ in days}
        data = 100 * pd.concat(objs=objs, axis=1)
        super().__init__(data=data.values, index=data.index, columns=data.columns)
        self._base_ = base
        self._color1 = COLORS.pop(random.randint(0, len(COLORS)))
        self._color2 = COLORS.pop(random.randint(0, len(COLORS)))
        return

    def trace(self, col:tuple) -> go.Scatter:
        data = self[~self[col].isna()].copy()
        return go.Scatter(
            name=col[1],
            x=data.index,
            y=data[col],
            visible=True if col[0] == '3M' else False,
            showlegend=True,
            line=dict(
                color=self._color1 if col[1] == self._base_.name else self._color2
            ),
            hovertemplate=f"{col[1]}<br>" + "%{y}% @%{x}<extra></extra>"
        )

    def traces(self, key:tuple=None) -> go.Scatter or list:
        if key in self.columns:
            return self.trace(key)

        if not key:
            return [self.trace(col) for col in self.columns]
        raise KeyError(f"Key Error: {key}")

    def _slider(self) -> list:
        steps = []
        for n, col in enumerate(self.columns):
            if n % 2:
                continue
            label = col[0].replace('M', '개월').replace('Y', '년')
            step = dict(
                method='update',
                label=label,
                args=[
                    dict(visible=[True if (i == n) or (i == n+1) else False for i in range(len(self.columns))]),
                    dict(title=f"{self._base_.name}({self._base_.ticker}) Relative Returns: {label}")
                ]
            )
            steps.append(step)
        slider = [dict(active=0, currentvalue=dict(prefix="비교 기간: "), pad=dict(t=50), steps=steps)]
        return slider

    def figure(self) -> go.Figure:
        data = self.traces()
        fig = go.Figure(data=data)
        fig.update_layout(
            # title=f"{self._base_.name}({self._base_.ticker}) Relative Returns",
            plot_bgcolor="white",
            sliders=self._slider(),
            hovermode='x unified',
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

    def show(self):
        self.figure().show()
        return

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{self._base_.path}/RELATIVE.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return