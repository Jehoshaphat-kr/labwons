from typing import Union
from labwons.equity.equity import Equity
from labwons.bundle.performance import performance
from labwons.bundle._bars import _bars
import pandas as pd


class Bundle(object):
    _color_ = [
        "rgb(155, 194, 230)",
        "rgb(244, 176, 132)",
        "rgb(255, 217, 102)",
        "rgb(169, 208, 142)",
        "rgb(132, 151, 176)",
        "rgb(201, 201, 201)",
    ]
    _slots_ = {}
    def __init__(self, ticker:Union[Equity, str], *tickers, **kwargs):
        if isinstance(ticker, str):
            self._base_ = Equity(ticker=ticker, **kwargs)
        elif isinstance(ticker, Equity):
            self._base_ = ticker
        else:
            raise KeyError
        self._slots_[ticker] = self._base_
        for t in tickers:
            self.append(t)

        autoappend = kwargs["autoappend"] if "autoappend" in kwargs else True
        if autoappend:
            for t in getattr(self._slots_[ticker], '_naver').similarities.index:
                self.append(t, **kwargs)

        self.settings = {
            "language": kwargs["language"] if "language" in kwargs else "eng",
            "color": dict(zip([n.name for n in self._slots_.values()], self._color_[:len(self._slots_)])),
        }
        return

    def _objs_(self, attr:str, is_method:bool=False) -> list:
        return [getattr(e, attr)() if is_method else getattr(e, attr) for e in self._slots_.values()]

    def append(self, ticker:str, **kwargs):
        if len(self._slots_) == len(self._color_):
            return
        if not ticker in self._slots_:
            self._slots_[ticker] = Equity(ticker, **kwargs)
        return

    @property
    def overview(self) -> pd.DataFrame:
        return pd.DataFrame(data=self._objs_("describe", True))

    @property
    def returns(self) -> performance:
        return performance(self._slots_, self.settings)

    # @property
    # def profitRate(self) -> _bars:
    #     objs = [obj.annualProfitRate["영업이익률"] for e in self._slots_.values()]
    #     return _bars(self._slots_, data=pd.)

if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)

    bundle = Bundle("005930", '000660', '042700', '000990', autoappend=False, language='kor')
    print(bundle.overview)
    print(bundle.returns)
    bundle.returns.show()
