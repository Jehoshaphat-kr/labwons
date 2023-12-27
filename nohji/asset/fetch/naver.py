from nohji.util.brush import str2num
from nohji.util.web import web
from nohji.meta import meta

from datetime import datetime
from pandas import DataFrame, Series
from numpy import nan
from typing import Union


class naver:
    """
    Fetch source data from Naver

    @currentPrice
        type        : Union[int, float]
        description : current price (close)

    @resemblences
        type        : DataFrame
        description : current price (close)
        columns     : ['종목명', '현재가', '등락률', '시가총액(억)', '외국인비율(%)', '매출액(억)', '영업이익(억)',
                       '조정영업이익(억)', '영업이익증가율(%)', '당기순이익(억)', '주당순이익(원)', 'ROE(%)', 'PER(%)',
                       'PBR(배)']
        example     :
                        종목명  현재가 등락률 시가총액(억) 외국인비율(%)  매출액(억) 영업이익(억)  ...  PER(%) PBR(배)
            058470    리노공업  143800  -1.57        21918         37.25         751          336  ...   21.69    4.35
            005930    삼성전자   70600   0.14      4214666         53.21      600055         6685  ...   13.47    1.37
            000660  SK하이닉스  132000   1.15       960963         52.59       73059       -28821  ...  -11.73    1.58
            402340    SK스퀘어   48450   0.41        67336         45.29       -1274        -7345  ...   -3.64    0.43
            042700  한미반도체   60200  -9.20        58598         12.38         491          112  ...   29.07   10.80

    @multiplesTrailing
        type        : Series
        description : trailing multiples
        example     :
            trailingPE         30.53
            trailingEps     16642.00
            estimatePE         22.00
            estimateEps     22901.00
            priceToBook         1.22
            bookValue      416754.00
            dividendYield        2.1
            dtype: float64
    """
    def __init__(self, ticker:str):
        self._tic_ = ticker
        self._url_ = f"https://finance.naver.com/item/main.naver?code={ticker}"
        self._typ_ = meta(ticker).quoteType
        self._mem_ = {}
        return

    @property
    def currentPrice(self) -> Union[int, float]:
        if not "currentPrice" in self._mem_:
            html = web.html(self._url_)
            curr = [d.text for d in html.find_all("dd") if d.text.startswith("현재가")][0]
            self._mem_["currentPrice"] = str2num(curr[curr.index("현재가 ") + 4: curr.index(" 전일대비")])
        return self._mem_["currentPrice"]

    @property
    def resemblances(self) -> DataFrame:
        columns = ['종목명', '현재가', '등락률', '시가총액(억)', '외국인비율(%)', '매출액(억)', '영업이익(억)',
                   '조정영업이익(억)', '영업이익증가율(%)', '당기순이익(억)', '주당순이익(원)', 'ROE(%)', 'PER(%)',
                   'PBR(배)']
        if not self._typ_ == "EQUITY":
            return DataFrame(columns=columns)
        if not "resemblances" in self._mem_:
            data = web.list(self._url_)[4]
            data = data.set_index(keys='종목명').drop(index=['전일대비'])
            data.index.name = None
            for col in data:
                data[col] = data[col].apply(str2num)
            data = data.T
            data["종목명"] = [i.replace('*', '')[:-6] for i in data.index]
            data.index = [i[-6:] for i in data.index]
            self._mem_["resemblances"] = data
        return self._mem_["resemblances"]

    @property
    def multiplesTrailing(self) -> Series:
        index = ["trailingPE", "trailingEps", "estimatePE", "estimateEps",
                 "priceToBook", "bookValue", "dividendYield"]
        if not self._typ_ == "EQUITY":
            return Series(index=index)
        if not "multiplesTrailing" in self._mem_:
            data = web.list(self._url_)[8]
            per, eps = map(str, data.columns[-1].split('l'))
            estPE, estEps = map(str, data.iloc[0, -1].split('l'))
            pbr, bps = map(str, data.iloc[1, -1].split('l'))
            self._mem_["multiplesTrailing"] = Series({
                "trailingPE": str2num(per),
                "trailingEps": str2num(eps),
                "estimatePE": str2num(estPE),
                "estimateEps": str2num(estEps),
                "priceToBook": str2num(pbr),
                "bookValue": str2num(bps),
                "dividendYield": str2num(data.iloc[-1, -1])
            })
        return self._mem_["multiplesTrailing"]

    @property
    def ipo(self) -> Union[datetime.date, float]:
        if self._typ_ == "ETF":
            return datetime.strptime(str(str2num(web.list(self._url_)[6].iloc[-1, -1])), "%Y%m%d").date()
        elif self._typ_ == "EQUITY":
            return meta(self._tic_).ipo
        return nan

    @property
    def underlyingAsset(self) -> Union[str, float]:
        if self._typ_ == "ETF":
            return web.list(self._url_)[6].columns[-1]
        return nan

    @property
    def nav(self) -> Union[int, float]:
        if self._typ_ == "ETF":
            return str2num(web.list(self._url_)[8].columns[-1])
        return nan


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    naver = naver(
        # "005930"
        "069500"
    )
    print(naver.currentPrice)
    print(naver.resemblances)
    print(naver.multiplesTrailing)
    print(naver.ipo)
    print(naver.underlyingAsset)
    print(naver.nav)