from labwons.asset.common.tech.ohlcv import ohlcv
from labwons.asset.common.tech import typ, trend
from inspect import signature
from pandas import DataFrame, Series
# from ta import add_all_ta_features
# from warnings import filterwarnings
# filterwarnings("ignore", category=RuntimeWarning)


class tech(object):

    def __init__(self, data:DataFrame, meta:Series):
        # self.data = add_all_ta_features(data, "open", "high", "low", "close", "volume")
        self.data = data
        self.meta = meta
        self._inst_ = {"data":data, "meta":meta, "ohlcv": ohlcv(data, meta)}
        # self._args_ = {"data":data, "meta":meta, "ohlcv":self._inst_["ohlcv"]}
        return

    def __str__(self) -> str:
        return str(self.data)

    def __getitem__(self, item:str):
        return self.data[item]

    def __getattr__(self, item:str):
        if item in self._inst_:
            return self._inst_[item]
        if item in globals():
            _attr_ = getattr(globals()[item], item)
            _args_ = {arg: getattr(self, arg) for arg in signature(_attr_).parameters}
            self._inst_[item] = _attr_(**_args_)
            return self._inst_[item]
        if not item in dir(self):
            raise AttributeError


if __name__ == "__main__":
    from pandas import set_option
    from labwons.asset.kr.etf.fetch import fetch
    set_option('display.expand_frame_repr', False)

    mySrc = fetch("005930")
    myTech = tech(mySrc.ohlcv, mySrc.meta)
    # print(myTech.typ)
    print(myTech.trend)
    myTech.trend.show()