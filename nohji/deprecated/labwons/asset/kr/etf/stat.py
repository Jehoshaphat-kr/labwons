from labwons.asset.kr.etf.fetch import fetch
from typing import Union, Hashable
from pandas import Series


class stat(object):

    def __init__(self, ticker:Union[str, Hashable]):
        self._src_ = _src_ = fetch(ticker)
        self._des_ = Series()
        return

    def __call__(self) -> Series:
        return self.description

    @property
    def description(self) -> Series:
        if self._des_.empty:
            data = {}
            for attr in dir(self):
                if not (attr.startswith("_") or attr == "description"):
                    attribute = self.__getattribute__(attr)
                    data[attr] = attribute
            self._des_ = Series(data)
        return self._des_

    @property
    def averageVolume(self) -> int:
        return int(self._src_["ohlcv"]["volume"].mean())

    @property
    def averageVolume10days(self) -> int:
        return int(self._src_["ohlcv"]["volume"][-10:].mean())

    @property
    def benchmarkName(self) -> str:
        return self._src_["benchmarkName"]

    @property
    def benchmarkTicker(self) -> str:
        return self._src_["benchmarkTicker"]

    @property
    def beta(self) -> float:
        return self._src_["snapShot"]["beta"]

    @property
    def country(self) -> str:
        return self._src_["country"]

    @property
    def currency(self) -> str:
        return self._src_["currency"]

    @property
    def currentPrice(self) -> Union[int, float]:
        return self._src_["currentPrice"]

    @property
    def dividendYield(self) -> float:
        return self._src_["multiplesOutstanding"]["dividendYield"]

    @property
    def exchange(self) -> str: return self._src_["exchange"]

    @property
    def fiftyTwoWeekHigh(self) -> Union[int, float]:
        return self._src_["snapShot"]["fiftyTwoWeekHigh"]

    @property
    def fiftyTwoWeekHighRatio(self) -> float:
        return round(100 * (self.currentPrice / self.fiftyTwoWeekHigh - 1), 2)

    @property
    def fiftyTwoWeekLow(self) -> Union[int, float]:
        return self._src_["snapShot"]["fiftyTwoWeekLow"]

    @property
    def fiftyTwoWeekLowRatio(self) -> float:
        return round(100 * (self.currentPrice / self.fiftyTwoWeekLow - 1), 2)

    @property
    def fiscalPE(self) -> float:
        return self._src_["multiplesOutstanding"]["fiscalPE"]

    @property
    def foreignRate(self) -> float:
        return self._src_["snapShot"]["foreignRate"]

    @property
    def ipo(self) -> str: return self._src_["ipo"]

    @property
    def marketCap(self) -> int:
        return self._src_["snapShot"]["marketCap"]

    @property
    def name(self) -> str: return self._src_["name"]

    @property
    def nav(self) -> str:
        return self._src_["nav"]

    @property
    def previousClose(self) -> Union[int, float]:
        return self._src_["snapShot"]["previousClose"]

    @property
    def priceToBook(self) -> float:
        return self._src_["multiplesOutstanding"]["priceToBook"]

    @property
    def quoteType(self) -> str: return self._src_["quoteType"]

    @property
    def sector(self) -> str: return self._src_["sectorWeights"].iloc[:,0].idxmax()

    @property
    def underlyingAsset(self) -> str: return self._src_["underlyingAsset"]

    @property
    def volume(self) -> int: return self._src_["snapShot"]["volume"]





if __name__ == "__main__":

    st = stat("102780")
    print(st.description)
    # print(st.name)
    # print(st.sector)