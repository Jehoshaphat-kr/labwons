from pandas import concat, DataFrame, Series


def gen(data:Series) -> DataFrame:
    objs = {data.name: data}
    for dd in [5, 20, 60, 120, 200]:
        objs[f"{dd}TD"] = data.rolling(window=dd).mean()
    return concat(objs=objs, axis=1)
