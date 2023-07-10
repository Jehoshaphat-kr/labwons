from labwons.common.config import DESKTOP
from labwons.equity.refine import _refine
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from pandas import DataFrame

class ohlcv(DataFrame):
    def __init__(self, base:_refine):
        baseData = base.getOhlcv()
        super().__init__(
            index=baseData.index,
            columns=baseData.columns,
            data=baseData.values
        )
        self._base_ = base
        return

    def __call__(self):
        return

    def traceCandle(self) -> go.Candlestick:
        return go.Candlestick(
            name=f'{self._base_.name}',
            x=self.index,
            open=self['open'],
            high=self['high'],
            low=self['low'],
            close=self['close'],
            visible=True,
            showlegend=False,
            increasing_line=dict(
                color='red'
            ),
            decreasing_line=dict(
                color='royalblue'
            ),
            xhoverformat='%Y/%m/%d',
            yhoverformat=self._base_.dtype,
        )

    def traceBar(self):
        series = self['volume']
        return go.Bar(
            name=series.name,
            x=series.index,
            y=series,
            visible=True,
            showlegend=False,
            xhoverformat='%Y/%m/%d',
            marker=dict(color=series.pct_change().apply(lambda x: 'royalblue' if x < 0 else 'red')),
            hovertemplate='%{y} @%{x}<extra></extra>'
        )

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            row_width=[0.15, 0.85],
            vertical_spacing=0.01
        )
        fig.add_traces(data=[self.traceCandle(), self.traceBar()], rows=[1, 2], cols=[1, 1])
        fig.update_layout(
            title=f"{self._base_.name}({self._base_.ticker}) OHLCV",
            plot_bgcolor="white",
            # legend=dict(tracegroupgap=5),
            xaxis_rangeslider=dict(visible=False),
            xaxis_rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=2, label="3Y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            xaxis=dict(
                title="",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            xaxis2=dict(
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
                title=f"[{self._base_.unit}]",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            yaxis2=dict(
                title=f"",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            )
        )
        return fig

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{DESKTOP}/{self._base_.ticker}_{self._base_.name}_OHLCV.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return

