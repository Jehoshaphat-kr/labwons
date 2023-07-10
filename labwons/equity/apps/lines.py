from labwons.common.config import DESKTOP
from plotly import graph_objects as go
from plotly.offline import plot
from pandas import Series

class lines(Series):
    def __init__(self, base:Series, **kwargs):
        super().__init__(
            index=base.index,
            data=base.values,
            name=base.name
        )
        self._kwargs = kwargs
        return

    def __call__(self) -> go.Scatter:
        return self.trace()

    def trace(self) -> go.Scatter:
        _trace = go.Scatter(
            name=f'{self.name}',
            x=self.index,
            y=self,
            visible=True,
            showlegend=True,
            connectgaps=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat='.2f',
        )
        for key in self._kwargs:
            if key in vars(go.Scatter).keys():
                setattr(_trace, key, self._kwargs[key])
        return _trace

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
                title=self._kwargs['unit'],
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.8
            )
        )
        for key in self._kwargs:
            if key in vars(go.Layout).keys():
                setattr(layout, key, self._kwargs[key])
        fig = go.Figure(data=self.trace(), layout=layout)
        return fig

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{DESKTOP}/{self._base_.ticker}_{self._base_.name}.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return

    def show(self):
        self.figure().show()
        return

