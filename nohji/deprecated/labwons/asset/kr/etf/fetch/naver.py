from labwons.common.web import web
from nohji.deprecated.labwons.common.tools import str2num
from labwons.asset.kr.etf.fetch.__urls__ import urls
from datetime import datetime
from typing import Union


def getCurrentPrice(url:Union[str, urls]) -> int or float:
    if isinstance(url, urls):
        url = url.naver
    html = web.html(url)
    curr = [d.text for d in html.find_all("dd") if d.text.startswith("현재가")][0]
    return str2num(curr[curr.index("현재가 ") + 4: curr.index(" 전일대비")])

def getIpo(url:Union[str, urls]) -> datetime.date:
    if isinstance(url, urls):
        url = url.naver
    return datetime.strptime(str(str2num(web.list(url)[6].iloc[-1, -1])), "%Y%m%d").date()

def getUnderlyingAsset(url:Union[str, urls]) -> str:
    if isinstance(url, urls):
        url = url.naver
    return web.list(url)[6].columns[-1]

def getNav(url:Union[str, urls]) -> int or float:
    if isinstance(url, urls):
        url = url.naver
    return str2num(web.list(url)[8].columns[-1])


if __name__ == "__main__":
    from labwons.asset.kr.etf.fetch.__urls__ import urls
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    myUrl = urls(
        "069500"
    )
    # print(getCurrentPrice(myUrl.naver))
    # print(getUnderlyingAsset(myUrl.naver))
    # print(getNav(myUrl.naver))

    print(getCurrentPrice(myUrl))
    print(getIpo(myUrl))
    print(getUnderlyingAsset(myUrl))
    print(getNav(myUrl))
