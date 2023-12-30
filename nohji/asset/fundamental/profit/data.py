from nohji.asset.fetch import fetch
from nohji.asset.core.datatype import multiframes


def genKr(_fetch:fetch) -> multiframes:
    columns = _fetch.fnguide.abstract.columns.tolist()
    columns = columns[: columns.index('당기순이익') + 1] + ["EPS(원)"]

    yy = _fetch.fnguide.abstract.Y[columns].join(_fetch.krx.marketCap.rename(inplace=True,), how='left')
    qq = _fetch.fnguide.abstract.Q[columns].join(_fetch.krx.marketCap, how='left')
    return multiframes(dict(Y=yy, Q=qq))
