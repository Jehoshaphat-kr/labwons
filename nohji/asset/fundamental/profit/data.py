from nohji.asset.fetch import fetch
from nohji.asset.core.datatype import multiframes


def genKr(_fetch:fetch) -> multiframes:
    abstract = _fetch.fnguide.abstract
    columns = abstract.columns.tolist()
    columns = columns[: columns.index('당기순이익') + 1] + ["EPS"]

    yCap = _fetch.krx.yearlyMarketCap.copy()
    qCap = _fetch.krx.quarterlyMarketCap.copy()

    yCap.index = yCap.index[:-1].tolist() + [abstract.Y.index[-1]]
    qCap.index = qCap.index[:-1].tolist() + [abstract.Q.index[-1]]
    yy = abstract.Y[columns].join(yCap, how='left')
    qq = abstract.Q[columns].join(qCap, how='left')

    yy = yy[[yCap.name] + columns]
    qq = qq[[qCap.name] + columns]
    return multiframes(dict(Y=yy, Q=qq))
