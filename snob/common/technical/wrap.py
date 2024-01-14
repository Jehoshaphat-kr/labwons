from pandas import DataFrame
from inspect import currentframe



class technicalAnalysis:

    def __init__(self, ohlcv:DataFrame):
        self.ohlcv = ohlcv
        return

    @property
    def bollingerBand(self):
        _attr_ = f"_{currentframe().f_code.co_name}_"
        if not hasattr(self, _attr_):
            # dc = dataChart()
            # dc.data = data = bollinger.calculate(self.ohlcv)
            # dc.trace = trace = bollinger.trace(data)
            # dc.chart = bollinger.chart(trace)
            setattr(self, _attr_, self.ohlcv)
        return getattr(self, _attr_)


if __name__ == "__main__":
    from nohji.asset.fetch import fetch

    data = fetch("005930").krx.ohlcv
    ta = technicalAnalysis(data)
    print(ta.bollingerBand)