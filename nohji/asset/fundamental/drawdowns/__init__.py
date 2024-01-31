from nohji.util.chart import r1c1nsy
from nohji.asset.fundamental.drawdowns import data

from pandas import DataFrame, Series
from plotly.graph_objects import Figure, Scatter


class drawDown:
    colors = ["royalblue", "red", "green", "purple", "orange", "grey"]

    def __init__(self, resembles:DataFrame, meta: Series):
        if meta.country == "KOR":
            self.data = data.genKr(resembles, meta)
        elif meta.country == "USA":
            self.data = data.genKr(resembles, meta)
        else:
            raise AttributeError
        self.meta = meta
        self.title = f"{meta['name']}({meta.name}) : Draw Down"

        self.periods = []
        self.assets = []
        for col in self.data:
            if not col[0] in self.periods:
                self.periods.append(col[0])
            if not col[1] in self.assets:
                self.assets.append(col[1])
        self.n_asset = len(self.assets)
        return

    def __str__(self) -> str:
        return str(self.data)

    def __call__(self, **kwargs):
        self.figure(**kwargs).show()
        return

    @property
    def sliders(self) -> list:
        steps = []
        for n, col in enumerate(self.data.columns):
            if n % self.n_asset: continue
            step = dict(
                method='update',
                label=col[0],
                args=[
                    dict(visible=[True if i in range(n, n + self.n_asset) else False for i in range(len(self.data.columns))]),
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
                    "dash": "solid" if ticker == self.meta.ticker else "dash",
                    "color": self.colors[int(self.data.columns.tolist().index(col) % self.n_asset)]
                },
                connectgaps=True,
                visible=True if yy == self.periods[0] else False,
                showlegend=True,
                xhoverformat="%Y/%m/%d",
                yhoverformat=".2f",
                hovertemplate=name.split("_")[0] + ": %{y}%<extra></extra>"
            )
            fig.add_trace(trace=trace)
        fig.add_hline(y=0, line_width=1.0, line_color="grey")
        fig.update_layout(title=f"{self.title} - {self.periods[0]}", sliders=self.sliders)
        fig.update_yaxes(title="낙폭 [%]")
        return fig

