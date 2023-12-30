from pandas import DataFrame, Series
from numpy import nan


def gen(typ:Series) -> DataFrame:
    data = DataFrame()
    data['price'] = typ
    data['middle'] = typ.rolling(window=20).mean()
    data['stdev'] = typ.rolling(window=20).std()
    data['upperband'] = data.middle + 2 * data.stdev
    data['lowerband'] = data.middle - 2 * data.stdev
    data['uppertrend'] = data.middle + data.stdev
    data['lowertrend'] = data.middle - data.stdev
    data['width'] = 100 * (4 * data.stdev) / data.middle
    data['pctb'] = (
            (data.price - data.lowerband) / (data.upperband - data.lowerband)
    ).where(data.upperband != data.lowerband, nan)
    return data