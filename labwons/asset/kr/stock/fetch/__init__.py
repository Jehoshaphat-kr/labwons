from labwons.asset.kr.stock.fetch import (
    __urls__,
    fnguide,
    krx,
    naver
)
from inspect import signature
from typing import Union, Hashable


class fetch:

    __slots__ = (
        "ticker",
        "_url_",
        "_arg_",
        "_mem_",
        "abstract",
        "analogy",
        "benchmarkMultiples",
        "businessSummary",
        "cashFlow",
        "consensusOutstanding",
        "consensusPrice",
        "consensusProfit",
        "consensusTendency",
        "currentPrice",
        "expenses",
        "financialStatement",
        "financialStatementSeparate",
        "foreignRate",
        "growthRate",
        "incomeStatement",
        "marketShares",
        "multipleBand",
        "multiples",
        "multiplesOutstanding",
        "multiplesTrailing",
        "products",
        "profitRate",
        "shareHolders",
        "shareInstitutes",
        "shortBalance",
        "shortSell",
        "snapShot",
        "stabilityRate",
        "analogy",
        "currentPrice",
        "multiplesTrailing",
        "marketCap"
    )

    def __init__(self, ticker:Union[str, Hashable]):
        self.ticker = ticker
        self._url_ = __urls__.urls(ticker)
        self._arg_ = {"ticker": self.ticker, "url": self._url_, "gb": self._url_.gb}
        self._mem_ = {}
        return

    def __getattr__(self, item:str):
        if item in self._mem_:
            return self._mem_[item]

        for _module_ in (fnguide, krx, naver):
            _item_ = f"get{item[0].capitalize()}{item[1:]}"
            if hasattr(_module_, _item_):
                _attr_ = getattr(_module_, _item_)
                _args_ = {key: self._arg_[key] for key in signature(_attr_).parameters if key in self._arg_}
                self._mem_[item] = _attr_(**_args_)
                return self._mem_[item]
        raise AttributeError(f"No such attribute as : {item}")


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    myStock = fetch(
        # "005930" # SamsungElec
        # "000660" # SK hynix
        # "207940" # SAMSUNG BIOLOGICS
        # "005380" # HyundaiMtr
        # "005490"  # POSCO
        # "035420" # NAVER Corporation
        # "000270" # Kia Corporation
        # "051910" # LG Chem, Ltd.
        # "006400" # Samsung SDI Co., Ltd.
        # "068270" # Celltrion, Inc.
        "035720"  # Kakao Corp.
        # "028260" # Samsung C&T Corporation
        # "105560" # KB Financial Group Inc.
        # "012330" # Mobis
        # "055550" # Shinhan Financial Group Co., Ltd.
        # "066570" # LG Electronics Inc.
        # "032830" # Samsung Life Insurance Co., Ltd.
        # "096770" # SK Innovation Co., Ltd.
        # "003550" # LG Corp.
        # "015760" # Korea Electric Power Corporation
        # "017670" # SK Telecom Co.,Ltd
        # "316140" # Woori Financial Group Inc.

        # "359090"  # C&R Research
        # "042660"  # Daewoo Shipbuilding & Marine Engineering Co.,Ltd
        # "021080" # Atinum Investment
        # "130500" # GH Advanced Materials Inc.
        # "323280" # SHT-5 SPAC
    )
    print(myStock.abstract)
    print(myStock.analogy)
    print(myStock.benchmarkMultiples)
    print(myStock.businessSummary)
    print(myStock.cashFlow)
    print(myStock.consensusOutstanding)
    print(myStock.consensusPrice)
    print(myStock.consensusProfit)
    print(myStock.consensusTendency)
    print(myStock.currentPrice)
    print(myStock.expenses)
    print(myStock.financialStatement)
    print(myStock.financialStatementSeparate)
    print(myStock.foreignRate)
    print(myStock.growthRate)
    print(myStock.incomeStatement)
    print(myStock.marketShares)
    print(myStock.multipleBand)
    print(myStock.multiples)
    print(myStock.multiplesOutstanding)
    print(myStock.multiplesTrailing)
    print(myStock.products)
    print(myStock.profitRate)
    print(myStock.shareHolders)
    print(myStock.shareInstitutes)
    print(myStock.shortBalance)
    print(myStock.shortSell)
    print(myStock.snapShot)
    print(myStock.stabilityRate)

    print(myStock.analogy)
    print(myStock.currentPrice)
    print(myStock.multiplesTrailing)

    print(myStock.marketCap)