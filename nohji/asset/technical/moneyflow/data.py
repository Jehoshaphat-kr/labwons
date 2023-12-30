from pandas import DataFrame
from ta import add_volume_ta
from warnings import filterwarnings
filterwarnings("ignore", message="invalid value encountered in scalar divide")
filterwarnings("ignore", message="invalid value encountered in cast")

def gen(ohlcv:DataFrame) -> DataFrame:
    sampler = dict(
        volume_obv='obv',
        volume_cmf='cmf',
        volume_mfi='mfi',
    )
    data = add_volume_ta(ohlcv.copy(), "high", "low", "close", "volume")[sampler.keys()]
    return data.rename(columns=sampler)
