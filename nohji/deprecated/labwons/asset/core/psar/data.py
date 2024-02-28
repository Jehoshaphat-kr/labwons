from pandas import DataFrame
from numpy import isnan
from ta.trend import PSARIndicator
from warnings import filterwarnings
filterwarnings("ignore", message="invalid value encountered in scalar divide")
filterwarnings("ignore", message="invalid value encountered in cast")

def gen(ohlcv:DataFrame) -> DataFrame:
    data = DataFrame()
    psar = PSARIndicator(ohlcv.high, ohlcv.low, ohlcv.close)
    data["up"] = psar.psar_up()
    data["down"] = psar.psar_down()
    data['psar'] = data.apply(lambda x: x['up'] if isnan(x['down']) else x['down'], axis=1)
    data['typ'] = (ohlcv.high + ohlcv.low + ohlcv.close) / 3
    data['pct'] = 100 * (data['typ'] / data['psar'] - 1)
    return data[["typ", "up", "down", "psar", "pct"]]
