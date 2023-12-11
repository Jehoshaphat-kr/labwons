from labwons.asset.kr.stock.fetch import fetch


class datum(fetch):

    __slots__ = ('b', 'c')

    def __init__(self, ticker:str):
        fetch.__init__(self, ticker)
        self.b = self.shortSell
        return

    @property
    def a(self) -> int:
        return 1



if __name__ == "__main__":
    data = datum("005930")
    print(data.a)
    print(data.b)
    print(data.shortSell)