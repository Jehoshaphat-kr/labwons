from labwons.common.metadata.metadata import MetaData
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

str2int = lambda x: np.nan if not x else int(x.replace(', ', '').replace(',', ''))
class fnguide(object):

    def __init__(self, ticker:str):
        self._t = ticker
        return

    def __url__(self, page:str, hold:str='') -> str:
        """
        :param page : [str]
        :param hold : [str] 연결 - "D" 또는 "" / 별도 - "B"
        :return:
        """
        url = f"http://comp.fnguide.com/SVO2/ASP/%s.asp?" \
            f"pGB=1&" \
            f"gicode=A{self._t}&" \
            f"cID=&" \
            f"MenuYn=Y&" \
            f"ReportGB=%s&" \
            f"NewMenuID=%s&" \
            f"stkGb=%s"
        pages = {
            "SVD_Main": {
                "ReportGB": "",
                "NewMenuID": "Y",
                "stkGb": "701"
            },
            "SVD_Corp": {
                "ReportGB": "",
                "NewMenuID": "102",
                "stkGb": "701"
            },
            "SVD_Finance": {
                "ReportGB": hold,
                "NewMenuID": "103",
                "stkGb": "701"
            },
            "SVD_FinanceRatio": {
                "ReportGB": hold,
                "NewMenuID": "104",
                "stkGb": "701"
            },
            "SVD_Invest": {
                "ReportGB": "",
                "NewMenuID": "105",
                "stkGb": "701"
            },
            "ETF_Snapshot": {
                "ReportGB": "",
                "NewMenuID": "401",
                "stkGb": "770"
            }
        }
        if not page in pages or not hold in ['', 'D', 'B', 'A']:
            raise KeyError
        return url % (page, pages[page]["ReportGB"], pages[page]["NewMenuID"], pages[page]["stkGb"])

    def __tb__(self, page:str, hold:str='') -> list:
        if not hasattr(self, f"_u{page}{hold}"):
            self.__setattr__(f'_u{page}{hold}', pd.read_html(self.__url__(page, hold), header=0))
        return self.__getattribute__(f'_u{page}{hold}')

    @property
    def __gb__(self) -> str:
        if not hasattr(self, f"_gb"):
            html = self.__tb__('SVD_Main')
            self.__setattr__('_gb', "B" if html[11].iloc[1].isnull().sum() > html[14].iloc[1].isnull().sum() else "D")
        return self.__getattribute__('_gb')

    @property
    def __xml__(self) -> etree.ElementTree:
        if not hasattr(self, "_xml"):
            req = requests.get(url=f"http://cdn.fnguide.com/SVO2/xml/Snapshot_all/{self._t}.xml").text[39:]
            self.__setattr__("_xml", etree.fromstring(req).find("price"))
        return self.__getattribute__("_xml")

    @property
    def __pg__(self) -> Soup:
        if not hasattr(self, "_page"):
            self.__setattr__("_page", Soup(requests.get(self.__url__('SVD_Main')).content, 'lxml'))
        return self.__getattribute__("_page")

    @property
    def __pgh__(self) -> list:
        if not hasattr(self, "_page_header"):
            try:
                header = [val for val in self.__pg__.find('div', id='corp_group2').text.split('\n') if val]
            except AttributeError:
                header = self.__pg__.find_all('script')[-1].text.split('\n')
            self.__setattr__("_page_header", header)
        return self.__getattribute__("_page_header")

    @property
    def __cap__(self) -> pd.DataFrame:
        if not hasattr(self, '_cap'):
            cap = get_market_cap_by_date(
                fromdate=(datetime.today() - timedelta(365 * 5)).strftime("%Y%m%d"),
                todate=datetime.today().strftime("%Y%m%d"),
                freq='m',
                ticker=self._t
            )
            cap = cap[
                cap.index.astype(str).str.contains('03') | \
                cap.index.astype(str).str.contains('06') | \
                cap.index.astype(str).str.contains('09') | \
                cap.index.astype(str).str.contains('12') | \
                (cap.index == cap.index[-1])
            ]
            cap.index = cap.index.strftime("%Y/%m")
            cap['시가총액'] = round(cap['시가총액'] / 100000000, 0)
            self.__setattr__('_cap', cap[['시가총액']])
        return self.__getattribute__('_cap')

    @staticmethod
    def _finance(data:pd.DataFrame) -> pd.DataFrame:
        data = data.set_index(keys=[data.columns[0]])
        data = data.drop(columns=[col for col in data if not col.startswith('20')])
        data.index.name = None
        data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:])//3}Q"]
        data.index = [
            i.replace('계산에 참여한 계정 펼치기', '').replace('(', '').replace(')', '').replace('*', '') for i in data.index
        ]
        return data.T.astype(float)

    def _overview(self, data:pd.DataFrame) -> pd.DataFrame:
        data = data.set_index(keys=[data.columns[0]])
        if isinstance(data.columns[0], tuple):
            data.columns = data.columns.droplevel()
        else:
            data.columns = data.iloc[0]
            data = data.drop(index=data.index[0])

        data = data.T
        data = data.head(len(data) - len([i for i in data.index if i.endswith(')')]) + 1)
        data.index.name = '기말'

        cap = self.__cap__.copy()
        cap.index = cap.index[:-1].tolist() + [data.index[-1]]
        return data.join(other=cap, how='left')[cap.columns.tolist() + data.columns.tolist()].astype(float)

    def _multipleBand(self, header:str) -> pd.DataFrame:
        if not hasattr(self, '_band_src'):
            url = f"http://cdn.fnguide.com/SVO2/json/chart/01_06/chart_A{self._t}_D.json"
            src = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
            self.__setattr__('_band_src', src)
        src = self.__getattribute__('_band_src')
        header = pd.DataFrame(src[header])[['ID', 'NAME']].set_index(keys='ID')
        header = header.to_dict()['NAME']
        header.update({'GS_YM': '날짜', 'PRICE': '종가'})
        data = pd.DataFrame(src['CHART'])
        data = data[header.keys()].replace('-', np.nan).replace('', np.nan)
        data['GS_YM'] = pd.to_datetime(data['GS_YM'])
        return data.rename(columns=header).set_index(keys='날짜').astype(float)
    
    def _consensusProfit(self, period:str) -> pd.DataFrame:
        columns = {
            "GS_YM": "기말",
            "SALES_R": "매출실적", "SALES_F": "매출전망",
            "OP_R": "영업이익실적", "OP_F": "영업이익전망"
        }
        url = f"https://cdn.fnguide.com/SVO2/json/chart/07_01/chart_A{self._t}_{self.__gb__}_{period}.json"
        raw = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        basis = pd.DataFrame(raw['CHART']).replace('-', np.nan)[columns.keys()]
        basis = basis.rename(columns=columns)
        return basis.set_index(keys="기말").astype(float)

    def _consensusSeries(self, year:str) -> pd.DataFrame:
        columns = {
            "STD_DT": "날짜",
            "SALES": "매출", "SALES_MAX": "매출(최대)", "SALES_MIN": "매출(최소)",
            "OP": "영업이익", "OP_MAX": "영업이익(최대)", "OP_MIN": "영업이익(최소)",
            "EPS": "EPS", "EPS_MAX": "EPS(최대)", "EPS_MIN": "EPS(최소)",
            "PER": "PER", "PER_MAX": "PER(최대)", "PER_MIN": "PER(최소)", "PER_12F": "12M PER"
        }
        url = f"https://cdn.fnguide.com/SVO2/json/chart/07_02/chart_A{self._t}_{self.__gb__}_FY{year}.json"
        raw = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        basis = pd.DataFrame(raw['CHART'])[columns.keys()]
        basis = basis.rename(columns=columns)
        basis = basis.set_index(keys='날짜')
        basis = basis.replace('', np.nan)
        for col in basis:
            basis[col] = basis[col].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)
        return basis.astype(float)

    @property
    def previousClose(self) -> int:
        return str2num(self.__xml__.find("close_val").text)

    @property
    def previousForeignRate(self) -> float:
        return str2num(self.__xml__.find('frgn_rate').text)

    @property
    def beta(self) -> float:
        return str2num(self.__xml__.find("beta").text)

    @property
    def volume(self) -> int:
        return str2num(self.__xml__.find('deal_cnt').text)

    @property
    def sharesOutstanding(self) -> int:
        return str2num(self.__xml__.find('listed_stock_1').text)

    @property
    def floatShares(self) -> int:
        return str2num(self.__xml__.find('ff_sher').text)

    @property
    def floatSharesRate(self) -> float:
        return round(100 * self.floatShares / self.sharesOutstanding, 2)

    @property
    def marketCap(self) -> int:
        return str2num(self.__xml__.find('mkt_cap_1').text)

    @property
    def fiftyTwoWeekLow(self) -> int:
        return str2num(self.__xml__.find('low52week').text)

    @property
    def fiftyTwoWeekLowRate(self) -> float:
        return round(100 * (self.previousClose / self.fiftyTwoWeekLow - 1), 2)

    @property
    def fiftyTwoWeekHigh(self) -> int:
        return str2num(self.__xml__.find('high52week').text)

    @property
    def fiftyTwoWeekHighRate(self) -> float:
        return  round(100 * (self.previousClose / self.fiftyTwoWeekHigh - 1), 2)

    @property
    def forwardPE(self) -> float:
        try:
            return str2num(self.__pgh__[self.__pgh__.index('12M PER') + 1])
        except ValueError:
            return np.nan

    @property
    def dividendYield(self) -> float:
        try:
            return str2num(self.__pgh__[self.__pgh__.index('배당수익률') + 1])
        except ValueError:
            return str2num(self.__pg__.find_all('td', class_='r cle')[-1].text)

    @property
    def fiscalPE(self) -> float:
        try:
            return str2num(self.__pgh__[self.__pgh__.index('PER') + 1])
        except ValueError:
            val = self.__pgh__[[n for n, h in enumerate(self.__pgh__) if "PER" in h][0] + 1]
            return str2num(val[val.index(":"): ])

    @property
    def fiscalEps(self) -> int:
        return int(1 / (self.fiscalPE / self.previousClose))

    @property
    def priceToBook(self) -> float:
        try:
            return str2num(self.__pgh__[self.__pgh__.index('PBR') + 1])
        except ValueError:
            val = self.__pgh__[[n for n, h in enumerate(self.__pgh__) if "PBR" in h][0] + 1]
            return str2num(val[val.index(":"):])

    @property
    def fiscalPS(self) -> float:
        return round(self.previousClose / float(self.annualMultiples["SPS"].values[-2]), 2)

    @property
    def trailingEpsGrowth(self) -> float:
        return float(self.annualGrowthRate["EPS증가율"].values[-1])

    @property
    def targetPrice(self) -> float:
        try:
            return float(self.__tb__('SVD_Main')[7]["목표주가"][0])
        except ValueError:
            return self.fiftyTwoWeekHigh

    @property
    def businessSummary(self) -> str:
        html = self.__pg__.find('ul', id='bizSummaryContent').find_all('li')
        t = '\n\n '.join([e.text for e in html])
        w = [
            '.\n' if t[n] == '.' and not any([t[n - 1].isdigit(), t[n + 1].isdigit(), t[n + 1].isalpha()]) else t[n]
            for n in range(1, len(t) - 2)
        ]
        s = ' ' + t[0] + ''.join(w) + t[-2] + t[-1]
        return s.replace(' ', '').replace('\xa0\xa0', ' ').replace('\xa0', ' ').replace('\n ', '\n')

    @property
    def annualOverview(self) -> pd.DataFrame:
        return self._overview(self.__tb__('SVD_Main')[11] if self.__gb__ == 'D' else self.__tb__('SVD_Main')[14])

    @property
    def annualProducts(self) -> pd.DataFrame:
        """
        :return:
                 반도체 부문
        기말
        2019/12        100.0
        2020/12        100.0
        2021/12        100.0
        2022/12        100.0
        """
        url = f"http://cdn.fnguide.com/SVO2//json/chart/02/chart_A{self._t}_01_N.json"
        src = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'), strict=False)
        header = pd.DataFrame(src['chart_H'])[['ID', 'NAME']].set_index(keys='ID').to_dict()['NAME']
        header.update({'PRODUCT_DATE': '기말'})
        data = pd.DataFrame(src['chart']).rename(columns=header).set_index(keys='기말')
        data = data.drop(columns=[c for c in data.columns if data[c].astype(float).sum() == 0])

        i = data.columns[-1]
        data['Sum'] = data.astype(float).sum(axis=1)
        data = data[(90 <= data.Sum) & (data.Sum < 110)].astype(float)
        data[i] = data[i] - (data.Sum - 100)
        return data.drop(columns=['Sum'])

    @property
    def annualExpenses(self) -> pd.DataFrame:
        html = self.__tb__('SVD_Corp')
        data = pd.concat(
            objs=[
                html[4 if self.__gb__ == 'D' else 6].set_index(keys=['항목']).T,  # 매출원가율
                html[5 if self.__gb__ == 'D' else 7].set_index(keys=['항목']).T,  # 판관비
            ], axis=1
        )
        data.columns.name = None
        data.index.name = '기말'
        return data

    @property
    def annualSalesShares(self) -> pd.DataFrame:
        """
        :return:
                        기타   드라마 판매   드라마 편성
                  내수  수출   내수   수출    내수  수출
        2020/12    NaN   NaN    NaN    NaN     NaN   NaN
        2021/12    NaN   NaN    NaN    NaN     NaN   NaN
        2022/12  97.20  2.80  23.40  76.60  100.00  0.00
        """
        src = self.__tb__('SVD_Corp')[10 if self.__gb__ == 'D' else 11]
        data = src[src.columns[1:]].set_index(keys=src.columns[1])
        data = data.T.copy()
        data.columns = [col.replace("\xa0", " ") for col in data.columns]
        domestic = data[data[data.columns[0]] == "내수"].drop(columns=data.columns[0])
        exported = data[data[data.columns[0]] == "수출"].drop(columns=data.columns[0])
        domestic.index = exported.index = [i.replace('.1', '') for i in domestic.index]
        domestic.columns.name = exported.columns.name = None
        data = pd.concat(objs={"내수": domestic, "수출": exported}, axis=1)
        # return data # 내수/수출 구분 우선 시

        data = pd.concat(objs={(c[1], c[0]): data[c] for c in data}, axis=1)
        return data[sorted(data.columns, key=lambda x: x[0])] # 상품 구분 우선 시

    @property
    def annualHolders(self) -> pd.DataFrame:
        """
        :return:
                    최대주주등 10%이상주주 5%이상주주 임원 자기주식 우리사주조합
        2021/01/01       56.03         NaN       6.26  NaN      NaN          NaN
        2022/01/01       54.95         NaN       6.25  NaN      NaN          NaN
        2023/01/01       54.79         NaN       6.25  NaN      NaN          NaN
        2023/11/14       54.79         NaN       6.25  NaN      NaN          NaN
        """
        data = self.__tb__('SVD_Corp')[12]
        data = data.set_index(keys=[data.columns[0]])
        data.index.name = None
        data.index = [col[:col.index("(") - 1] if "(" in col else col for col in data.index]
        data.index = [i.replace(" ", "").replace("&nbsp;", "") for i in data.index]
        return data.T

    @property
    def annualProfit(self) -> pd.DataFrame:
        """
        columns: ['매출액', '매출원가', '매출총이익', '판매비와관리비', '영업이익', '영업이익발표기준',
                  '금융수익', '금융원가', '기타수익', '기타비용', '종속기업,공동지배기업및관계기업관련손익',
                  '세전계속사업이익', '법인세비용', '계속영업이익', '중단영업이익', '당기순이익',
                  '지배주주순이익', '비지배주주순이익']
        :return:
                 매출액 매출원가 매출총이익 판매비와관리비 영업이익 금융수익 금융원가 기타수익 기타비용 ... 당기순이익
        2020/12  319004   210898     108106          57980    50126    33279    19804      848     1716 ...      47589
        2021/12  429978   240456     189522   		 65419   124103    23775    14699     1161     1804 ...      96162
        2022/12  446216   289937     156279  		 88184    68094    37143    50916     2414    18019 ...      22417
        2023/2Q  123940   152172     -28231  		 34613   -62844    15203    25144      261      739 ...     -55734
        """
        return self._finance(self.__tb__('SVD_Finance', self.__gb__)[0])

    @property
    def annualInventory(self) -> pd.DataFrame:
        """
        :return:
                재고자산 재고비율
        2020/12   49804      7.77
        2021/12   54954      6.47
        2022/12  103457     11.27
        2023/2Q  112521     12.13
        """
        data = self._finance(self.__tb__('SVD_Finance', 'A')[2])
        data["재고비율"] = round(100 * data["재고자산"] / data["자산총계"], 2)
        return data[["재고자산", "재고비율"]].fillna(0).astype(float)

    @property
    def annualCashFlow(self) -> pd.DataFrame:
        """
        :return:
                 영업현금흐름  투자현금흐름  재무현금흐름  환율변동손익  현금및현금성자산
        2020/12        123146       -118404          2521          -563             29760
        2021/12        197976       -223923         44923          1843             50580
        2022/12        147805       -178837         28218          2005             49770
        2023/2Q         -6940        -53509         70579           508             60408
        """
        data = self._finance(self.__tb__('SVD_Finance', self.__gb__)[4])
        cols = {
            "영업활동으로인한현금흐름": "영업현금흐름",
            "투자활동으로인한현금흐름": "투자현금흐름",
            "재무활동으로인한현금흐름": "재무현금흐름",
            "환율변동효과": "환율변동손익",
            "기말현금및현금성자산": "현금및현금성자산"
        }
        return data[list(cols.keys())].rename(columns=cols).fillna(0).astype(int)

    @property
    def annualGrowthRate(self) -> pd.DataFrame:
        """
        :return:
                매출액증가율 판매비와관리비증가율 영업이익증가율 EBITDA증가율 EPS증가율
        2019/12        -33.3                 23.4          -87.0        -58.4     -87.1
        2020/12         18.2                  6.3           84.3         30.4     137.1
        2021/12         34.8                 12.8          147.6         56.0     101.9
        2022/12          3.8                 34.8          -45.1         -9.1     -76.8
        2023/2Q        -52.3                -26.0            NaN        -94.4       NaN
        """
        data = self.__tb__('SVD_FinanceRatio', self.__gb__)[0]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('성장성비율') + 1 : index.index('수익성비율')])
    
    @property
    def annualProfitRate(self) -> pd.DataFrame:
        """
        :return:
                 매출총이익율 세전계속사업이익률 영업이익률 EBITDA마진율    ROA    ROE   ROIC
        2019/12          30.3                9.0       10.1         42.0    3.1    4.2    5.0
        2020/12          33.9               19.6       15.7         46.4    7.0    9.5    7.4
        2021/12          44.1               31.2       28.9         53.7   11.5   16.8   15.3
        2022/12          35.0                9.0       15.3         47.0    2.2    3.6    5.5
        2023/2Q         -22.8              -59.0      -50.7          6.3  -10.8  -18.5  -12.7
        """
        data = self.__tb__('SVD_FinanceRatio', self.__gb__)[0]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('수익성비율') + 1: index.index('활동성비율')])

    @property
    def annualMultiples(self) -> pd.DataFrame:
        """
        columns: ['EPS', 'EBITDAPS', 'CFPS', 'SPS', 'BPS', 'DPS보통주', 'DPS1우선주', '배당성향',
                  'PER', 'PCR', 'PSR', 'PBR', 'EV/Sales', 'EV/EBITDA', '총현금흐름', '세후영업이익',
                  '유무형자산상각비', '총투자', 'FCFF']
        :return:
                   EPS  EBITDAPS   CFPS    SPS    BPS  DPS보통주  DPS1우선주  배당성향   PER   PCR   PSR  ...   FCFF
        2019/12   2755     15576  14597  37075  69271       1000         NaN     34.0  34.15  6.45  2.54  ... -98006
        2020/12   6532     20309  19955  43819  74721       1170         NaN     17.0  18.14  5.94  2.70  ...  23760
        2021/12  13190     31685  27828  59063  88543       1540         NaN     11.0   9.93  4.71  2.22  ... -27789
        2022/12   3063     28792  22501  61293  90064       1200         NaN     37.0  24.49  3.33  1.22  ... -65070
        2023/2Q  -7653      1078   2058  17025  82019        600         NaN      NaN    NaN   NaN   NaN  ... -65503
        """
        data = self.__tb__('SVD_Invest', self.__gb__)[3]
        data = data[~data[data.columns[0]].isin(["Per\xa0Share", "Dividends", "Multiples", "FCF"])]
        data = self._finance(data)
        data.columns = [c.replace("원", "").replace(",현금", "").replace("현금%", "") for c in data.columns]
        return data

    @property
    def quarterOverview(self) -> pd.DataFrame:
        return self._overview(self.__tb__('SVD_Main')[12] if self.__gb__ == 'D' else self.__tb__('SVD_Main')[15])

    @property
    def quarterProfitLoss(self) -> pd.DataFrame:
        return self._finance(self.__tb__('SVD_Finance', self.__gb__)[1])

    @property
    def quarterAsset(self) -> pd.DataFrame:
        return self._finance(self.__tb__('SVD_Finance', self.__gb__)[3])

    @property
    def quarterCashFlow(self) -> pd.DataFrame:
        return self._finance(self.__tb__('SVD_Finance', self.__gb__)[5])

    @property
    def quarterGrowthRate(self) -> pd.DataFrame:
        data = self.__tb__('SVD_FinanceRatio', self.__gb__)[1]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('성장성비율') + 1: index.index('수익성비율')])

    @property
    def quarterProfitRate(self) -> pd.DataFrame:
        data = self.__tb__('SVD_FinanceRatio', self.__gb__)[1]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('수익성비율') + 1: ])

    @property
    def foreignRate(self) -> pd.DataFrame:
        """
        외국인보유비중(시계열) : 기간별 사용 시 .dropna() 사용
        :return: 
                                 3M               1Y               3Y
                        종가   비중      종가   비중      종가   비중
        날짜                                                           
        2020-10-01       NaN    NaN       NaN    NaN  117090.0  42.69
        2020-11-01       NaN    NaN       NaN    NaN  124662.0  42.62
        2020-12-01       NaN    NaN       NaN    NaN  125610.0  42.78
        ...              ...    ...       ...    ...       ...    ...
        2023-10-12  158000.0  36.86       NaN    NaN       NaN    NaN
        2023-10-13  157300.0  36.99       NaN    NaN       NaN    NaN
        2023-10-16  156800.0  37.07  155780.0  36.91       NaN    NaN        
        """
        objs = dict()
        for dt in ['3M', '1Y', '3Y']:
            url = f"http://cdn.fnguide.com/SVO2/json/chart/01_01/chart_A{self._t}_{dt}.json"
            data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
            frm = pd.DataFrame(data["CHART"])[['TRD_DT', 'J_PRC', 'FRG_RT']]
            frm = frm.rename(columns={'TRD_DT': '날짜', 'J_PRC': '종가', 'FRG_RT': '비중'}).set_index(keys='날짜')
            frm.index = pd.to_datetime(frm.index)
            frm = frm.replace('', '0.0')
            objs[dt] = frm
        return pd.concat(objs=objs, axis=1).astype(float)
    
    @property
    def consensus(self) -> pd.DataFrame:
        """
        컨센서스 (발행 의견의 전체 평균)
        :return:
                   투자의견  컨센서스    종가   격차
        날짜
        2022-10-17    4.00     180000  139900 -22.28
        2022-10-18    4.00     180000  139700 -22.39
        2022-10-19    4.00     180000  135800 -24.56
        ...            ...        ...     ...    ...
        2023-10-12    4.00     198000  158000 -20.20
        2023-10-13    4.00     198000  157300 -20.56
        2023-10-16    4.00     198333  156800 -20.94
        """
        url = f"http://cdn.fnguide.com/SVO2/json/chart/01_02/chart_A{self._t}.json"
        raw = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        basis = pd.DataFrame(raw['CHART'])
        basis = basis.rename(columns={'TRD_DT': '날짜', 'VAL1': '투자의견', 'VAL2': '컨센서스', 'VAL3': '종가'})
        basis = basis.set_index(keys='날짜')
        basis.index = pd.to_datetime(basis.index)
        basis = basis.astype(float)
        basis['격차'] = round(100 * (basis['종가'] / basis['컨센서스'] - 1), 2)
        return basis

    @property
    def consensusAnnualProfit(self) -> pd.DataFrame:
        """
        컨센서스 영업이익 실적(연간)
        :return:
                   매출실적    매출전망  영업이익실적  영업이익전망
        기말
        2020/12  2368069.88  2363386.08     359938.76     362889.46
        2021/12  2796047.99  2781487.45     516338.56        528376
        2022/12   3022313.6  3047210.04      433766.3     459810.75
        2023/12         NaN  2609787.67           NaN      72144.57
        2024/12         NaN  2955967.19           NaN     331331.43
        2025/12         NaN  3259557.88           NaN     456468.88
        """
        return self._consensusProfit('A')

    @property
    def consensusQuarterProfit(self) -> pd.DataFrame:
        """
        컨센서스 영업이익 실적(분기)
        :return:
                  매출실적   매출전망  영업이익실적  영업이익전망
        분기
        2023/03  637453.71  642011.82       6401.78      10000.91
        2023/06  600055.33  618592.73       6685.47       2817.73
        2023/09     670000  679076.36         24000      21343.64
        2023/12        NaN  700258.57           NaN       36391.9
        2024/03        NaN  711187.78           NaN      50888.89
        2024/06        NaN  700681.11           NaN      65308.89
        """
        return self._consensusProfit('Q')

    @property
    def consensusThisYear(self) -> pd.DataFrame:
        """
        컨센서스 추이
        :return:
                       매출  매출(최대)  매출(최소)   영업이익  영업이익(최대) 영업이익(최소)      EPS  EPS(최대)  EPS(최소)    PER  PER(최대)  PER(최소)  12M PER
        날짜
        2022/11   3063374.5     3288390     2826800     336985          419430         265250  3935.14    4842.57    3249.68  15.81      19.14      12.84     15.3
        2022/12  2942704.08     3173270     2635050     291990          389990         196600  3463.21    4294.48    2662.58  15.97      20.77      12.88    15.97
        2023/01  2820243.82     3073260     2635050  211293.59          342396         128930  2583.89    4140.17    1589.21  23.61      38.38      14.73    22.15
        2023/02  2728378.14     3073260     2581450  168233.05          329278          97490  2269.22    3734.23    1346.16  26.71      45.02      16.23    22.45
        2023/03   2723824.5     2900830     2594060  114761.09          184940          42540  1735.61    3137.21     758.32  36.87       84.4       20.4    25.65
        2023/04  2688688.59     2884560     2560260     100754          184940          46570  1624.44    3351.85     932.77  40.32      70.22      19.54    25.21
        2023/05  2678715.91     2884560     2540150   95985.36          122270          59390  1556.63    3351.85    1068.80  45.87       66.8       21.3    24.93
        2023/06  2660441.74     2785651     2476590   95079.48          122270          59390  1548.96    3477.57    1068.80  46.61      67.55      20.76    23.27
        2023/07  2604180.14     2708860     2527000   85640.81          126210          61590  1593.81    3442.83     963.24  43.79      72.46      20.27    19.75
        2023/08  2609199.41     2708860     2527000   85829.45          126210          46620  1510.10    3442.83     963.24   44.3      69.45      19.43       18
        2023/09   2613926.3     2708860     2527000   71636.43          100390          41620  1358.22    3442.83     832.63  50.36      82.15      19.87    18.16
        2023/10  2609787.67     2661845     2528300   72144.57           96690          57010  1264.41    1722.45     908.63  54.41      75.72      39.94    19.22
        """
        return self._consensusSeries('1')

    @property
    def consensusNextYear(self) -> pd.DataFrame:
        """
        컨센서스 추이
        :return:
                       매출  매출(최대)  매출(최소)   영업이익  영업이익(최대) 영업이익(최소)      EPS  EPS(최대)  EPS(최소)    PER  PER(최대)  PER(최소)  12M PER
        날짜
        2022/11   3063374.5     3288390     2826800     336985          419430         265250  3935.14    4842.57    3249.68  15.81      19.14      12.84     15.3
        2022/12  2942704.08     3173270     2635050     291990          389990         196600  3463.21    4294.48    2662.58  15.97      20.77      12.88    15.97
        2023/01  2820243.82     3073260     2635050  211293.59          342396         128930  2583.89    4140.17    1589.21  23.61      38.38      14.73    22.15
        2023/02  2728378.14     3073260     2581450  168233.05          329278          97490  2269.22    3734.23    1346.16  26.71      45.02      16.23    22.45
        2023/03   2723824.5     2900830     2594060  114761.09          184940          42540  1735.61    3137.21     758.32  36.87       84.4       20.4    25.65
        2023/04  2688688.59     2884560     2560260     100754          184940          46570  1624.44    3351.85     932.77  40.32      70.22      19.54    25.21
        2023/05  2678715.91     2884560     2540150   95985.36          122270          59390  1556.63    3351.85    1068.80  45.87       66.8       21.3    24.93
        2023/06  2660441.74     2785651     2476590   95079.48          122270          59390  1548.96    3477.57    1068.80  46.61      67.55      20.76    23.27
        2023/07  2604180.14     2708860     2527000   85640.81          126210          61590  1593.81    3442.83     963.24  43.79      72.46      20.27    19.75
        2023/08  2609199.41     2708860     2527000   85829.45          126210          46620  1510.10    3442.83     963.24   44.3      69.45      19.43       18
        2023/09   2613926.3     2708860     2527000   71636.43          100390          41620  1358.22    3442.83     832.63  50.36      82.15      19.87    18.16
        2023/10  2609787.67     2661845     2528300   72144.57           96690          57010  1264.41    1722.45     908.63  54.41      75.72      39.94    19.22
        """
        return self._consensusSeries('2')

    @property
    def benchmarkMultiples(self) -> pd.DataFrame:
        """
        벤치마크 베수 비교
        :return: 
        """
        url = f"http://cdn.fnguide.com/SVO2/json/chart/01_04/chart_A{self._t}_{self.__gb__}.json"
        data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        objs = dict()
        for label, index in (('PER', '02'), ('EV/EBITDA', '03'), ('ROE', '04'), ('배당수익률', '05')):
            header1 = pd.DataFrame(data[f'{index}_H'])[['ID', 'NAME']].set_index(keys='ID')
            header1['NAME'] = header1['NAME'].astype(str).str.replace("'", "20")
            header1 = header1.to_dict()['NAME']
            header1.update({'CD_NM': '이름'})

            inner1 = pd.DataFrame(data[index])[list(header1.keys())].rename(columns=header1).set_index(keys='이름')
            inner1.index.name = None
            for col in inner1.columns:
                inner1[col] = inner1[col].apply(lambda x: np.nan if x == '-' else x)
            objs[label] = inner1.T
        return pd.concat(objs=objs, axis=1).astype(float)

    @property
    def perBand(self) -> pd.DataFrame:
        """
        PER 밴드
        :return:
                   수정주가    12.85X     19.44X     26.04X     32.63X     39.22X
        날짜
        2018-12-01  47050.0  41007.43   62045.68   83083.93  104122.18  125160.43
        2019-01-01  50000.0  41298.85   62486.61   83674.36  104862.12  126049.88
        2019-02-01  52800.0  41590.27   62927.53   84264.79  105602.06  126939.32
        ...             ...       ...        ...        ...        ...        ...
        2025-10-01      NaN  96413.81  145877.47  195341.13  244804.79  294268.44
        2025-11-01      NaN  96413.81  145877.47  195341.13  244804.79  294268.44
        2025-12-01      NaN  96413.81  145877.47  195341.13  244804.79  294268.44
        """
        return self._multipleBand('CHART_E')

    @property
    def pbrBand(self) -> pd.DataFrame:
        """
        PBR 밴드
        :return:
                   수정주가     2.24X      3.61X      4.98X      6.34X      7.71X
        날짜
        2018-12-01  47050.0  39169.38   63081.94   86994.49  110907.05  134819.60
        2019-01-01  50000.0  39610.24   63791.93   87973.63  112155.33  136337.02
        2019-02-01  52800.0  40051.10   64501.93   88952.77  113403.60  137854.44
        ...             ...       ...        ...        ...        ...        ...
        2025-10-01      NaN  72823.52  117281.63  161739.74  206197.85  250655.96
        2025-11-01      NaN  72823.52  117281.63  161739.74  206197.85  250655.96
        2025-12-01      NaN  72823.52  117281.63  161739.74  206197.85  250655.96
        """
        return self._multipleBand('CHART_B')

    @property
    def shortRatio(self) -> pd.DataFrame:
        """
        차입공매도 비중
        :return:
                    공매도비중      종가
        날짜
        2022-10-17       10.81  139900.0
        2022-10-24        7.94  140000.0
        2022-10-31        2.42  136800.0
        ...                ...
        2023-10-02       11.54  153800.0
        2023-10-09       14.76  154700.0
        2023-10-16       18.95  156800.0
        """
        url = f"http://cdn.fnguide.com/SVO2/json/chart/11_01/chart_A{self._t}_SELL1Y.json"
        data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        data = pd.DataFrame(data['CHART']).rename(
            columns={'TRD_DT': '날짜', 'VAL': '공매도비중', 'ADJ_PRC': '종가'}
        ).set_index(keys='날짜')
        data.index = pd.to_datetime(data.index)
        return data.astype(float)

    @property
    def shortBalance(self) -> pd.DataFrame:
        """
        대차잔고 비중
        :return:
                   대차잔고비중   종가
        날짜
        2022-10-17        3.50  139900
        2022-10-24        3.50  140000
        2022-10-31        3.44  136800
        ...                ...     ...
        2023-10-02        9.45  153800
        2023-10-09        9.52  154700
        2023-10-16        8.69  156800
        """
        url = f"http://cdn.fnguide.com/SVO2/json/chart/11_01/chart_A{self._t}_BALANCE1Y.json"
        columns = {'TRD_DT': '날짜', 'BALANCE_RT': '대차잔고비중', 'ADJ_PRC': '종가'}
        data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        data = pd.DataFrame(data['CHART']).rename(columns=columns)[columns.values()].set_index(keys='날짜')
        data.index = pd.to_datetime(data.index)
        return data.astype(float)

    @property
    def etfComponent(self) -> pd.DataFrame:
        """
        ETF 구성 비중
        :return:
                            이름        비중
        티커
        005930          삼성전자  26.469999
        006400           삼성SDI  18.270000
        207940  삼성바이오로직스  10.450000
        028260          삼성물산   8.730000
        000810          삼성화재   6.720000
        009150          삼성전기   6.400000
        032830          삼성생명   5.080000
        010140        삼성중공업   3.960000
        018260    삼성에스디에스   3.640000
        028050    삼성엔지니어링   3.490000
        016360          삼성증권   1.830000
        008770          호텔신라   1.760000
        012750            에스원   1.150000
        030000          제일기획   1.130000
        029780          삼성카드   0.600000
        """
        data = get_etf_portfolio_deposit_file(self._t)
        data['이름'] = MetaData[MetaData.index.isin(data.index)]['korName']
        return data[['이름', '비중']]

    @property
    def etfSectors(self) -> pd.DataFrame:
        """
        ETF 섹터 비중
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
        n, base = 100, ""
        src = requests.get(url=self.__url__('ETF_Snapshot')).text.split('\r\n')
        while n < len(src):
            if 'etf1StockInfoData' in src[n]:
                while not "];" in src[n + 1]:
                    base += src[n + 1]
                    n += 1
                break
            n += 1
        data = pd.DataFrame(data=eval(base)).drop(columns=['val05'])
        data.columns = np.array(["섹터", MetaData.loc[self._t, 'name'], "유사펀드", "시장"])
        return data.set_index(keys='섹터')


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)
    # ticker = '005930'
    # ticker = '000660' # SK하이닉스
    # ticker = '003800' # 에이스침대
    # ticker = '058470' # 리노공업
    # ticker = '102780' # KODEX 삼성그룹
    # ticker = "253450" # 스튜디오드래곤
    ticker = "316140" # 우리금융지주


    # guide = fnguide(ticker)

    # EQUITY
    # print(guide.previousClose)
    # print(guide.previousForeignRate)
    # print(guide.beta)
    # print(guide.volume)
    # print(guide.marketCap)
    # print(guide.fiftyTwoWeekLow)
    # print(guide.fiftyTwoWeekHigh)
    # print(guide.dividendYield)
    # print(guide.forwardPE)
    # print(guide.fiscalPE)
    # print(guide.fiscalEps)
    # print(guide.priceToBook)
    # print(guide.businessSummary)
    # print(guide.annualOverview)
    # print(guide.annualProducts)
    # print(guide.annualExpenses)
    # print(guide.annualSalesShares)
    # print(guide.annualHolders)
    # print(guide.annualProfit)
    # print(guide.annualInventory)
    # print(guide.annualCashFlow)
    # print(guide.annualGrowthRate)
    # print(guide.annualProfitRate)
    # print(guide.annualMultiples)
    # print(guide.quarterOverview)
    # print(guide.quarterProfitLoss)
    # print(guide.quarterAsset)
    # print(guide.quarterCashFlow)
    # print(guide.quarterGrowthRate)
    # print(guide.quarterProfitRate)
    # print(guide.foreignRate)
    # print(guide.consensus)
    # print(guide.consensusAnnualProfit)
    # print(guide.consensusQuarterProfit)
    # print(guide.consensusThisYear)
    # print(guide.consensusNextYear)
    # print(guide.benchmarkMultiples)
    # print(guide.perBand)
    # print(guide.pbrBand)
    # print(guide.shortRatio)
    # print(guide.shortBalance)
    # print(guide.targetPrice)

    # ETF
    # print(guide.previousClose)
    # print(guide.foreignHold)
    # print(guide.beta)
    # print(guide.volume)
    # print(guide.marketCap)
    # print(guide.fiftyTwoWeekLow)
    # print(guide.fiftyTwoWeekHigh)
    # print(guide.etfSectors)
    # print(guide.etfComponent)
