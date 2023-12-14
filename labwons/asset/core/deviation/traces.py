from pandas import DataFrame, Series
from plotly.graph_objects import Bar


class traces(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data
        self.meta = meta
        return

    def __getattr__(self, item:str) -> Bar:
        data = Series()
        for col in self.data:
            if col in item:
                data = self.data[col].dropna()
                break

        if not data.empty:
            return Bar(
                name=data.name,
                x=data.index,
                y=data,
                visible=True,
                showlegend=False,
                marker={
                    "color": data.apply(lambda x: "red" if x >= 0 else "royalblue")
                },
                xhoverformat='%Y/%m/%d',
                yhoverformat=".2d",
                hovertemplate=str(data.name) + ": %{y}<extra></extra>",
            )
        if not item in dir(self):
            raise AttributeError

    @property
    def all(self) -> list:
        return [getattr(self, f"D{col}") for col in self.data]

