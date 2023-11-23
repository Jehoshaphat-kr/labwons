from urllib.request import urlopen
import pandas as pd
import numpy as np
import json

class fnguide(object):


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
