from nohji.asset.fetch import fetch
from nohji.asset.core.datatype import multiframes

from pandas import concat


def genKr(_fetch:fetch) -> multiframes:
    if _fetch.meta.industry.endswith("은행"):
        columns = ["순영업수익", "판매비와관리비", "영업이익"]
    else:
        columns = ["매출액", "매출원가", "판매비와관리비", "영업이익"]
    profit = concat([_fetch.fnguide.abstract.Y, _fetch.fnguide.abstract.Q], axis=0)[["영업이익률"]]

    incomeY = _fetch.fnguide.incomeStatement.Y[columns].join(profit, how="left")
    incomeQ = _fetch.fnguide.incomeStatement.Q[columns].join(profit, how="left")

    return multiframes(dict(Y=incomeY, Q=incomeQ))
