from labwons.common.charts import r2c1nsy
from labwons.common.basis import candleStick, barTY
from pandas import DataFrame


class ohlcv(r2c1nsy):

    def __init__(self, price: DataFrame, name: str, ticker: str):
        super().__init__()
        ohlc = candleStick(price, name=f"{name}({ticker})")
        volume = barTY(price.volume)
        self.add_trace(row=1, col=1, trace=ohlc)
        self.add_trace(row=2, col=1, trace=volume)
        return


if __name__ == "__main__":
    from nohji.deprecated.labwons.equity import stock

    fetch = stock("005930")
    test = ohlcv(fetch.price, "samsumg", "005930")
    test.show()
