from datetime import datetime, timedelta
from bs4 import BeautifulSoup as Soup
from pykrx.stock import (
    get_market_cap_by_date,
    get_etf_portfolio_deposit_file
)
from urllib.request import urlopen
from lxml import etree
import pandas as pd
import numpy as np
import requests, json


def str2num(src:str) -> int or float:
    src = "".join([char for char in src if char.isdigit() or char == "."])
    if not src:
        return np.nan
    if "." in src:
        return float(src)
    return int(src)

def snapshot(url:str) -> pd.Series:
    """
    * COMMON for EQUITY, ETF
    :param url: [str] startswith('cdn.fnguide.com') ~ endswith('.xml')
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
    src = Soup(requests.get(url).content, 'xml').find('price')
    return pd.Series({
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

def stockHeader(url:str) -> pd.Series:
    """
    * EQUITY ONLY
    :param url: [str]
    :return:
        fiscalPE         2.90
        forwardPE        3.06
        sectorPE         6.17
        priceToBook      0.32
        dividendYield    9.03
        dtype: float64
    """
    src = Soup(requests.get(url).content, 'lxml').find('div', id='corp_group2')
    src = [val for val in src.text.split('\n') if val]
    return pd.Series({
        "fiscalPE": str2num(src[src.index('PER') + 1]),
        "forwardPE": str2num(src[src.index('12M PER') + 1]),
        "sectorPE": str2num(src[src.index('업종 PER') + 1]),
        "priceToBook": str2num(src[src.index('PBR') + 1]),
        "dividendYield": str2num(src[src.index('배당수익률') + 1]),
    })

def etfMultiples(url:str):
    """
    * ETF ONLY
    :param url: [str]
    :return:
        dividendYield     1.68
        fiscalPE         12.58
        priceToBook       1.15
        dtype: float64
    """
    src = Soup(requests.get(url).content, 'lxml')
    script = src.find_all('script')[-1].text.split('\n')
    pe = script[[n for n, h in enumerate(script) if "PER" in h][0] + 1]
    pb = script[[n for n, h in enumerate(script) if "PBR" in h][0] + 1]
    return pd.Series({
        "dividendYield": str2num(src.find_all('td', class_='r cle')[-1].text),
        "fiscalPE" : str2num(pe[pe.index(":"): ]),
        "priceToBook": str2num(pb[pb.index(":"):])
    })



if __name__ == "__main__":
    # ticker = '316140' # 우리금융지주
    ticker = '102780'

    xml = f"http://cdn.fnguide.com/SVO2/xml/Snapshot_all/{ticker}.xml"
    url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=101&stkGb=701"
    etf = f"http://comp.fnguide.com/SVO2/ASP/etf_snapshot.asp?pGB=1&gicode=A102780&cID=&MenuYn=Y&ReportGB=&NewMenuID=401&stkGb=770"

    # print(snapshot(xml))
    # print(stockHeader(url))
    # print(etfMultiples(etf))