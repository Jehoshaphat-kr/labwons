from pandas import DataFrame, Series

def genKr(
    abstract: DataFrame,
    resembles: DataFrame,
    multipleOutstanding: Series,
    snapShot: Series,
    currentPrice: int,
) -> DataFrame:

    resembles = resembles[["종목명", "PER(%)"]].rename(columns={"PER(%)": "PER"}).copy()
    abstract = abstract["PER"][:-1].copy()
    compensate = currentPrice / snapShot.previousClose

    ticker, name = resembles.index[0], resembles.종목명[0]

    index = [ticker] * 5
    names = [
        name,
        f"{name}<br>(직전회계연도)",
        f"{name}<br>(3Y 평균)",
        f"{name}<br>(5Y 평균)",
        f"{name}<br>(12M 전망)"
    ]
    value = [
        resembles.PER[0],
        multipleOutstanding.fiscalPE * compensate,
        abstract[-3:].mean(),
        abstract.mean(),
        multipleOutstanding.forwardPE * compensate
    ]
    index += resembles.index.tolist()[1:] + [""]
    names += resembles.종목명.tolist()[1:] + ["Sector PE"]
    value += resembles.PER.tolist()[1:] + [multipleOutstanding.sectorPE]
    return DataFrame(data={"종목명": names, "PER": value}, index=index)