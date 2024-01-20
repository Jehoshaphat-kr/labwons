from nohji.asset.fetch._fnguide import fnguide
from nohji.asset.fetch._krx import krx
from nohji.asset.fetch._naver import naver


class Data(fnguide, krx, naver):

    def __init__(self, ticker:str, period:int=10, freq:str="d"):
        fnguide.__init__(self, ticker)
        krx.__init__(self, ticker, period, freq)
        naver.__init__(self, ticker)
        return

    def __repr__(self) -> str:
        comma = ",\n\t"
        attrs = sorted([attr for attr in self.__dir__() if not attr.startswith("_")])
        return f"< Source Data of : {self.meta.longName}({self.meta.name}) >\n" \
               f"Properties([\n" \
               f"\t{comma.join(attrs)}\n" \
               f"])"

if __name__ == "__main__":

    data = Data("005930")
    print(data)
