from labwons.common.charts import r2c1nsy
from labwons.common.traces import candleStick, barTY
from pandas import DataFrame


class ohlcv(r2c1nsy):

    class _traces(object):
        def __init__(self, data:DataFrame, name:str):
            color = data.apply(lambda r: "red" if r["close"] >= r["open"] else "royalblue", axis=1)
            self.ohlc = candleStick(data, name)
            self.volume = barTY(data.volume, showlegend=False, marker={"color": color.values})
            return
    traces:_traces = None

    def __init__(self, data: DataFrame, name: str, ticker:str):
        super().__init__()
        self.traces = traces = self._traces(data, name)
        self.add_trace(row=1, col=1, trace=traces.ohlc)
        self.add_trace(row=2, col=1, trace=traces.volume)
        self.update_layout(title=f"<b>{name}({ticker})</b> : OHLCV")
        return

    def __call__(self, **kwargs):
        self.update_layout(**kwargs)
        self.show()
        return

