from pandas import DataFrame
from ta import add_momentum_ta
from warnings import filterwarnings
filterwarnings("ignore", message="invalid value encountered in scalar divide")
filterwarnings("ignore", message="invalid value encountered in cast")

def gen(data:DataFrame) -> DataFrame:
    sampler = {
        'momentum_rsi':'rsi',
        'momentum_stoch':'stoch_osc',
        'momentum_stoch_signal':'stoch_osc_sig',
        'momentum_stoch_rsi':'stoch_rsi',
        'momentum_stoch_rsi_k':'stoch_rsi_k',
        'momentum_stoch_rsi_d':'stoch_rsi_d'
    }
    data = add_momentum_ta(data.copy(), "high", "low", "close", "volume")[sampler.keys()]
    return data.rename(columns=sampler)
