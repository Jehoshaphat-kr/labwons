from nohji.util.chart import r2c2nsy

from pandas import DataFrame, Series
from plotly.graph_objects import Bar, Figure


class benchmarkMultiples:

    colors = ['royalblue', "#9BC2E6", "#A9D08E"]

    def __init__(self, benchmark:DataFrame, meta: Series):
        if meta.country == "KOR":
            self.data = benchmark.copy()
        elif meta.country == "USA":
            self.data = benchmark.copy()
        else:
            raise AttributeError
        self.meta = meta
        self.title = f"{meta['name']}({meta.name}) : Benchmark Multiples"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    def figure(self, **kwargs) -> Figure:
        fig = r2c2nsy(
            subplot_titles=[col[0] for n, col in enumerate(self.data) if not n % 3],
            vertical_spacing=0.1,
            horizontal_spacing=0.08,
        )
        for n, col in enumerate(self.data):
            unit = '' if col[0].startswith('PER') or col[0].startswith('EV') else '%'
            data = self.data[col]
            trace = Bar(
                name=col[1],
                x=data.index,
                y=data,
                visible=True,
                showlegend=True if n < 3 else False,
                legendgroup=col[1],
                marker=dict(color=self.colors[n % 3]),
                hovertemplate=col[1] + ": %{y}" + unit + "<extra></extra>"
            )
            row = 1 if col[0].startswith('PER') or col[0].startswith('EV') else 2
            col = 1 if col[0].startswith('PER') or col[0].startswith('ROE') else 2
            fig.add_trace(row=row, col=col, trace=trace)

        # fig.update_layout(title=self.title, legend=dict(y=1.025), **kwargs)
        fig.update_layout(
            title=self.title,
            legend={
                "orientation": "v",
                "yanchor": "bottom",
                "x": 0.99, "y": 0.01
            },
            **kwargs
        )
        fig.update_yaxes(row=1, col=1, title='[-]')
        fig.update_yaxes(row=1, col=2, title='[-]')
        fig.update_yaxes(row=2, col=1, title='[%]')
        fig.update_yaxes(row=2, col=2, title='[%]')
        return fig
