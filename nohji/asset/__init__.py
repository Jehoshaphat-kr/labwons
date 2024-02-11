from nohji.asset.core.mem import mem
from nohji.asset.fetch import Data
from nohji.asset.technical import Technical
from nohji.asset.fundamental import Fundamental


class _Asset(Technical, Fundamental):

    def __init__(self, ticker:str, period:int=10, freq:str="d"):
        self._src_ = __src__ = Data(ticker, period, freq)

        Technical.__init__(self, __src__)
        Fundamental.__init__(self, __src__)
        return

    def __getitem__(self, item):
        if hasattr(self._src_, item):
            return getattr(self._src_, item)
        raise KeyError(f"No such <item; {item}> in <Asset; {self['ticker']}>")

    def __contains__(self, item):
        return item in Technical.__dict__ or item in Fundamental.__dict__


def Asset(ticker:str, period:int=10, freq:str="d") -> _Asset:
    __key__ = f"__asset_object_{ticker}_{period}_{freq}__"
    if not __key__ in mem:
        mem[__key__] = _Asset(ticker, period, freq)
    return mem[__key__]
