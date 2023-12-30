from nohji.asset.core.decorator import krmarket
from nohji.asset.fetch.fnguide import fnguide
from nohji.asset.fetch.krx import krx
from nohji.asset.fetch.naver import naver
from nohji.meta import meta



class fetch:

    def __init__(self, ticker:str):
        self.meta = meta(ticker)
        return

    @krmarket
    def fnguide(self) -> fnguide:
        return fnguide(self.meta.name)

    @krmarket
    def krx(self) -> krx:
        return krx(self.meta.name)

    @krmarket
    def naver(self) -> naver:
        return naver(self.meta.name)