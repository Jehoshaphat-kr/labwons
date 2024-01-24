from nohji.util.chart import r1c1nsy
from nohji.asset.fundamental.benchmarks import data

from pandas import DataFrame, Series
from plotly.graph_objects import Figure, Scatter


class benchmarks:
    colors = ["royalblue", "red", "green", "purple", "orange", "grey"]

    def __init__(self, resembles:DataFrame, meta: Series):
        if meta.country == "KOR":
            self.data = data.genKr(resembles)
        elif meta.country == "USA":
            self.data = data.genKr(resembles)
        else:
            raise AttributeError
        self.meta = meta
        self.title = f"{meta['name']}({meta.name}) : Relative Returns"
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    @property
    def sliders(self) -> list:
        asset = int(len(self.data.columns) / 6)
        steps = []
        for n, col in enumerate(self.data.columns):
            if n % asset: continue
            step = dict(
                method='update',
                label=col[0],
                args=[
                    dict(visible=[True if i in range(n, n + asset) else False for i in range(len(self.data.columns))]),
                    dict(title=f"{self.title} - {col[0]}"),
                ]
            )
            steps.append(step)
        slider = [dict(active=0, currentvalue=dict(prefix="Period: "), pad=dict(t=50), steps=steps)]
        return slider

    def figure(self, **kwargs) -> Figure:
        fig = r1c1nsy(**kwargs)
        for col in self.data.columns:
            data = self.data[col].dropna()
            yy, column = col
            name, ticker = tuple(column.split("_"))
            trace = Scatter(
                name=name,
                x=data.index,
                y=data,
                mode="lines",
                line={
                    "dash": "solid" if ticker == self.data.ticker else "dash",
                    "color": self.colors[self.data.columns.tolist().index(col) % self.nAsset]
                },
                connectgaps=True,
                visible=True if yy == "5Y" else False,
                showlegend=True,
                xhoverformat="%Y/%m/%d",
                yhoverformat=".2f",
                hovertemplate=name.split("_")[0] + ": %{y}%<extra></extra>"
            )
            fig.add_trace(trace=trace)
        fig.add_hline(y=0, line_width=1.0, line_color="grey")
        fig.update_layout(title=f"{self.title} - 5Y", sliders=self.sliders)
        fig.update_yaxes(title="수익률 [%]")
        return fig

