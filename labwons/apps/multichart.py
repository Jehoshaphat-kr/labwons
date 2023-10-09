from labwons.common.config import PATH
from labwons.equity.equity import Equity
from labwons.indicator import Indicator
from plotly.subplots import make_subplots
from plotly.offline import plot
import plotly.graph_objects as go


class MultiChart(object):

    def __init__(self, *args):
        self.args = args
        self.units = list()
        for arg in args:
            if not arg.unit in self.units:
                self.units.append(arg.unit)
        if len(self.units) > 2:
            raise ValueError('The number of units of given object is more than 2. Unable to express dimensions')
        self._n_equity = len([arg for arg in args if isinstance(arg, Equity)])
        self._trs = list()
        self._ys = list()
        return

    @staticmethod
    def f1x1y2() -> go.Figure:
        fig = make_subplots(
            rows=1, cols=1,
            x_title='날짜', shared_xaxes=True,
            specs=[
                [{'secondary_y': True}]
            ]
        )
        fig.update_layout(
            plot_bgcolor='white',
            margin=dict(r=0),
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=0.96,
                y=1
            ),
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
            hovermode="x unified",
            xaxis=dict(
                tickformat="%Y/%m/%d",
                showticklabels=True,
                showgrid=True,
                gridcolor='lightgrey',
            ),
            yaxis=dict(
                # title=f'[{self.units[0]}]',
                showgrid=True,
                gridcolor='lightgrey',
            ),
            yaxis2=dict(
                # title=f'[{self.units[1]}]'
            )
        )
        return fig


    def _traces(self) -> list:
        if self._trs:
            return self._trs
        for elem in self.args:
            if isinstance(elem, Equity):
                if self._n_equity == 1:
                    ohlc = elem.ohlcv()
                    ohlc.showlegend = True
                    self._trs.append(ohlc)
                    self._ys.append(False if elem.unit == self.units[0] else True)
                typical = elem.typical(
                    line=dict(
                        color='black' if self._n_equity == 1 else None,
                        dash='dot' if self._n_equity == 1 else 'solid',
                        width=0.8 if self._n_equity == 1 else 1.0
                    )
                )
                self._trs.append(typical)
            elif isinstance(elem, Indicator):
                self._trs.append(elem())
            self._ys.append(False if elem.unit == self.units[0] else True)
        return self._trs

    def figure(self) -> go.Figure:
        if len(self.units) > 1:
            fig = self._figSeparate()
        else:
            fig = self._figUniform()
        return fig

    def _figUniform(self) -> go.Figure:
        fig = go.Figure(
            data=self._traces(),
            layout=go.Layout(
                title=", ".join([arg.name for arg in self.args]),
                plot_bgcolor="white",
                legend=dict(
                    orientation="h",
                    xanchor="right",
                    yanchor="bottom",
                    x=0.98,
                    y=1.02
                ),
                hovermode="x unified",
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
                    title="Date",
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
                    title=f"[{self.units[0]}]",
                    showgrid=True,
                    gridwidth=0.5,
                    gridcolor="lightgrey",
                    showline=True,
                    linewidth=1,
                    linecolor="grey",
                    mirror=False,
                    autorange=True
                ),
            )
        )
        return fig

    def _figSeparate(self) -> go.Figure:
        fig = make_subplots(
            rows=1, cols=1,
            x_title='날짜', shared_xaxes=True,
            specs=[
                [{'secondary_y': True}]
            ]
        )
        fig.add_traces(
            data=self._traces(),
            rows=[1] * len(self._traces()),
            cols=[1] * len(self._traces()),
            secondary_ys=self._ys
        )
        fig.update_layout(
            title=", ".join([arg.name for arg in self.args]),
            plot_bgcolor='white',
            margin=dict(r=0),
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=0.96,
                y=1
            ),
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
            hovermode="x unified",
            xaxis=dict(
                tickformat="%Y/%m/%d",
                showticklabels=True,
                showgrid=True,
                gridcolor='lightgrey',
            ),
            yaxis=dict(
                title=f'[{self.units[0]}]',
                showgrid=True,
                gridcolor='lightgrey',
            ),
            yaxis2=dict(
                title=f'[{self.units[1]}]'
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
            filename=f'{PATH.BASE}/f{"_".join([arg.name for arg in self.args])}.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return