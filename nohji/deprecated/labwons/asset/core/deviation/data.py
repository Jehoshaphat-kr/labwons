from pandas import concat, DataFrame, Series


def gen(data:DataFrame) -> DataFrame:
    objs = {}
    cols = data.columns.tolist()
    for col in cols[1:]:
        both = data[[cols[0], col]].dropna()
        if data.empty:
            objs[col] = Series(name=col, dtype=float)
            continue
        objs[col] = (both[cols[0]] - both[col]) / (abs(both[cols[0]] - both[col]).sum() / len(both))
    return concat(objs=objs, axis=1)
