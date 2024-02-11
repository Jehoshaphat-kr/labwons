from nohji.meta import meta
from nohji.asset import Asset

from datetime import datetime
from pandas import concat
from pykrx.stock import get_market_cap_by_ticker
from tqdm import tqdm
from typing import Iterable


class sampling:

    _prog = "off"

    def __init__(self, tickers:Iterable=None, **kwargs):
        _data_ = meta.data
        _data_ = _data_[(_data_["quoteType"] == "EQUITY") & (_data_["country"] == "KOR")]
        if tickers:
            _data_ = _data_[_data_.index.isin(tickers)]
        for key, value in kwargs.items():
            if not key in _data_:
                continue
            if isinstance(value, list):
                _data_ = _data_[_data_[key].isin(value)]
            else:
                _data_ = _data_[_data_[key] == value]
        _cap_ = get_market_cap_by_ticker(date=datetime.today().strftime("%Y%m%d"), alternative=True)
        self._data_ = _data_.copy().join(_cap_, how="left")
        return

    def __repr__(self) -> repr:
        return repr(self._data_)

    def __iter__(self):
        if self.prog == "on":
            loop = tqdm(self._data_.index)
            for ticker in loop:
                loop.set_description(desc=f"{ticker}...")
                yield Asset(ticker)
        else:
            for ticker in self._data_.index:
                yield Asset(ticker)
        return

    @property
    def prog(self) -> str:
        return self._prog

    @prog.setter
    def prog(self, prog:str):
        if not prog.lower() in ["on", "off"]:
            raise KeyError(f"progress set error")
        self._prog = prog.lower()

    def append(self, spec:str, key:str=""):
        if key:
            self._data_[key] = [getattr(a, spec).stat[key] for a in self]
            return
        data = concat([getattr(a, spec).stat.carrier for a in self], axis=1).T
        self._data_ = self._data_.join(data, how="left")
        return


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    bubbles = sampling(industry="WI26 반도체")
    # bubbles = sampling(industry=["WI26 반도체", "WI26 자동차"])
    # bubbles = sampling(tickers=["005930", "012330", '000660'])
    bubbles.prog = "on"
    print(bubbles)

    # bubbles.append("Trend")
    # print(bubbles)

