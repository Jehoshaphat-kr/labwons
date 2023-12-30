from nohji.asset.core.datatype import multiframes
from nohji.asset.core.decorator import etfonly, stockonly, common
from nohji.meta import meta
from nohji.util.brush import cutString, str2num
from nohji.util.web import web

from numpy import nan
from pandas import concat, DataFrame, Series, to_datetime
from typing import Union


class _url:
    """
    Set of urls for fnguide pages
    """

    class _cdn:
        __slots__ = (
            "multipleBands",
            "products",
            "expenses",
            "profitConsensusAnnual",
            "profitConsensusQuarter",
            "priceConsensus",
            "abstractConsensusRelevant",
            "abstractConsensusForward",
            "foreignRate3Months",
            "foreignRate1Year",
            "foreignRate3Years",
            "benchmarkMultiples",
            "shares",
            "shortSell",
            "shortBalance"
        )
        def __init__(self, ticker: str, gb: str):
            base = "http://cdn.fnguide.com/SVO2"
            self.products = f"{base}/json/chart/02/chart_A{ticker}_01_N.json"
            self.multipleBands = f"{base}/json/chart/01_06/chart_A{ticker}_D.json"
            self.expenses = f"{base}/json/chart/02/chart_A{ticker}_D.json"
            self.profitConsensusAnnual = f"{base}/json/chart/07_01/chart_A{ticker}_{gb}_A.json"
            self.profitConsensusQuarter = f"{base}/json/chart/07_01/chart_A{ticker}_{gb}_Q.json"
            self.priceConsensus = f"{base}/json/chart/01_02/chart_A{ticker}.json"
            self.abstractConsensusRelevant = f"{base}/json/chart/07_02/chart_A{ticker}_{gb}_FY1.json"
            self.abstractConsensusForward = f"{base}/json/chart/07_02/chart_A{ticker}_{gb}_FY2.json"
            self.foreignRate3Months = f"{base}/json/chart/01_01/chart_A{ticker}_3M.json"
            self.foreignRate1Year = f"{base}/json/chart/01_01/chart_A{ticker}_1Y.json"
            self.foreignRate3Years = f"{base}/json/chart/01_01/chart_A{ticker}_3Y.json"
            self.benchmarkMultiples = f"{base}/json/chart/01_04/chart_A{ticker}_{gb}.json"
            self.shares = f"{base}/json/chart/08_01/chart_A{ticker}.json"
            self.shortSell = f"{base}/json/chart/11_01/chart_A{ticker}_SELL1Y.json"
            self.shortBalance = f"{base}/json/chart/11_01/chart_A{ticker}_BALANCE1Y.json"
            return

    def __init__(self, ticker:str):
        self.ticker = ticker
        self.xml = f"http://cdn.fnguide.com/SVO2/xml/Snapshot_all/{ticker}.xml"
        return

    def __html__(self, assetType:str, page:str, ReportGB:str, stkGb:str) -> str:
        return f"http://comp.fnguide.com/SVO2/ASP/{assetType}_{page}.asp?" \
               f"pGB=1&" \
               f"gicode=A{self.ticker}&" \
               f"cID=&" \
               f"MenuYn=Y" \
               f"&ReportGB={ReportGB}" \
               f"&NewMenuID=" \
               f"&stkGb={stkGb}"

    @stockonly
    def gb(self) -> str:
        tbs = web.list(self.snapshot)
        return "B" if tbs[11].iloc[1].isnull().sum() > tbs[14].iloc[1].isnull().sum() else "D"

    @stockonly
    def cdn(self):
        return self._cdn(self.ticker, self.gb)

    @stockonly
    def snapshot(self) -> str:
        return self.__html__("SVD", "Main", "", "701")

    @stockonly
    def corp(self) -> str:
        return self.__html__("SVD", "Corp", self.gb, "701")

    @stockonly
    def finance(self) -> str:
        return self.__html__("SVD", "Finance", self.gb, "701")

    @stockonly
    def financeB(self) -> str:
        return self.__html__("SVD", "Finance", 'A', "701")

    @stockonly
    def ratio(self) -> str:
        return self.__html__("SVD", "FinanceRatio", self.gb, "701")

    @stockonly
    def invest(self) -> str:
        return self.__html__("SVD", "Invest", "", "701")

    @etfonly
    def etf(self) -> str:
        return self.__html__("etf", "snapshot", "", "770")



