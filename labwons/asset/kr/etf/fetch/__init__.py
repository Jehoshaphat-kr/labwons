from labwons.asset.kr.etf.fetch import (
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
        "multiplesOutstanding",
        "sectorWeights",
        "snapShot",
        "currentPrice",
        "underlyingAsset",
        "nav",
        "components"
    )

    def __init__(self, ticker:Union[str, Hashable]):
        self.ticker = ticker
        self._url_ = __urls__.urls(ticker)
        self._arg_ = {"ticker": self.ticker, "url": self._url_}
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

    test = fetch(
        '102780' # KODEX 삼성그룹
        # '114800' # KODEX 인버스
        # '069500'  # KODEX 200
    )

    print(test.multiplesOutstanding)
    print(test.sectorWeights)
    print(test.snapShot)
    print(test.currentPrice)
    print(test.underlyingAsset)
    print(test.nav)
    print(test.components)