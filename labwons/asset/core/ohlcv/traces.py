from pandas import DataFrame
from plotly.graph_objects import Bar, Candlestick
from typing import Union, Hashable


class traces(object):

    def __init__(self, data:DataFrame, name:Union[str, Hashable]):
        if not all([c in data.columns for c in ['open', 'high', 'low', 'close', 'volume']]):
            raise ValueError(f"Candlestick requires ['open', 'high', 'low', 'close', 'volume'] column data")

        self.data = data.dropna()
        self.name = name
        return

    def __call__(self, item:str, **kwargs):
        trace = getattr(self, item)
        for key, value in kwargs.items():
            try:
                setattr(trace, key, value)
            except (AttributeError, KeyError, ValueError, TypeError):
                continue
        return trace

    @property
    def ohlc(self) -> Candlestick:
        if not hasattr(self, "_ohlc"):
            dtype = ".2f" if isinstance(self.data[self.data.columns[0]], float) else ",d"
            trace = Candlestick(
                name=self.name,
                x=self.data.index,
                open=self.data.open,
                high=self.data.high,
                low=self.data.low,
                close=self.data.close,
                visible=True,
                showlegend=True,
                increasing_line=dict(
                    color='red'
                ),
                decreasing_line=dict(
                    color='royalblue'
                ),
                hoverinfo='x+y',
                xhoverformat='%Y/%m/%d',
                yhoverformat=dtype,
            )
            setattr(self, "_ohlc", trace)
        return getattr(self, "_ohlc")

    @property
    def vol(self) -> Bar:
        if not hasattr(self, "_vol"):
            trace = Bar(
                name="Vol.",
                x=self.data.index,
                y=self.data.volume,
                visible=True,
                showlegend=False,
                marker={
                    "color": self.data.apply(lambda r: "red" if r["close"] >= r["open"] else "royalblue", axis=1)
                },
                xhoverformat='%Y/%m/%d',
                yhoverformat=',d',
                hovertemplate=self.name + ": %{y}<extra></extra>",
            )
            setattr(self, "_vol", trace)
        return getattr(self, "_vol")
