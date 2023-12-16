from pandas import DataFrame, Series
from plotly.graph_objects import Scatter


class traces(object):

    def __init__(self, data:DataFrame):
        self.data = data
        self.opt = {
            "rsi": {
                "name": "RSI",
                "unit": "%"
            },
            "stoch_osc": {
                "name": "S.OSC",
                "unit":"%",
            },
            "stoch_osc_sig": {
                "name": "S.OSC-Sig",
                "unit": "%",
                "line": {
                    "dash": "dash"
                }
            },
            "stoch_rsi": {
                "name": "S.RSI",
                "unit": ""
            },
            "stoch_rsi_k": {
                "name": "S.RSI-K",
                "unit": ""
            },
            "stoch_rsi_d": {
                "name": "S.RSI-D",
                "unit": ""
            },

        }
        return

    def __line__(self, column:str, **kwargs) -> Scatter:
        name = kwargs["name"] if "name" in kwargs else column
        unit = kwargs["unit"] if "unit" in kwargs else ""
        trace = Scatter(
            name="middle",
            x=self.data.index,
            y=self.data[column],
            mode="lines",
            visible=True,
            showlegend=False,
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate=name + ": %{y}" + unit + "<extra></extra>"
        )
        for key, value in kwargs.items():
            try:
                setattr(trace, key, value)
            except (AttributeError, KeyError, TypeError, ValueError):
                continue
        return trace

    def __getattr__(self, item:str):
        if not item in self.data:
            raise KeyError
        return self.__line__(item, **self.opt[item])



