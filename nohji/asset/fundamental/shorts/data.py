from pandas import concat, DataFrame


def gen(shortSell:DataFrame, shortBalance:DataFrame) -> DataFrame:
    return concat(
        axis=1,
        objs={
        '종가': shortSell["종가"],
        '공매도비중': shortSell["공매도비중"],
        '대차잔고비중': shortBalance["대차잔고비중"]
    })