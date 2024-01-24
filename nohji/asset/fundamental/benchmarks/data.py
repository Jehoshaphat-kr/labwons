from nohji.asset.fetch import get_multi_ohlcv

from datetime import timedelta
from pandas import concat, DataFrame


def genKr(resembles: DataFrame) -> DataFrame:
    names = resembles["종목명"].to_dict()

    ohlcv = get_multi_ohlcv(*names.keys())
    close = concat({tic: ohlcv[tic].close for tic in names.keys()})

    objs = {}
    for yy in [5, 3, 2, 1, 0.5]:
        col = f"{yy}Y" if isinstance(yy, int) else f"{int(yy * 12)}M"
        date = close.index[-1] - timedelta(int(yy * 365))
        data = close[close.index >= date].dropna()
        objs[col] = 100 * ((data.pct_change().fillna(0) + 1).cumprod() - 1)
    return concat(objs, axis=1)