class fnguide:
    """
    Fetch source data from fnguide

    @abstract
        constraint  : stockonly
        type        : DataFrame (multi frames included)
        description : abstracted dataframe of financial statement, ratio and others.
        columns     : ['이자수익', '영업이익', '영업이익(발표기준)', '당기순이익',
                       '지배주주순이익', '비지배주주순이익',
                       '자산총계', '부채총계', '자본총계', '지배주주지분', '비지배주주지분',
                       '자본금', '부채비율', '유보율', '영업이익률',
                       '지배주주순이익률', 'ROA', 'ROE', 'EPS(원)', 'BPS(원)', 'DPS(원)', 'PER', 'PBR',
                       '발행주식수', '배당수익률']
        example     :
                      이자수익 영업이익 당기순이익 ...   PER   PBR 발행주식수 배당수익률
            기말
            2018/12        NaN     NaN        NaN  ...   NaN   NaN       NaN        NaN
            2019/12     105768   28000      20376  ...  4.29  0.39    722268       6.03
            2020/12      95239   20804      15152  ...  5.38  0.30    722268       3.70
            2021/12      98947   36597      28074  ...  3.56  0.36    728061       7.09
            2022/12     146545   44305      33240  ...  2.68  0.29    728061       9.78
            2023/12(E)  198704   40045      30132  ...  3.25  0.30       NaN        NaN

    @benchmarkMultiples
        constraint  : stockonly
        type        : DataFrame (Multi-Indexed)
        description : compared data of multiples: ["PER", "EV/EBITDA", "ROE", "배당수익률"]
                      also, by index.
        columns     : MultiIndex([(       'PER',  '우리금융지주'),
                                  (       'PER', '코스피 금융업'),
                                  (       'PER',     '코스피'),
                                  ( 'EV/EBITDA',  '우리금융지주'),
                                  ( 'EV/EBITDA', '코스피 금융업'),
                                  ( 'EV/EBITDA',     '코스피'),
                                  (       'ROE',  '우리금융지주'),
                                  (       'ROE', '코스피 금융업'),
                                  (       'ROE',     '코스피'),
                                  ('배당수익률',  '우리금융지주'),
                                  ('배당수익률', '코스피 금융업'),
                                  ('배당수익률',     '코스피')
                                ])
        example     :
                                                  PER  ...                           배당수익률
                  우리금융지주  코스피 금융업  코스피  ...  우리금융지주  코스피 금융업  코스피
            2021          3.56           5.94   11.08  ...          7.09           3.48    1.78
            2022          2.68           5.53   10.87  ...          9.78           4.32    2.22
            2023E         3.25           6.08   17.54  ...           NaN            NaN     NaN

    @businessSummary
        constraint  : stockonly
        type        : str
        description : business summary of the corp.
        example     :
            한국 및 DX부문 해외 9개 지역총괄과 DS부문 해외 5개 지역총괄, SDC, Harman 등 233개의
            종속기업으로 구성된 글로벌 전자기업임. 세트사업은 TV를 비롯 모니터, 냉장고, 세탁기,
            에어컨, 스마트폰, 네트워크시스템, 컴퓨터 등을 생산하는 DX부문이 있음.
            부품 사업에는 DRAM, NAND Flash, 모바일AP 등의 제품을 생산하고 있는 DS 부문과 중소형OLED
            등의 디스플레이 패널을 생산하고 있는 SDC가 있음.

            3분기에는 스마트폰 플래그십 신제품 출시와 디스플레이 프리미엄 제품 판매 확대로 견조한 실적을
            거둔 디스플레이와 MX(모바일경험)가 반도체 부문의 영업손실을 상쇄함. 메모리 반도체의 영업적자는
            직전분기 대비 판매단가가 상승하며 축소됐으나, 시스템 LSI 및 파운드리의 영업적자는 부진한
            레거시 파운드리 가동률로 소폭 확대됨. 4분기는 메모리 부문 적자 축소와 디스플레이의 북미
            고객사 신제품 효과가 지속되며 실적 개선이 예상됨.

    @cashFlow
        constraint  : stockonly
        type        : DataFrame
        description : cash flow of the corp.
        example     :
                     영업현금흐름  투자현금흐름  재무현금흐름  환율변동손익  현금및현금성자산
            2020/12        123146       -118404          2521          -563             29760
            2021/12        197976       -223923         44923          1843             50580
            2022/12        147805       -178837         28218          2005             49770
            2023/2Q         -6940        -53509         70579           508             60408

    @consensusOutstanding
        constraint  : stockonly
        type        : Series
        description : abbreviated consensus
        example     :
            투자의견         4.0
            목표주가     15411.0
            EPS           3908.0
            PER              3.3
            추정기관수      18.0
            dtype: float64

    @consensusPrice
        constraint  : stockonly
        type        : DataFrame
        description : average price consensus of trailing 1 year,
                      given if and only if more than 3 consensus data is gathered.
        example     :
                       투자의견  컨센서스     종가   격차
            날짜
            2022-11-23      4.0   16378.0  12300.0 -24.90
            2022-11-24      4.0   16378.0  12550.0 -23.37
            2022-11-25      4.0   16378.0  12450.0 -23.98
            ...             ...       ...      ...    ...
            2023-11-20      4.0   15411.0  12490.0 -18.95
            2023-11-21      4.0   15411.0  12720.0 -17.46
            2023-11-22      4.0   15411.0  12700.0 -17.59

    @consensusProfit
        constraint  : stockonly
        type        : DataFrame (multi frames included)
        description : yearly or quarterly profit consensus
        example     :
            [Yearly: <attribute; Y>]
                    매출실적  매출전망  영업이익실적  영업이익전망
            기말
            2020/12  2013.35   2032.00        778.82        784.67
            2021/12  2801.67   2773.23       1171.04       1144.04
            2022/12  3224.23   3340.00       1366.35       1460.00
            2023/12      NaN   2578.67           NaN       1055.50
            2024/12      NaN   3048.83           NaN       1278.83
            2025/12      NaN   3469.00           NaN       1465.50

            [Quarterly: <attribute; Q>]
                    매출실적  매출전망  영업이익실적  영업이익전망
            기말
            2023/03   490.91    732.25        172.63         277.5
            2023/06   751.31    696.25        335.62         266.0
            2023/09   733.99    770.25        333.24         332.0
            2023/12      NaN    601.60           NaN         213.0
            2024/03      NaN    582.50           NaN         219.5
            2024/06      NaN    817.00           NaN         366.5

    @consensusThisFiscalYear, consensusNextFiscalYear
        constraint  : stockonly
        type        : DataFrame
        description : abstracted consensus data
        columns     : ['매출', '매출(최대)', '매출(최소)', '영업이익', '영업이익(최대)', '영업이익(최소)', 'EPS',
                       'EPS(최대)', 'EPS(최소)', 'PER', 'PER(최대)', 'PER(최소)', '12M PER']
        example     :
                           매출  매출(최대)  매출(최소)   영업이익  영업이익(최대) 영업이익(최소)  ...  12M PER
            날짜
            2022/11   3063374.5     3288390     2826800     336985          419430         265250  ...     15.3
            2022/12  2942704.08     3173270     2635050     291990          389990         196600  ...    15.97
            2023/01  2820243.82     3073260     2635050  211293.59          342396         128930  ...    22.15
            2023/02  2728378.14     3073260     2581450  168233.05          329278          97490  ...    22.45
            2023/03   2723824.5     2900830     2594060  114761.09          184940          42540  ..     25.65
            2023/04  2688688.59     2884560     2560260     100754          184940          46570  ...    25.21
            2023/05  2678715.91     2884560     2540150   95985.36          122270          59390  ...    24.93
            2023/06  2660441.74     2785651     2476590   95079.48          122270          59390  ...    23.27
            2023/07  2604180.14     2708860     2527000   85640.81          126210          61590  ...    19.75
            2023/08  2609199.41     2708860     2527000   85829.45          126210          46620  ...       18
            2023/09   2613926.3     2708860     2527000   71636.43          100390          41620  ...    18.16
            2023/10  2609787.67     2661845     2528300   72144.57           96690          57010  ...    19.22

    @expenses
        constraint  : stockonly
        type        : DataFrame (multi frames included)
        description : expenses ratio
        example     :
                     판관비율  매출원가율
            기말
            2019/12     16.58       20.62
            2020/12     13.81       12.31
            2021/12     15.25       10.70
            2022/12     10.69       14.06

    @financialStatement
        constraint  : stockonly
        type        : DataFrame (multi frames included)
        description : financial statement of the prior (auto detected by linked or separated)
        columns     : ['자산', '유동자산', '비유동자산', '기타금융업자산',
                       '부채', '유동부채', '비유동부채', '기타금융업부채',
                       '자본', '자본금', '신종자본증권', '자본잉여금', '기타자본',
                       '기타포괄손익누계액', '이익잉여금결손금']
        example     :
                     자산  유동자산  비유동자산  기타금융업자산  부채  유동부채  비유동부채  ...  이익잉여금결손금
            2020/12  3615      2577        1038             NaN   242       219          23  ...              3265
            2021/12  4664      3357        1306             NaN   487       460          27  ...              4068
            2022/12  5315      3770        1545             NaN   383       364          19  ...              4823
            2023/3Q  5773      4194        1579             NaN   460       438          22  ...              5205

    @financialSeparatedStatement
        constraint  : stockonly
        type        : DataFrame (multi frames included)
        description : financial statement of the separated statement
        columns     : ['유동자산', '현금및단기예금', '유가증권', '매출채권', '재고자산', '임대주택자산', '비유동자산',
                       '투자자산', '유형자산', '감가상각자산', '무형자산', '자산총계', '유동부채', '매입채무',
                       '단기차입금', '유동성장기부채', '비유동부채', '사채', '장기차입금', '이연부채', '부채총계',
                       '자본금', '자본잉여금', '자본조정', '자기주식', '기타포괄손익누계액', '이익잉여금', '자본총계',
                       '순운전자본', '순차입금', '투하자본']
        example     :
                     유동자산  현금및단기예금  유가증권  매출채권  재고자산  임대주택자산  비유동자산  ...  투하자본
            2020/12      2577            2066       NaN       291       123           NaN        1038  ...      1235
            2021/12      3357    	     2830       NaN       354       116           NaN        1306  ...      1340
            2022/12      3770            3171       NaN       393       131           NaN        1545  ...      1740
            2023/3Q      4194            3545       NaN       433       143           NaN        1579  ...      1719

    @foreignExhaustRate
        constraint  : stockonly
        type        : DataFrame (Multi-Indexed)
        description : time-series of foreign hold(exhuast) rate
        columns     : MultiIndex([('3M', '종가'),
                                  ('3M', '비중'),
                                  ('1Y', '종가'),
                                  ('1Y', '비중'),
                                  ('3Y', '종가'),
                                  ('3Y', '비중')
                                ])
        example     :
                                    3M              1Y              3Y
                           종가   비중     종가   비중     종가   비중
            날짜
            2020-11-01      NaN    NaN      NaN    NaN  10105.0  25.67
            2020-12-01      NaN    NaN      NaN    NaN  10033.0  25.21
            2021-01-01      NaN    NaN      NaN    NaN   9629.0  25.05
            ...             ...    ...      ...    ...      ...    ...
            2023-11-20  12490.0  37.18      NaN    NaN      NaN    NaN
            2023-11-21  12720.0  37.34      NaN    NaN      NaN    NaN
            2023-11-22  12700.0  37.36  12604.0  37.25      NaN    NaN

    @growthRate
        constraint  : stockonly
        type        : DataFrame (multi frames included)
        description : growth rate (YoY)
        example     :
            [Y]
                     매출액증가율  판매비와관리비증가율  영업이익증가율  EBITDA증가율  EPS증가율
            2019/12          13.3                  -4.2            11.5           9.8        8.5
            2020/12          18.2                   8.8            21.4          21.4        4.9
            2021/12          39.2                  29.7            50.4          47.0       87.5
            2022/12          15.1                  27.3            16.7          16.4       10.2
            2023/3Q         -27.0                 -24.8           -30.4         -28.0      -21.4

            [Q]
                     매출액증가율  영업이익증가율  EBITDA증가율  EPS증가율
            2022/09           3.8           -31.4         -16.0      -24.2
            2022/12          -8.0           -69.0         -40.5      120.8
            2023/03         -18.1           -95.5         -57.2      -87.4
            2023/06         -22.3           -95.3         -57.3      -85.9
            2023/3Q         -12.2           -77.6         -41.4      -39.8

    @incomeStatement
        constraint  : stockonly
        type        : DataFrame (multi frames included)
        description : income statement
        columns     : ['매출액', '매출원가', '매출총이익', '판매비와관리비', '영업이익', '영업이익발표기준',
                       '금융수익', '금융원가', '기타수익', '기타비용', '종속기업,공동지배기업및관계기업관련손익',
                       '세전계속사업이익', '법인세비용', '계속영업이익', '중단영업이익', '당기순이익',
                       '지배주주순이익', '비지배주주순이익']
        example     :
                     매출액 매출원가 매출총이익 판매비와관리비 영업이익 금융수익 금융원가 기타수익 기타비용 ... 당기순이익
            2020/12  319004   210898     108106          57980    50126    33279    19804      848     1716 ...      47589
            2021/12  429978   240456     189522   		 65419   124103    23775    14699     1161     1804 ...      96162
            2022/12  446216   289937     156279  		 88184    68094    37143    50916     2414    18019 ...      22417
            2023/2Q  123940   152172     -28231  		 34613   -62844    15203    25144      261      739 ...     -55734

    @marketShares
        constraint  : stockonly
        type        : DataFrame
        description : market shares of the products, mostly not provided
        example     :
                    IC TEST SOCKET 류   LEENO PIN 류          상품     상품 등  의료기기 부품류          합계
                        내수     수출    내수   수출    내수  수출  내수  수출       내수  수출   내수   수출
            2020/12      NaN      NaN    NaN    NaN     NaN   NaN    NaN   NaN       NaN    NaN    NaN    NaN
            2021/12      NaN      NaN    NaN    NaN     NaN   NaN    NaN   NaN       NaN    NaN    NaN    NaN
            2022/12    10.50    89.50  27.80  72.20  100.00  0.00  95.80  4.20     99.30   0.70  24.30  75.70

    @multipleBands
        constraint  : stockonly
        type        : DataFrame
        description : multiple band provided by fnguide
        example     :
                                                PER  ...                           PBR
                           종가     2.46X     3.42X  ...     0.38X     0.46X     0.54X
            날짜                                     ...
            2018-12-01      NaN       NaN       NaN  ...       NaN       NaN       NaN
            2019-01-01      NaN       NaN       NaN  ...       NaN       NaN       NaN
            2019-02-01  14800.0       NaN       NaN  ...       NaN       NaN       NaN
            ...             ...       ...       ...  ...       ...       ...       ...
            2025-10-01      NaN  10455.54  14535.75  ...  17745.94  21650.05  25554.16
            2025-11-01      NaN  10488.84  14582.04  ...  17844.72  21770.56  25696.39
            2025-12-01      NaN  10522.13  14628.33  ...  17943.50  21891.06  25838.63

    @multiplesOutstanding
        constraint  : common
        type        : Series
        description : multiples outstanding
        example     :
            [stock]
            fiscalPE         2.90
            forwardPE        3.06
            sectorPE         6.17
            priceToBook      0.32
            dividendYield    9.03
            dtype: float64

            [ETF]
            dividendYield     1.68
            fiscalPE         12.58
            priceToBook       1.15
            dtype: float64

    @products
        constraint  : stockonly
        type        : DataFrame
        description : products of the corp
        example     :
                    유가증권평가및처분이익  이자수익  수수료수익  외환거래이익  기타(계)
            기말
            2019/12                  41.49     46.58        7.53          2.65      1.75
            2020/12                  56.93     33.26        5.92          2.65      1.24
            2021/12                  50.70     36.39        7.19          2.07      3.65
            2022/12                  54.21     34.58        5.27          3.31      2.63

    @profitRate
        constraint  : stockonly
        type        : DataFrame
        description : profit rate
        example     :
                     매출총이익율  세전계속사업이익률  영업이익률  EBITDA마진율   ROA   ROE  ROIC
            2019/12          43.5                41.7        37.7          42.6  17.4  18.8  44.0
            2020/12          44.1                36.5        38.7          43.7  16.1  17.4  48.6
            2021/12          46.8                49.6        41.8          46.2  25.1  27.5  69.0
            2022/12          48.0                47.8        42.4          46.7  22.9  25.1  70.6
            2023/3Q          48.3                54.7        42.6          47.9  20.1  21.7  56.0

    @sectorWeights
        constraint  : etfonly
        type        : DataFrame
        description : sector weights of the etf
        example     :
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

    @shareHolders
        constraint  : stockonly
        type        : Series
        description : stock shares holded by affiliate person
        example     :
            최대주주등      9.13
            5%이상주주    12.02
            임원         0.04
            자기주식       0.66
            공시제외주주    78.15
            dtype: float64

    @shareInstitutes
        constraint  : stockonly
        type        : DataFrame
        description : stock shares holded by institutes

    @shortBalance
        constraint  : stockonly
        type        : DataFrame
        description : short balance
        example     :
                       대차잔고비중   종가
            날짜
            2022-10-17        3.50  139900
            2022-10-24        3.50  140000
            2022-10-31        3.44  136800
            ...                ...     ...
            2023-10-02        9.45  153800
            2023-10-09        9.52  154700
            2023-10-16        8.69  156800

    @shortSell
        constraint  : stockonly
        type        : DataFrame
        description : short sell ratio
        example     :
                        공매도비중     종가
            날짜
            2022-11-28        1.37  12150.0
            2022-12-05        5.70  12800.0
            2022-12-12        1.75  12850.0
            ...                ...      ...
            2023-11-06        8.32  12570.0
            2023-11-13        0.09  12400.0
            2023-11-20        0.13  12490.0

    @snapShot
        constraint  : common
        type        : Series
        description : snap shot of the asset
        example     :
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

    @stabilityRate
        constraint  : stockonly
        type        : DataFrame
        description : stability rate of the corp.
        example     :
                     유동비율  당좌비율  부채비율  유보율  순차입금비율  이자보상배율  자기자본비율
            2019/12     980.4     932.0       8.5  3869.6           NaN        8094.6          92.2
            2020/12    1175.7    1119.3       7.2  4357.2           NaN       12174.7          93.3
            2021/12     730.0     704.8      11.7  5411.7           NaN       17775.4          89.6
            2022/12    1036.3    1000.2       7.8  6402.1           NaN       18929.7          92.8
            2023/3Q     956.9     924.2       8.7  6902.7           NaN       11841.9          92.0
    """

    def __init__(self, ticker:str):
        self.ticker = ticker
        self.url = _url(ticker)
        return

    @stockonly
    def abstract(self) -> DataFrame:
        def _get_(index:int) -> DataFrame:
            data = web.list(self.url.snapshot)[index]
            data = data.set_index(keys=[data.columns[0]])
            if isinstance(data.columns[0], tuple):
                data.columns = data.columns.droplevel()
            else:
                data.columns = data.iloc[0]
                data = data.drop(index=data.index[0])
            data = data.T
            data = data.head(len(data) - len([i for i in data.index if i.endswith(')')]) + 1)
            data.index.name = '기말'
            data.columns.name = None
            for col in data:
                data[col] = data[col].apply(str2num)
            return data
        return multiframes(dict(
            Y=_get_(11 if self.url.gb == 'D' else 14),
            Q=_get_(12 if self.url.gb == 'D' else 15)
        ))

    @stockonly
    def benchmarkMultiples(self) -> DataFrame:
        json = web.json(self.url.cdn.benchmarkMultiples)
        def _get_(key: str) -> DataFrame:
            head = DataFrame(json[f'{key}_H'])[['ID', 'NAME']].set_index(keys='ID')
            head['NAME'] = head['NAME'].str.replace("'", "20")
            head = head.to_dict()['NAME']
            head.update({'CD_NM': '이름'})
            data = DataFrame(json[key])[head.keys()].rename(columns=head).set_index(keys='이름')
            data.index.name = None
            return data.replace('-', nan).T.astype(float)
        return concat(
            objs={'PER': _get_('02'), 'EV/EBITDA': _get_('03'), 'ROE': _get_('04'), '배당수익률': _get_('05')},
            axis=1
        )

    @stockonly
    def businessSummary(self) -> str:
        html = web.html(self.url.snapshot).find('ul', id='bizSummaryContent').find_all('li')
        t = '\n\n '.join([e.text for e in html])
        w = [
            '.\n' if t[n] == '.' and not any([t[n - 1].isdigit(), t[n + 1].isdigit(), t[n + 1].isalpha()]) else t[n]
            for n in range(1, len(t) - 2)
        ]
        s = f' {t[0]}{str().join(w)}{t[-2]}{t[-1]}'
        return s.replace(' ', '').replace('\xa0\xa0', ' ').replace('\xa0', ' ').replace('\n ', '\n')

    @stockonly
    def cashFlow(self) -> DataFrame:
        cut = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        col = {
            "영업활동으로인한현금흐름": "영업현금흐름",
            "투자활동으로인한현금흐름": "투자현금흐름",
            "재무활동으로인한현금흐름": "재무현금흐름",
            "환율변동효과": "환율변동손익",
            "기말현금및현금성자산": "현금및현금성자산"
        }
        def _get_(index:int) -> DataFrame:
            data = web.list(self.url.finance)[index]
            data = data.set_index(keys=[data.columns[0]])
            data = data.drop(columns=[c for c in data if not c.startswith('20')])
            data.index.name = None
            data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
            data.index = [cutString(x, cut) for x in data.index]
            data = data.T
            return data[col.keys()].rename(columns=col).fillna(0).astype(int)
        return multiframes(dict(
            Y=_get_(4),
            Q=_get_(5)
        ))

    @stockonly
    def consensusOutstanding(self) -> Series:
        src = web.list(self.url.snapshot)[7]
        data = []
        for dat in src.iloc[0].tolist():
            try:
                data.append(float(dat))
            except ValueError:
                data.append(nan)
        return Series(dict(zip(src.columns.tolist(), data)))

    @stockonly
    def consensusPrice(self) -> DataFrame:
        cols = {'TRD_DT': '날짜', 'VAL1': '투자의견', 'VAL2': '컨센서스', 'VAL3': '종가'}
        data = web.data(self.url.cdn.priceConsensus, "CHART")
        data = data.rename(columns=cols).set_index(keys='날짜')
        data.index = to_datetime(data.index)
        for col in data:
            data[col] = data[col].apply(str2num)
        data['격차'] = round(100 * (data['종가'] / data['컨센서스'] - 1), 2)
        return data.astype(float)

    @stockonly
    def consensusProfit(self) -> DataFrame:
        cols = {
            "GS_YM": "기말",
            "SALES_R": "매출실적", "SALES_F": "매출전망",
            "OP_R": "영업이익실적", "OP_F": "영업이익전망"
        }
        yy = web.data(self.url.cdn.profitConsensusAnnual, "CHART")[cols.keys()].rename(columns=cols)
        qq = web.data(self.url.cdn.profitConsensusQuarter, "CHART")[cols.keys()].rename(columns=cols)
        for y, q in zip(yy, qq):
            yy[y] = yy[y].apply(str2num)
            qq[q] = qq[q].apply(str2num)
        return multiframes(dict(Y=yy, Q=qq))

    @stockonly
    def consensusThisFiscalYear(self) -> DataFrame:
        cols = {
            "STD_DT": "날짜",
            "SALES": "매출", "SALES_MAX": "매출(최대)", "SALES_MIN": "매출(최소)",
            "OP": "영업이익", "OP_MAX": "영업이익(최대)", "OP_MIN": "영업이익(최소)",
            "EPS": "EPS", "EPS_MAX": "EPS(최대)", "EPS_MIN": "EPS(최소)",
            "PER": "PER", "PER_MAX": "PER(최대)", "PER_MIN": "PER(최소)", "PER_12F": "12M PER"
        }
        data = web.data(self.url.cdn.abstractConsensusRelevant, "CHART")
        if data.empty:
            return DataFrame(columns=list(cols.values()))
        data = data[cols.keys()].rename(columns=cols).set_index(keys='날짜')
        for col in data:
            data[col] = data[col].apply(str2num)
        return data

    @stockonly
    def consensusNextFiscalYear(self) -> DataFrame:
        cols = {
            "STD_DT": "날짜",
            "SALES": "매출", "SALES_MAX": "매출(최대)", "SALES_MIN": "매출(최소)",
            "OP": "영업이익", "OP_MAX": "영업이익(최대)", "OP_MIN": "영업이익(최소)",
            "EPS": "EPS", "EPS_MAX": "EPS(최대)", "EPS_MIN": "EPS(최소)",
            "PER": "PER", "PER_MAX": "PER(최대)", "PER_MIN": "PER(최소)", "PER_12F": "12M PER"
        }
        data = web.data(self.url.cdn.abstractConsensusForward, "CHART")
        if data.empty:
            return DataFrame(columns=list(cols.values()))
        data = data[cols.keys()].rename(columns=cols).set_index(keys='날짜')
        for col in data:
            data[col] = data[col].apply(str2num)
        return data

    @stockonly
    def expenses(self) -> DataFrame:
        json = web.json(self.url.cdn.expenses)
        def _get_(period: str) -> DataFrame:
            manage = DataFrame(json[f"05_{period}"]).set_index(keys="GS_YM")["VAL1"]
            cost = DataFrame(json[f"06_{period}"]).set_index(keys="GS_YM")["VAL1"]
            manage.index.name = cost.index.name = '기말'
            data = concat({"판관비율": manage, "매출원가율": cost}, axis=1)
            for col in data:
                data[col] = data[col].apply(str2num)
            return data
        return multiframes(dict(Y=_get_('Y'), Q=_get_('Q')))

    @stockonly
    def financialStatement(self) -> DataFrame:
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        def _get_(period:str) -> DataFrame:
            data = web.list(self.url.finance)[{"Y": 2, "Q": 3}[period]]
            data = data.set_index(keys=[data.columns[0]])
            data = data.drop(columns=[col for col in data if not col.startswith('20')])
            data.index.name = None
            data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
            data.index = [cutString(x, cutter) for x in data.index]
            return data.T.astype(float)
        return multiframes(dict(Y=_get_("Y"), Q=_get_("Q")))

    @stockonly
    def financialSeparatedStatement(self) -> DataFrame:
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        def _get_(period: str) -> DataFrame:
            data = web.list(self.url.financeB)[{"Y": 2, "Q": 3}[period]]
            data = data.set_index(keys=[data.columns[0]])
            data = data.drop(columns=[col for col in data if not col.startswith('20')])
            data.index.name = None
            data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
            data.index = [cutString(x, cutter) for x in data.index]
            return data.T.astype(float)
        return multiframes(dict(Y=_get_("Y"), Q=_get_("Q")))

    @stockonly
    def foreignExhaustRate(self) -> DataFrame:
        urls = [self.url.cdn.foreignRate3Months, self.url.cdn.foreignRate1Year, self.url.cdn.foreignRate3Years]
        cols = {'TRD_DT': '날짜', 'J_PRC': '종가', 'FRG_RT': '비중'}
        objs = {}
        for _url_ in urls:
            data = web.data(_url_, "CHART")[cols.keys()]
            data = data.rename(columns=cols).set_index(keys='날짜')
            data.index = to_datetime(data.index)
            for col in data:
                data[col] = data[col].apply(str2num)
            objs[_url_[_url_.rfind('_') + 1: _url_.rfind('.')]] = data
        return concat(objs=objs, axis=1)

    @stockonly
    def growthRate(self) -> DataFrame:
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        def _get_(index:int):
            data = web.list(self.url.ratio)[index]
            cols = data[data.columns[0]].tolist()
            data = data.iloc[cols.index('성장성비율') + 1: cols.index('수익성비율')]
            data = data.set_index(keys=[data.columns[0]])
            data = data.drop(columns=[col for col in data if not col.startswith('20')])
            data.index.name = None
            data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
            data.index = [cutString(x, cutter) for x in data.index]
            return data.T.astype(float)
        return multiframes(dict(Y=_get_(0), Q=_get_(1)))

    @stockonly
    def incomeStatement(self) -> DataFrame:
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*']
        def _get_(period:str) -> DataFrame:
            data = web.list(self.url.finance)[{"Y": 0, "Q": 1}[period]]
            data = data.set_index(keys=[data.columns[0]])
            data = data.drop(columns=[col for col in data if not col.startswith('20')])
            data.index.name = None
            data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
            data.index = [cutString(x, cutter) for x in data.index]
            return data.T.astype(float)
        return multiframes(dict(Y=_get_("Y"), Q=_get_("Q")))

    @stockonly
    def marketShares(self) -> DataFrame:
        src = web.list(self.url.corp)[{'D': 10, 'B': 11}[self.url.gb]]
        data = src[src.columns[1:]].set_index(keys=src.columns[1])
        data = data.T.copy()
        if all([i.startswith("Unnamed") for i in data.index]):
            return DataFrame(columns=["내수", "수출"])
        data.columns = [col.replace("\xa0", " ") for col in data.columns]

        domestic = data[data[data.columns[0]] == "내수"].drop(columns=data.columns[0])
        exported = data[data[data.columns[0]] == "수출"].drop(columns=data.columns[0])
        domestic.index = exported.index = [i.replace('.1', '') for i in domestic.index]
        domestic.columns.name = exported.columns.name = None
        data = concat(objs={"내수": domestic, "수출": exported}, axis=1)
        # return data  # 내수/수출 구분 우선 시
        data = concat(objs={(c[1], c[0]): data[c] for c in data}, axis=1)
        return data[sorted(data.columns, key=lambda x: x[0])]  # 상품 구분 우선 시

    @stockonly
    def multipleBand(self) -> DataFrame:
        json = web.json(self.url.cdn.multipleBands)
        def _get_(key: str) -> DataFrame:
            head = DataFrame(json[key])[['ID', 'NAME']].set_index(keys='ID')
            head = head.to_dict()['NAME']
            head.update({'GS_YM': '날짜', 'PRICE': '종가'})
            data = DataFrame(json['CHART']).rename(columns=head)[head.values()]
            data["날짜"] = to_datetime(data["날짜"])
            data = data.set_index(keys='날짜')
            for col in data:
                data[col] = data[col].apply(str2num)
            return data
        return concat(objs={'PER': _get_('CHART_E'), 'PBR': _get_('CHART_B')}, axis=1)

    @common
    def multiplesOutstanding(self) -> Series:
        if meta(self.ticker).quoteType == "ETF":
            html = web.html(self.url.etf)
            script = html.find_all('script')[-1].text.split('\n')
            pe = script[[n for n, h in enumerate(script) if "PER" in h][0] + 1]
            pb = script[[n for n, h in enumerate(script) if "PBR" in h][0] + 1]
            data = {
                "dividendYield": str2num(html.find_all('td', class_='r cle')[-1].text),
                "fiscalPE": str2num(pe[pe.index(":"):]),
                "priceToBook": str2num(pb[pb.index(":"):])
            }
        else:
            src = web.html(self.url.snapshot).find('div', id='corp_group2')
            src = [val for val in src.text.split('\n') if val]
            data = {
                "fiscalPE": str2num(src[src.index('PER') + 1]),
                "forwardPE": str2num(src[src.index('12M PER') + 1]),
                "sectorPE": str2num(src[src.index('업종 PER') + 1]),
                "priceToBook": str2num(src[src.index('PBR') + 1]),
                "dividendYield": str2num(src[src.index('배당수익률') + 1]),
            }
        return Series(data)

    @stockonly
    def products(self) -> DataFrame:
        json = web.json(self.url.cdn.products)
        head = DataFrame(json['chart_H'])[['ID', 'NAME']].set_index(keys='ID').to_dict()['NAME']
        head.update({'PRODUCT_DATE': '기말'})
        data = DataFrame(json['chart']).rename(columns=head).set_index(keys='기말')
        data = data.drop(columns=[c for c in data.columns if data[c].astype(float).sum() == 0])

        i = data.columns[-1]
        data['Sum'] = data.astype(float).sum(axis=1)
        data = data[(90 <= data.Sum) & (data.Sum < 110)].astype(float)
        data[i] = data[i] - (data.Sum - 100)
        return data.drop(columns=['Sum'])

    @stockonly
    def profitRate(self) -> DataFrame:
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        data = web.list(self.url.ratio)[0]
        cols = data[data.columns[0]].tolist()
        idet = cols.index('수익성비율') + 1
        iend = cols.index('활동성비율') if "활동성비율" in cols else len(cols) - 1
        data = data.iloc[idet: iend]
        data = data.set_index(keys=[data.columns[0]])
        data = data.drop(columns=[col for col in data if not col.startswith('20')])
        data.index.name = None
        data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
        data.index = [cutString(x, cutter) for x in data.index]
        return data.T.astype(float)

    @etfonly
    def sectorWeights(self) -> DataFrame:
        html = web.html(self.url.etf)
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

    @stockonly
    def shareHolders(self) -> Series:
        data = web.data(self.url.cdn.shares).replace("", nan)
        return Series(index=data["NM"].values, data=data["STK_RT"].values, dtype=float).dropna()

    @stockonly
    def shareInstitutes(self) -> Series:
        data = web.list(self.url.snapshot)[2]
        return data.replace("관련 데이터가 없습니다.", nan)

    @stockonly
    def shortBalance(self) -> DataFrame:
        cols = {'TRD_DT': '날짜', 'BALANCE_RT': '대차잔고비중', 'ADJ_PRC': '종가'}
        data = web.data(self.url.cdn.shortBalance, "CHART").rename(columns=cols)[cols.values()].set_index(keys='날짜')
        data.index = to_datetime(data.index)
        return data.replace("", nan).astype(float)

    @stockonly
    def shortSell(self) -> DataFrame:
        cols = {'TRD_DT': '날짜', 'VAL': '공매도비중', 'ADJ_PRC': '종가'}
        data = web.data(self.url.cdn.shortSell, "CHART").rename(columns=cols).set_index(keys='날짜')
        data.index = to_datetime(data.index)
        return data.replace("", nan).astype(float)

    @common
    def snapShot(self) -> Series:
        src = web.html(self.url.xml).find('price')
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

    @stockonly
    def stabilityRate(self) -> DataFrame:
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        data = web.list(self.url.ratio)[0]
        cols = data[data.columns[0]].tolist()
        data = data.iloc[cols.index('안정성비율') + 1: cols.index('성장성비율')]
        data = data.set_index(keys=[data.columns[0]])
        data = data.drop(columns=[col for col in data if not col.startswith('20')])
        data.index.name = None
        data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
        data.index = [cutString(x, cutter) for x in data.index]
        return data.T.astype(float)


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    fn = fnguide(
        # "005930"
        "069500"
    )

    # print(fn.abstract)
    # print(fn.abstract.Y)
    # print(fn.abstract.Q)
    # print(fn.benchmarkMultiples)
    # print(fn.businessSummary)
    # print(fn.cashFlow)
    # print(fn.consensusOutstanding)
    # print(fn.consensusPrice)
    # print(fn.consensusProfit)
    # print(fn.consensusProfit.Y)
    # print(fn.consensusProfit.Q)
    # print(fn.consensusThisFiscalYear)
    # print(fn.consensusNextFiscalYear)
    # print(fn.expenses)
    # print(fn.expenses.Y)
    # print(fn.expenses.Q)
    # print(fn.financialStatement)
    # print(fn.financialStatement.Y)
    # print(fn.financialStatement.Q)
    # print(fn.financialSeparatedStatement)
    # print(fn.financialSeparatedStatement.Y)
    # print(fn.financialSeparatedStatement.Q)
    # print(fn.foreignExhaustRate)
    # print(fn.growthRate)
    # print(fn.growthRate.Y)
    # print(fn.growthRate.Q)
    # print(fn.incomeStatement)
    # print(fn.incomeStatement.Y)
    # print(fn.incomeStatement.Q)
    # print(fn.marketShares)
    # print(fn.multipleBand)
    # print(fn.multiplesOutstanding)
    # print(fn.products)
    # print(fn.profitRate)
    # print(fn.shareHolders)
    # print(fn.shareInstitutes)
    # print(fn.shortBalance)
    # print(fn.shortSell)
    # print(fn.snapShot)
    # print(fn.stabilityRate)

    print(fn.sectorWeights)