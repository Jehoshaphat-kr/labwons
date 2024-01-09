from nohji.util.brush import str2num
from nohji.util.web import web
from nohji.asset.core.decorator import common, stockonly, etfonly

from datetime import datetime
from pandas import DataFrame, Series, isna
from numpy import nan
from typing import Union


class naver:
    """
    Fetch source data from Naver

    @currentPrice
        type        : Union[int, float]
        description : current price (close)

    @resemblances
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

    @ipo
        type        : Union[int, float]
        description : current price (close)

    @currentPrice
        type        : Union[int, float]
        description : current price (close)

    @currentPrice
        type        : Union[int, float]
        description : current price (close)
    """

    def __init__(self, meta:Union[Series, str]):
        self.meta = Series(data={"ticker": meta}) if isinstance(meta, str) else meta
        self.ticker = self.meta.ticker
        self._url_main = f"https://finance.naver.com/item/main.naver?code={self.ticker}"
        self._url_finn = f"https://finance.naver.com/item/coinfo.naver?code={self.ticker}"
        return

    @common
    def currentPrice(self) -> Union[int, float]:
        html = web.html(self._url_main)
        curr = [d.text for d in html.find_all("dd") if d.text.startswith("현재가")][0]
        return str2num(curr[curr.index("현재가 ") + 4: curr.index(" 전일대비")])

    @stockonly
    def resemblances(self) -> DataFrame:
        data = web.list(self._url_main)[4]
        data = data.set_index(keys='종목명').drop(index=['전일대비'])
        data.index.name = None
        for col in data:
            data[col] = data[col].apply(str2num)
        data = data.T
        data["종목명"] = [i.replace('*', '')[:-6] for i in data.index]
        data.index = [i[-6:] for i in data.index]
        return data

    @stockonly
    def multiplesTrailing(self) -> Series:
        data = web.list(self._url_main)[8]
        per, eps = map(str, data.columns[-1].split('l'))
        estPE, estEps = map(str, data.iloc[0, -1].split('l'))
        pbr, bps = map(str, data.iloc[1, -1].split('l'))
        return Series({
            "trailingPE": str2num(per),
            "trailingEps": str2num(eps),
            "estimatePE": str2num(estPE),
            "estimateEps": str2num(estEps),
            "priceToBook": str2num(pbr),
            "bookValue": str2num(bps),
            "dividendYield": str2num(data.iloc[-1, -1])
        })

    @common
    def ipo(self) -> Union[datetime.date, float]:
        data = self.meta.ipo
        if not isna(data) and data:
            return data
        try:
            return datetime.strptime(str(str2num(web.list(self._url_main)[6].iloc[-1, -1])), "%Y%m%d").date()
        except (AttributeError, KeyError, TypeError, ValueError):
            return nan

    @etfonly
    def underlyingAsset(self) -> str:
        return web.list(self._url_main)[6].columns[-1]

    @etfonly
    def nav(self) -> Union[int, float]:
        return str2num(web.list(self._url_main)[8].columns[-1])


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    naver = naver(
        "005930"
        # "069500"
    )
    # print(naver.currentPrice)
    # print(naver.resemblances)
    # print(naver.multiplesTrailing)
    # print(naver.ipo)
    # print(naver.underlyingAsset)
    # print(naver.nav)

    import pandas as pd
    import requests
    import re

    url = "https://navercomp.wisereport.co.kr/v2/company/"

    def GetNvrEncparam(code="005930"):
        re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
        re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)
        _url = f"{url}c1010001.aspx?cmp_cd={code}"
        html = requests.get(_url).text
        encparam = re_enc.search(html).group(1)
        encid = re_id.search(html).group(1)
        print(html)
        params = {
            "cmp_cd": '000660',
            "fin_typ": 0,
            "freq_typ": "A",
            # "extY": 0,
            # "extQ": 0,
            # "encparam": 'bExFc2UxdWlVYTdlaENLZlNLQWs2UT09',
            "encparam": encparam,
            # "id": 'ZTRzQlVCd0'
            "id": encid
        }
        resp = requests.get(
            url=f"{url}/ajax/cF1001.aspx",
            headers={'User-agent': 'Mozilla/5.0'},
            params=params,
        )
        print(resp.text)
        return encparam, encid

    _enc, _id = GetNvrEncparam("000660")

    print(_enc, _id)


    params = {
        "cmp_cd": '000660',
        "fin_typ": 0,
        "freq_typ": "A",
        # "extY": 0,
        # "extQ": 0,
        # "encparam": 'bExFc2UxdWlVYTdlaENLZlNLQWs2UT09',
        "encparam": _enc,
        # "id": 'ZTRzQlVCd0'
        "id": _id
    }
    resp = requests.get(
        url=f"{url}/ajax/cF1001.aspx",
        headers={'User-agent': 'Mozilla/5.0'},
        params=params,
    )
    print(resp.text)
    # for t in pd.read_html(resp.text):
    #     print(t)