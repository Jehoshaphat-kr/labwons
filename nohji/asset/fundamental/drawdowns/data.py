from nohji.asset.fetch import get_multi_ohlcv

from datetime import timedelta
from pandas import concat, DataFrame, Series


def genKr(resembles: DataFrame, meta:Series) -> DataFrame:
    names = {row[1]: row[0] for row in resembles["종목명"].items()}
    names[meta.benchmark] = meta.benchmarkTicker

    objs = {}
    ohlcv = get_multi_ohlcv(*names.values())
    for name, ticker in names.items():
        price = ohlcv[ticker].close.dropna()
        if len(price) < 252:
            continue
        objs[f"{name}_{ticker}"] = price
    close = concat(objs, axis=1)

    objs = {}
    for yy in [5, 3, 2, 1, 0.5]:
        col = f"{yy}Y" if isinstance(yy, int) else f"{int(yy * 12)}M"
        date = close.index[-1] - timedelta(int(yy * 365))
        data = close[close.index >= date].dropna()
        if len(data) >= 0.95 * yy * 252:
            objs[col] = 100 * (data - data.cummax()) / data.cummax()
    return concat(objs, axis=1)