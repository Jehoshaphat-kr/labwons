from labwons.common.web import web
from nohji.deprecated.labwons.common.tools import str2num
from labwons.asset.kr.stock.fetch.__urls__ import urls
from pandas import DataFrame, Series
from typing import Union


def getCurrentPrice(url:Union[str, urls]) -> int:
    """
    :return:
        현재(종)가
    """
    if isinstance(url, urls):
        url = url.naver
    html = web.html(url)
    curr = [d.text for d in html.find_all("dd") if d.text.startswith("현재가")][0]
    return str2num(curr[curr.index("현재가 ") + 4: curr.index(" 전일대비")])

def getAnalogy(url:Union[str, urls]) -> DataFrame:
    """
    :return:
                    종목명  현재가 등락률 시가총액(억) 외국인비율(%)  매출액(억) 영업이익(억)  ...  PER(%) PBR(배)
        058470    리노공업  143800  -1.57        21918         37.25         751          336  ...   21.69    4.35
        005930    삼성전자   70600   0.14      4214666         53.21      600055         6685  ...   13.47    1.37
        000660  SK하이닉스  132000   1.15       960963         52.59       73059       -28821  ...  -11.73    1.58
        402340    SK스퀘어   48450   0.41        67336         45.29       -1274        -7345  ...   -3.64    0.43
        042700  한미반도체   60200  -9.20        58598         12.38         491          112  ...   29.07   10.80

    :columns: ['종목명', '현재가', '등락률', '시가총액(억)', '외국인비율(%)', '매출액(억)', '영업이익(억)',
               '조정영업이익(억)', '영업이익증가율(%)', '당기순이익(억)', '주당순이익(원)', 'ROE(%)', 'PER(%)',
               'PBR(배)']
    """
    if isinstance(url, urls):
        url = url.naver
    data = web.list(url)[4]
    data = data.set_index(keys='종목명').drop(index=['전일대비'])
    data.index.name = None
    for col in data:
        data[col] = data[col].apply(str2num)
    data = data.T
    data["종목명"] = [i.replace('*', '')[:-6] for i in data.index]
    data.index = [i[-6:] for i in data.index]
    return data

def getMultiplesTrailing(url:Union[str, urls]) -> Series:
    """
    :return:
        trailingPE         30.53
        trailingEps     16642.00
        estimatePE         22.00
        estimateEps     22901.00
        priceToBook         1.22
        bookValue      416754.00
        dividendYield        2.1
        dtype: float64
    """
    if isinstance(url, urls):
        url = url.naver
    data = web.list(url)[8]
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




if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    myURL = urls(
        # "005930" # SamsungElec
        # "000660" # SK hynix
        # "207940" # SAMSUNG BIOLOGICS
        # "005380" # HyundaiMtr
        # "005490"  # POSCO
        # "035420" # NAVER Corporation
        # "000270" # Kia Corporation
        # "051910" # LG Chem, Ltd.
        # "006400" # Samsung SDI Co., Ltd.
        # "068270" # Celltrion, Inc.
        "035720" # Kakao Corp.
        # "028260" # Samsung C&T Corporation
        # "105560" # KB Financial Group Inc.
        # "012330" # Mobis
        # "055550" # Shinhan Financial Group Co., Ltd.
        # "066570" # LG Electronics Inc.
        # "032830" # Samsung Life Insurance Co., Ltd.
        # "096770" # SK Innovation Co., Ltd.
        # "003550" # LG Corp.
        # "015760" # Korea Electric Power Corporation
        # "017670" # SK Telecom Co.,Ltd
        # "316140" # Woori Financial Group Inc.

        # "359090"  # C&R Research
        # "042660"  # Daewoo Shipbuilding & Marine Engineering Co.,Ltd
        # "021080" # Atinum Investment
        # "130500" # GH Advanced Materials Inc.
        # "323280" # SHT-5 SPAC
    )
    print(getAnalogy(myURL))
    print(getCurrentPrice(myURL))
    print(getMultiplesTrailing(myURL))
