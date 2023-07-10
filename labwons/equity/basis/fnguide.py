from bs4 import BeautifulSoup
import pandas as pd
import requests


def fnguide_business_summary(ticker:str) -> str:
    """
    Business Summary from FnGuide
    :return:
    [Example: 005930]
    한국 및 DX부문 해외 9개 지역총괄과 DS부문 해외 5개 지역총괄, SDC, Harman 등 233개의 종속기업으로 구성된 글로벌 전자기업임.
    세트사업(DX)에는 TV, 냉장고 등을 생산하는 CE부문과 스마트폰, 네트워크시스템, 컴퓨터 등을 생산하는 IM부문이 있음.
    부품사업(DS)에서는 D램, 낸드 플래쉬, 모바일AP 등의 제품을 생산하는 반도체 사업과 TFT-LCD 및 OLED 디스플레이 패널을 생산하는 DP사업으로 구성됨.

    글로벌 경기침체 여파로 주력인 반도체를 비롯해 스마트폰, TV 등 세트 부문 수요가 줄어들어 3분기 영업이익은 전년동기 대비 31.4% 감소함.
    DS부문은 실적 버팀목이던 메모리반도체 부진으로 영업이익이 절반 수준으로 감소함.
    전체 영업이익에서 차지하는 비중도 47%로 낮아짐.
    DC부문은 영업이익 2조원을 기록하며 최대 실적을 달성함.
    폴더블을 포함한 스마트폰 신제품 출시에 수요가 증가하고, 애플 판매량 호조에 영향을 받음.
    """
    u = "http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A%s&cID=&MenuYn=Y&ReportGB=D&NewMenuID=Y&stkGb=701"
    html = BeautifulSoup(requests.get(u % ticker).content, 'lxml').find('ul', id='bizSummaryContent').find_all('li')
    t = '\n\n '.join([e.text for e in html])
    w = [
        '.\n' if t[n] == '.' and not any([t[n - 1].isdigit(), t[n + 1].isdigit(), t[n + 1].isalpha()]) else t[n]
        for n in range(1, len(t) - 2)
    ]
    s = ' ' + t[0] + ''.join(w) + t[-2] + t[-1]
    return s.replace(' ', '').replace('\xa0\xa0', ' ').replace('\xa0', ' ').replace('\n ', '\n')

def fnguide_etf(ticker:str):
    """
    FuGuide provided ETF general information
    :return:
    [Example: 091160]

    """
    u = f"http://comp.fnguide.com/SVO2/ASP/" \
        f"etf_snapshot.asp?pGB=1&gicode=A{ticker}&cID=&MenuYn=Y&ReportGB=&NewMenuID=401&stkGb=770"

    key = ''
    dataset = {'price':[], 'comp':[], 'sector':[]}
    for line in requests.get(u).text.split('\n'):
        if "etf1PriceData" in line:
            key = 'price'
        if "etf1StyleInfoStkData" in line:
            key = 'comp'
        if "etf1StockInfoData" in line:
            key = 'sector'
        if "]" in line and key:
            key = ''
        if key:
            dataset[key].append(line)
    return (pd.DataFrame(data=eval(f"[{''.join(dataset[k][1:])}]")).set_index(keys='val01')['val02'] for k in dataset)

