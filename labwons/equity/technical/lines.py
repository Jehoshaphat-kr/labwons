from labwons.common.config import PATH
from plotly import graph_objects as go
from plotly.offline import plot
from pandas import Series, DataFrame

class line(Series):
    _attr_ = None
    def __init__(self, base:Series, **kwargs):
        super().__init__(
            index=base.index,
            data=base.values,
            name=base.name
        )
        self._attr_ = kwargs
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
        for key in self._attr_:
            if key in vars(go.Scatter).keys():
                setattr(_trace, key, self._attr_[key])
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
                title=self._attr_['unit'],
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.8
            )
        )
        for key in self._attr_:
            if key in vars(go.Layout).keys():
                setattr(layout, key, self._attr_[key])
        fig = go.Figure(data=self.trace(), layout=layout)
        return fig

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{self._base_.path}/{setter["name"] if "name" in setter else "_"}.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return

    def show(self):
        self.figure().show()
        return


class lines(DataFrame):
    _base_ = None
    _attr_ = None
    def __init__(self, data:DataFrame, base=None, **kwargs):
        data = data.copy()
        super().__init__(
            index=data.index,
            columns=data.columns,
            data=data.values
        )
        self._base_ = base
        self._attr_ = kwargs.copy()
        return

    def trace(self, col:str) -> go.Scatter:
        _trace = go.Scatter(
            name=f'{col}',
            x=self.index,
            y=self[col],
            visible=True,
            showlegend=True,
            connectgaps=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat='.2f',
        )
        for key in self._attr_:
            if key in vars(go.Scatter).keys():
                setattr(_trace, key, self._attr_[key])
        return _trace

    def traces(self) -> list:
        return [self.trace(col) for col in self.columns]

    def figure(self) -> go.Figure:
        layout = go.Layout(
            title=f"{self._base_.name}({self._base_.ticker}): "
                  f"{self._attr_['title'] if 'title' in self._attr_ else ''}",
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
                title=self._base_.unit,
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.8
            )
        )
        for key in self._attr_:
            if key in vars(go.Layout).keys():
                setattr(layout, key, self._attr_[key])
        fig = go.Figure(data=self.traces(), layout=layout)
        return fig

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f"{self._base_.path}/{self._attr_['title'] if 'title' in self._attr_ else ''}.html"
        )
        kwargs.update(setter)
        plot(**kwargs)
        return

    def show(self):
        self.figure().show()
        return
