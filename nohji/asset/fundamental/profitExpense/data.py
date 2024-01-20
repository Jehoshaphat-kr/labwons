from pandas import DataFrame, Series


def genKr(meta:Series, incomeStatement:DataFrame) -> DataFrame:
    if meta.industry.endswith("은행"):
        columns = ["순영업수익", "판매비와관리비", "영업이익"]
    else:
        columns = ["매출액", "매출원가", "판매비와관리비", "영업이익"]

    data = incomeStatement.Y[columns].copy()
    data.index = [f"{i} (합산)" if i == data.index[-1] else i for i in data.index]
    data["매출원가%"] = 100 * data["매출원가"] / data["매출액"]
    data["판매비와관리비%"] = 100 * data["판매비와관리비"] / data["매출액"]
    data["영업이익%"] = 100 * data["영업이익"] / data["매출액"]
    return data
