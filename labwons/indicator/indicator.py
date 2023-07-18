from labwons.common.config import PATH
from labwons.indicator.fetch import _fetch
from labwons.equity.technical.lines import line
from plotly import graph_objects as go
from plotly.offline import plot


class Indicator(_fetch):

    def __call__(self) -> go.Scatter:
        return self.trace()

    def trace(self) -> go.Scatter:
        if not hasattr(self, '__trace'):
            self.__setattr__(
                '__trace',
                go.Scatter(
                    name=self.name,
                    x=self.index,
                    y=self.values,
                    visible=True,
                    showlegend=True,
                    mode='lines',
                    connectgaps=True,
                    xhoverformat='%Y/%m/%d',
                    yhoverformat=self.dformat,
                    hovertemplate=self.ticker + '<br>%{y}' + self.unit + '@%{x}<extra></extra>'
                )
            )
        return self.__getattribute__('__trace')

    def figure(self) -> go.Figure:
        layout = go.Layout(
            title=self.name,
            plot_bgcolor='white',
            legend=dict(
                xanchor='left',
                yanchor='top',
                x=0.0,
                y=1.0
            ),
            xaxis=dict(
                title='Date',
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.8,
            ),
            yaxis=dict(
                title=self.unit,
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.8
            )
        )
        fig = go.Figure(data=self.trace(), layout=layout)
        return fig

    def show(self):
        self.figure().show()
        return

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{PATH.BASE}/{self.name}.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return

    @property
    def Monthly(self) -> line:
        series = self.resample('M').ffill()
        series.name = f"{self.name}(M)"
        return line(series, unit=self.unit)

    @property
    def MoM(self) -> line:
        series = 100 * self.resample('M').ffill().pct_change()
        series.name = f"{self.name}(MoM)"
        return line(series, unit='%')

    @property
    def YoY(self) -> line:
        series = 100 * self.resample('M').ffill().pct_change(12)
        series.name = f"{self.name}(YoY)"
        return line(series, unit='%')
