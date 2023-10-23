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


class fnguide(object):

    def __init__(self, ticker:str):
        self._t = ticker
        self._u = f"http://comp.fnguide.com/SVO2/ASP/%s.asp?" \
                  f"pGB=1&" \
                  f"gicode=A{ticker}&" \
                  f"cID=&" \
                  f"MenuYn=Y&" \
                  f"ReportGB=%s&" \
                  f"NewMenuID=%s&" \
                  f"stkGb=%s"

        xml = etree.fromstring(
            requests.get(
                url=f"http://cdn.fnguide.com/SVO2/xml/Snapshot_all/{ticker}.xml"
            ).text[39:]
        ).find('price')

        str2num = lambda x: int(x.replace(', ', '').replace(',', ''))
        self.previousClose = str2num(xml.find('close_val').text)
        self.foreignHold = float(xml.find('frgn_rate').text)
        self.beta = float(xml.find('beta').text) if xml.find('beta').text else np.nan
        self.volume = str2num(xml.find('deal_cnt').text)
        self.marketCap = str2num(xml.find('mkt_cap_1').text) # 억원
        self.fiftyTwoWeekLow = str2num(xml.find('low52week').text)
        self.fiftyTwoWeekHigh = str2num(xml.find('high52week').text)
        return

    def __url__(self, page:str, hold:str='') -> str:
        """
        :param page : [str]
        :param hold : [str] 연결 - "D" 또는 "" / 별도 - "B"
        :return:
        """
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
        if not page in pages or not hold in ['', 'D', 'B']:
            raise KeyError
        return self._u % (page, pages[page]["ReportGB"], pages[page]["NewMenuID"], pages[page]["stkGb"])

    def __html__(self, page:str, hold:str='') -> list:
        if not hasattr(self, f"_u{page}{hold}"):
            self.__setattr__(f'_u{page}{hold}', pd.read_html(self.__url__(page, hold), header=0))
        return self.__getattribute__(f'_u{page}{hold}')

    def __hold__(self) -> str:
        if not hasattr(self, f"_hold"):
            html = self.__html__('SVD_Main')
            if html[11].iloc[1].isnull().sum() > html[14].iloc[1].isnull().sum():
                self.__setattr__('_hold', 'B') # 별도
            else:
                self.__setattr__('_hold', 'D') # 연결
        return self.__getattribute__('_hold')

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

        cap = self.cap.copy()
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
        header.update({'GS_YM': '날짜'})
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
        url = f"https://cdn.fnguide.com/SVO2/json/chart/07_01/chart_A{self._t}_{self.__hold__()}_{period}.json"
        raw = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        basis = pd.DataFrame(raw['CHART']).replace('-', np.nan)[columns.keys()]
        basis = basis.rename(columns=columns)
        return basis.set_index(keys="기말")

    def _consensusSeries(self, year:str) -> pd.DataFrame:
        columns = {
            "STD_DT": "날짜",
            "SALES": "매출", "SALES_MAX": "매출(최대)", "SALES_MIN": "매출(최소)",
            "OP": "영업이익", "OP_MAX": "영업이익(최대)", "OP_MIN": "영업이익(최소)",
            "EPS": "EPS", "EPS_MAX": "EPS(최대)", "EPS_MIN": "EPS(최소)",
            "PER": "PER", "PER_MAX": "PER(최대)", "PER_MIN": "PER(최소)", "PER_12F": "12M PER"
        }
        url = f"https://cdn.fnguide.com/SVO2/json/chart/07_02/chart_A{self._t}_{self.__hold__()}_FY{year}.json"
        raw = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
        basis = pd.DataFrame(raw['CHART'])[columns.keys()]
        basis = basis.rename(columns=columns)
        basis = basis.set_index(keys='날짜')
        return basis

    @staticmethod
    def _finance(data:pd.DataFrame) -> pd.DataFrame:
        data = data.set_index(keys=[data.columns[0]])
        data = data.drop(columns=[col for col in data if not col.startswith('20')])
        data.index.name = None
        data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/최근"]
        data.index = [
            i.replace('계산에 참여한 계정 펼치기', '').replace('(', '').replace(')', '').replace('*', '') for i in data.index
        ]
        return data.T.astype(float)

    @property
    def cap(self) -> pd.DataFrame:
        if not hasattr(self, '__cap'):
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
            self.__setattr__('__cap', cap[['시가총액']])
        return self.__getattribute__('__cap')

    @property
    def summary(self) -> str:
        html = Soup(requests.get(self.__url__('SVD_Main')).content, 'lxml').find('ul', id='bizSummaryContent').find_all('li')
        t = '\n\n '.join([e.text for e in html])
        w = [
            '.\n' if t[n] == '.' and not any([t[n - 1].isdigit(), t[n + 1].isdigit(), t[n + 1].isalpha()]) else t[n]
            for n in range(1, len(t) - 2)
        ]
        s = ' ' + t[0] + ''.join(w) + t[-2] + t[-1]
        return s.replace(' ', '').replace('\xa0\xa0', ' ').replace('\xa0', ' ').replace('\n ', '\n')

    @property
    def annualOverview(self) -> pd.DataFrame:
        return self._overview(self.__html__('SVD_Main')[11] if self.__hold__() == 'D' else self.__html__('SVD_Main')[14])

    @property
    def annualProducts(self) -> pd.DataFrame:
        url = f"http://cdn.fnguide.com/SVO2//json/chart/02/chart_A{ticker}_01_N.json"
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
        html = self.__html__('SVD_Corp')
        data = pd.concat(
            objs=[
                html[4 if self.__hold__() == 'D' else 6].set_index(keys=['항목']).T,  # 매출원가율
                html[5 if self.__hold__() == 'D' else 7].set_index(keys=['항목']).T,  # 판관비
            ], axis=1
        )
        data.columns.name = None
        data.index.name = '기말'
        return data

    @property
    def annualSalesShares(self) -> pd.DataFrame:
        data = self.__html__('SVD_Corp')[10 if self.__hold__() == 'D' else 11]
        data = data[data.index.isin([0, len(data) - 1])]
        data = data[[col for col in data if col.startswith('20')]]
        values = []
        for n in range(int(len(data.columns) / 2)):
            value = data.iloc[-1][n * 2 : (n * 2) + 2]
            value.name = value.index[0].replace('.', '/')
            value.index = data.iloc[0][n * 2 : (n * 2) + 2]
            values.append(value)
        data = pd.concat(values, axis=1)
        data.index.name = None
        return data.T.fillna(0.0).astype(float)

    @property
    def annualHolders(self) -> pd.DataFrame:
        data = self.__html__('SVD_Corp')[12]
        data = data.set_index(keys=[data.columns[0]])
        data.index.name = None
        return data.T

    @property
    def annualProfitLoss(self) -> pd.DataFrame:
        return self._finance(self.__html__('SVD_Finance', self.__hold__())[0])

    @property
    def annualAsset(self) -> pd.DataFrame:
        return self._finance(self.__html__('SVD_Finance', self.__hold__())[2])

    @property
    def annualCashFlow(self) -> pd.DataFrame:
        return self._finance(self.__html__('SVD_Finance', self.__hold__())[4])

    @property
    def annualGrowthRate(self) -> pd.DataFrame:
        data = self.__html__('SVD_FinanceRatio', self.__hold__())[0]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('성장성비율') + 1 : index.index('수익성비율')])
    
    @property
    def annualProfitRate(self) -> pd.DataFrame:
        data = self.__html__('SVD_FinanceRatio', self.__hold__())[0]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('수익성비율') + 1: index.index('활동성비율')])

    @property
    def annualMultiples(self) -> pd.DataFrame:
        data = self.__html__('SVD_Invest', self.__hold__())[3]
        data = data[~data[data.columns[0]].isin(["Per\xa0Share", "Dividends", "Multiples", "FCF"])]
        return self._finance(data)

    @property
    def quarterOverview(self) -> pd.DataFrame:
        return self._overview(self.__html__('SVD_Main')[12] if self.__hold__() == 'D' else self.__html__('SVD_Main')[15])

    @property
    def quarterProfitLoss(self) -> pd.DataFrame:
        return self._finance(self.__html__('SVD_Finance', self.__hold__())[1])

    @property
    def quarterAsset(self) -> pd.DataFrame:
        return self._finance(self.__html__('SVD_Finance', self.__hold__())[3])

    @property
    def quarterCashFlow(self) -> pd.DataFrame:
        return self._finance(self.__html__('SVD_Finance', self.__hold__())[5])

    @property
    def quarterGrowthRate(self) -> pd.DataFrame:
        data = self.__html__('SVD_FinanceRatio', self.__hold__())[1]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('성장성비율') + 1: index.index('수익성비율')])

    @property
    def quarterProfitRate(self) -> pd.DataFrame:
        data = self.__html__('SVD_FinanceRatio', self.__hold__())[1]
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
        basis['컨센서스'] = basis['컨센서스'].apply(lambda x: int(x) if x else np.nan)
        basis['격차'] = round(100 * (basis['종가'].astype(int) / basis['컨센서스'] - 1), 2)
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
    ticker = '005930'
    # ticker = '000660' # SK하이닉스
    # ticker = '003800' # 에이스침대
    # ticker = '058470' # 리노공업
    # ticker = '102780' # KODEX 삼성그룹

    guide = fnguide(ticker)

    # EQUITY
    # print(guide.previousClose)
    # print(guide.foreignHold)
    # print(guide.beta)
    # print(guide.volume)
    # print(guide.marketCap)
    # print(guide.fiftyTwoWeekLow)
    # print(guide.fiftyTwoWeekHigh)
    # print(guide.summary)
    # print(guide.annualOverview)
    # print(guide.annualProducts)
    # print(guide.annualExpenses)
    # print(guide.annualSalesShares)
    # print(guide.annualHolders)
    # print(guide.annualProfitLoss)
    # print(guide.annualAsset)
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
    print(guide.consensusThisYear)
    print(guide.consensusNextYear)
    # print(guide.perBand)
    # print(guide.pbrBand)
    # print(guide.shortRatio)
    # print(guide.shortBalance)

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
