from nohji.asset.fetch import fetch
from nohji.asset.core.datatype import multiframes


def genKr(_fetch:fetch) -> multiframes:
    abstract = _fetch.fnguide.abstract
    columns = abstract.columns.tolist()
    columns = columns[: columns.index('영업이익') + 1] + ["자본총계", "부채총계", "자산총계", "부채비율"]

    yCap = _fetch.krx.marketCap.copy()
    qCap = _fetch.krx.marketCap.copy()

    yCap.index = yCap.index[:-1].tolist() + [abstract.Y.index[-1]]
    qCap.index = qCap.index[:-1].tolist() + [abstract.Q.index[-1]]
    yy = abstract.Y[columns].join(yCap, how='left')
    qq = abstract.Q[columns].join(qCap, how='left')

    yy = yy[[yCap.name] + columns]
    qq = qq[[qCap.name] + columns]
    return multiframes(dict(Y=yy, Q=qq))
