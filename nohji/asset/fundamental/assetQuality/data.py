from pandas import DataFrame, Series


def genKr(abstract:DataFrame, yearlyMarketCap:Series) -> DataFrame:
    columns = abstract.columns.tolist()
    columns = ["자본총계", "부채총계", "자산총계", "부채비율"] + columns[: columns.index('영업이익') + 1]

    marketCap = yearlyMarketCap.copy()
    marketCap.index = marketCap.index[:-1].tolist() + [abstract.Y.index[-1]]

    data = abstract.Y[columns].join(marketCap, how='left')
    return data[[marketCap.name] + columns]
