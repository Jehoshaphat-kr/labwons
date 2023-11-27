from labwons.equity.source.fnguide import _url
from labwons.equity.source.fnguide import _req
import pandas


class etf(object):

    __slots__ = (
        "__url__",
        "__mem__",
        "ticker",
        "snapShot",
        "multiples",
        "component",
        "sectors"
    )

    def __init__(self, ticker:str):
        self.__url__ = _url.url(ticker)
        self.__mem__ = {}
        self.ticker = ticker
        return

    def __getattr__(self, attr:str):
        if not attr in self.__mem__:
            self.__mem__[attr] = self.__slot__(attr)
        return self.__mem__[attr]

    def __slot__(self, attr:str):
        if attr == 'components':
            args = {"ticker": self.ticker}
        elif attr == 'sectors':
            args = {"_url": self.__url__, "ticker": self.ticker}
        else:
            args = {"_url": self.__url__}
        if not attr in ["ticker", "snapShot"]:
            attr = f"etf{attr.capitalize()}"
        func = getattr(_req, attr)
        return func(**args)


if __name__ == "__main__":
    pandas.set_option('display.expand_frame_repr', False)

    t = '102780'
    myEtf = etf(t)
    print(myEtf.snapShot)
    print(myEtf.multiples)
    print(myEtf.components)
    print(myEtf.sectors)


