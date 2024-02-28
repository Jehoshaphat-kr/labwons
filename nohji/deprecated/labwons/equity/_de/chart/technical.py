from labwons.common.basis import candleStick, barTY
from labwons.common.chart import Chart
from nohji.deprecated.labwons.equity import stock, etf
from nohji.deprecated.labwons.equity import equity
from typing import Union
from plotly.graph_objects import Figure




class technical(object):

    def __init__(self, data:Union[stock, etf, equity], name:str, ticker:str):
        self.d, self.n, self.t = data, name, ticker
        self.label = f"{name}({ticker})"
        return

    def __call__(self, *args, **kwargs):
        return

    def __getattr__(self, item:str):
        attr = self.__getattribute__(item)
        if callable(attr):
            return attr()

    def ohlcv(self, **kwargs) -> Figure:
        fig = Chart.r2c1nsy()
        ohlc = candleStick(self.d.price, name=self.label)
        fig.add_trace(row=1, col=1, trace=ohlc)
        fig.add_trace(row=2, col=1, trace=barTY(self.d.price.volume, showlegend=False))
        fig.update_layout(**kwargs)
        return fig



if __name__ == "__main__":
    d = stock("005930")
    c = technical(d, "Samsung", "005930")
    c.ohlcv().show()
