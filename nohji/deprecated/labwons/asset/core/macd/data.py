from pandas import DataFrame, Series
from ta.trend import MACD
from warnings import filterwarnings
filterwarnings("ignore", message="invalid value encountered in scalar divide")
filterwarnings("ignore", message="invalid value encountered in cast")

def gen(typ:Series) -> DataFrame:
    data = DataFrame()
    macd = MACD(close=typ)
    data["macd"] = macd.macd()
    data["signal"] = macd.macd_signal()
    data["diff"] = macd.macd_diff()
    return data
