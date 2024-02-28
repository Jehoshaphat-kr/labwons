from labwons.asset.core.ohlcv.traces import traces
from labwons.common.charts import r2c1nsy
from pandas import DataFrame, Series
from plotly.graph_objects import Figure


class ohlcv(object):

    def __init__(self, data:DataFrame, meta:Series):
        self.data = data
        self.meta = meta
        self.traces = traces(data, meta['name'])
        return

    def __call__(self, **kwargs):
        self.show(**kwargs)
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getitem__(self, item:str):
        return self.data[item]

    def __getattr__(self, item:str):
        if item in dir(self):
            return getattr(self, item)
        if hasattr(self.data, item):
            return getattr(self.data, item)
        raise AttributeError

    def figure(self, **kwargs) -> Figure:
        fig = r2c1nsy()
        fig.add_trace(row=1, col=1, trace=self.traces.ohlc)
        fig.add_trace(row=2, col=1, trace=self.traces.vol)
        fig.update_layout(title=f"{self.meta['name']}({self.meta.name}): OHLCV", **kwargs)
        fig.update_yaxes(row=1, col=1, title=f"Price [{self.meta.currency}]")
        fig.update_yaxes(row=2, col=1, title=f"Vol.")
        return fig

    def show(self, **kwargs):
        self.figure(**kwargs).show()
        return


if __name__ == "__main__":
    from pandas import set_option
    from labwons.asset.kr.etf.fetch import fetch
    set_option('display.expand_frame_repr', False)

    mySrc = fetch("005930")
    myOhlcv = ohlcv(mySrc.ohlcv, mySrc.meta)
    # print(myOhlcv)
    myOhlcv.show()