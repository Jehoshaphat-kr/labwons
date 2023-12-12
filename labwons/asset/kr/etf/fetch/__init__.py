from labwons.asset.kr.etf.fetch import (
    __urls__,
    fnguide,
    krx,
    naver
)
from labwons.common.metadata import metaData
from inspect import signature
from typing import Union, Hashable


class fetch:
    """
    Back data of ETF,
    """
    __ref__ = (fnguide, krx, naver)
    def __init__(self, ticker:Union[str, Hashable], period:int=10, freq:str='d'):
        self.ticker = ticker
        self._url_ = _url_ = __urls__.urls(ticker)
        self._arg_ = {"ticker": ticker, "url": _url_, "period": period, "freq": freq}
        self._mem_ = metaData(ticker).to_dict()
        return

    def __getitem__(self, item:str):
        return self.__getattr__(item)

    def __getattr__(self, item:str):
        _item_ = f"get{item[0].capitalize()}{item[1:]}"
        if item in self._mem_:
            return self._mem_[item]
        for _module_ in (fnguide, krx, naver):
            if hasattr(_module_, _item_):
                _attr_ = getattr(_module_, _item_)
                _args_ = {arg: self._arg_[arg] for arg in signature(_attr_).parameters}
                self._mem_[item] = _attr_(**_args_)
                return self._mem_[item]
        if not item in self.__dir__():
            raise AttributeError(f"No such attribute as : {item}")


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    test = fetch(
        '102780' # KODEX 삼성그룹
        # '114800' # KODEX 인버스
        # '069500'  # KODEX 200
    )
    # print(test._mem_)
    print(test.ticker)
    print(test.multiplesOutstanding)
    print(test.sectorWeights)
    print(test.snapShot)
    print(test.currentPrice)
    print(test.underlyingAsset)
    print(test.nav)
    print(test.components)