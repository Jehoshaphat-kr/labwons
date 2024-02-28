from labwons.common.web import web
from nohji.deprecated.labwons.common.tools import str2num
from labwons.asset.kr.etf.fetch.__urls__ import urls
from pandas import DataFrame, Series
from typing import Union


def getMultiplesOutstanding(url:Union[str, urls]) -> Series:
    """
    :return:
        dividendYield     1.68
        fiscalPE         12.58
        priceToBook       1.15
        dtype: float64
    """
    if isinstance(url, urls):
        url = url.etf
    html = web.html(url)
    script = html.find_all('script')[-1].text.split('\n')
    pe = script[[n for n, h in enumerate(script) if "PER" in h][0] + 1]
    pb = script[[n for n, h in enumerate(script) if "PBR" in h][0] + 1]
    return Series({
        "dividendYield": str2num(html.find_all('td', class_='r cle')[-1].text),
        "fiscalPE": str2num(pe[pe.index(":"):]),
        "priceToBook": str2num(pb[pb.index(":"):])
    })

def getSectorWeights(url:Union[str, urls]) -> DataFrame:
    """
    :return:
                    KODEX 삼성그룹  유사펀드   시장
        섹터
        에너지                                2.44
        소재                                 10.09
        산업재              17.44      7.48   9.92
        경기소비재           2.67     11.58  10.57
        필수소비재                            2.85
        의료                10.37      5.64   7.46
        금융                12.47      6.49   7.74
        IT                  57.05     52.54  47.36
        통신서비스                            1.01
        유틸리티                              0.57
        미분류
    """
    if isinstance(url, urls):
        url = url.etf
    html = web.html(url)
    name = html.find("title").text.split('|')[0].replace("\xa0", " ")
    name = name[:name.find("(")]

    n, base = 100, ""
    src = str(html).split('\r\n')
    while n < len(src):
        if 'etf1StockInfoData' in src[n]:
            while not "];" in src[n + 1]:
                base += src[n + 1]
                n += 1
            break
        n += 1
    data = DataFrame(data=eval(base)).drop(columns=['val05'])
    data.columns = ["섹터", name, "유사펀드", "시장"]
    data = data.set_index(keys='섹터')
    for col in data:
        data[col] = data[col].apply(str2num)
    return data

def getSnapShot(url:Union[str, urls]) -> Series:
    """
    :return:
        date                 2023/11/17
        previousClose             12510
        fiftyTwoWeekHigh          13480
        fiftyTwoWeekLow           10950
        marketCap                 94069
        sharesOutstanding     751949461
        floatShares           663064556
        volume                   868029
        foreignRate                37.2
        beta                    0.74993
        return1M                    0.0
        return3M                  10.12
        return6M                   6.83
        return1Y                   5.13
        return3Y                  26.36
        dtype: object
    """
    if isinstance(url, urls):
        url = url.xml
    src = web.html(url).find('price')
    return Series({
        "date": src.find("date").text,
        "previousClose": str2num(src.find("close_val").text),
        "fiftyTwoWeekHigh": str2num(src.find("high52week").text),
        "fiftyTwoWeekLow": str2num(src.find("low52week").text),
        "marketCap": str2num(src.find("mkt_cap_1").text),
        "sharesOutstanding": str2num(src.find("listed_stock_1").text),
        "floatShares": str2num(src.find("ff_sher").text),
        "volume": str2num(src.find("deal_cnt").text),
        "foreignRate": str2num(src.find("frgn_rate").text),
        "beta": str2num(src.find("beta").text),
        "return1M": str2num(src.find("change_1month").text),
        "return3M": str2num(src.find("change_3month").text),
        "return6M": str2num(src.find("change_6month").text),
        "return1Y": str2num(src.find("change_12month").text),
        "return3Y": str2num(src.find("change_36month").text),
    })


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)


    myUrl = urls(
        # '102780' # KODEX 삼성그룹
        # '114800' # KODEX 인버스
        '069500' # KODEX 200
    )
    print(getSectorWeights(myUrl.etf))
    print(getMultiplesOutstanding(myUrl.etf))
    print(getSnapShot(myUrl.xml))

    print(getSectorWeights(myUrl))
    print(getMultiplesOutstanding(myUrl))
    print(getSnapShot(myUrl))
