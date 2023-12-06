from labwons.common.metadata import metaData
from labwons.common.web import web
from labwons.common.tools import cutString, str2num
from labwons.equity.ticker.kr.urls import urls
from typing import Union
from datetime import datetime, timedelta
from pykrx.stock import get_market_cap_by_date
from pykrx.stock import get_etf_portfolio_deposit_file
from pykrx.stock import get_market_ohlcv_by_date
import pandas, numpy

class _price:

    _ed_:datetime.date = datetime.today().date()
    _pr_:int = 10
    _fq_:str = 'd' # one of ['d', 'm', 'y']
    def __init__(self, ticker:str):
        self.ticker = ticker
        return

    @property
    def enddate(self) -> str:
        return self._ed_.strftime("%Y%m%d")

    @enddate.setter
    def enddate(self, enddate:Union[str, datetime, datetime.date]):
        if isinstance(enddate, str):
            self._ed_ = datetime.strptime(enddate, "%Y%m%d").date()
        elif isinstance(enddate, datetime):
            self._ed_ = enddate.date()
        else:
            self._ed_ = enddate

    @property
    def period(self) -> int:
        return self._pr_

    @period.setter
    def period(self, period:int):
        self._pr_ = period

    @property
    def freq(self) -> str:
        return self._fq_

    @freq.setter
    def freq(self, freq:str):
        if not freq in ['d', 'm', 'y']:
            raise KeyError
        self._fq_ = freq

    @property
    def price(self) -> pandas.DataFrame:
        attr = f"_{self.enddate}_{self.period}_{self.freq}_"
        if not hasattr(self, attr):
            ohlcv = get_market_ohlcv_by_date(
                fromdate=(self._ed_ - timedelta(365 * self._pr_)).strftime("%Y%m%d"),
                todate=self.enddate,
                ticker=self.ticker,
                freq=self.freq
            )
            ohlcv = ohlcv.rename(columns=dict(시가='open', 고가='high', 저가='low', 종가='close', 거래량='volume'))

            trade_stop = ohlcv[ohlcv["open"] == 0].copy()
            if not trade_stop.empty:
                ohlcv.loc[trade_stop.index, ['open', 'high', 'low']] = trade_stop['close']
            ohlcv.index.name = 'date'
            self.__setattr__(attr, ohlcv)
        return self.__getattribute__(attr)



class stock(_price):

    class _two_dataframes(pandas.DataFrame):
        Y:pandas.DataFrame = pandas.DataFrame()
        Q:pandas.DataFrame = pandas.DataFrame()
        ThisYear: pandas.DataFrame = pandas.DataFrame()
        NextYear: pandas.DataFrame = pandas.DataFrame()
        def __init__(self, **kwargs):
            if "Y" in kwargs and "Q" in kwargs:
                self.Y, self.Q = kwargs["Y"], kwargs["Q"]
                super().__init__(self.Y.values, self.Y.index, self.Y.columns)
            elif "ThisYear" in kwargs and "NextYear" in kwargs:
                self.ThisYear, self.NextYear = kwargs["ThisYear"], kwargs["NextYear"]
                super().__init__(self.ThisYear.values, self.ThisYear.index, self.ThisYear.columns)
            else:
                raise KeyError
            return


    def __init__(self, ticker:str):
        super().__init__(ticker=ticker)
        self.urls = urls(ticker)
        return


    @property
    def abstract(self) -> pandas.DataFrame:
        """
        :return:
                      이자수익 영업이익 당기순이익 ...   PER   PBR 발행주식수 배당수익률
            기말
            2018/12        NaN     NaN        NaN  ...   NaN   NaN       NaN        NaN
            2019/12     105768   28000      20376  ...  4.29  0.39    722268       6.03
            2020/12      95239   20804      15152  ...  5.38  0.30    722268       3.70
            2021/12      98947   36597      28074  ...  3.56  0.36    728061       7.09
            2022/12     146545   44305      33240  ...  2.68  0.29    728061       9.78
            2023/12(E)  198704   40045      30132  ...  3.25  0.30       NaN        NaN

        :columns: ['이자수익', '영업이익', '영업이익(발표기준)', '당기순이익',
                   '지배주주순이익', '비지배주주순이익',
                   '자산총계', '부채총계', '자본총계', '지배주주지분', '비지배주주지분',
                   '자본금', '부채비율', '유보율', '영업이익률',
                   '지배주주순이익률', 'ROA', 'ROE', 'EPS(원)', 'BPS(원)', 'DPS(원)', 'PER', 'PBR',
                   '발행주식수', '배당수익률']
        """
        url = self.urls.snapshot
        def _get_(index:int) -> pandas.DataFrame:
            data = web.list(url)[index]
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

        if not hasattr(self, "_abstract"):
            yy = 11 if self.urls.gb == 'D' else 14
            qq = 12 if self.urls.gb == 'D' else 15
            self.__setattr__("_abstract", self._two_dataframes(Y=_get_(yy), Q=_get_(qq)))
        return self.__getattribute__("_abstract")


    @property
    def analogy(self) -> pandas.DataFrame:
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
        if not hasattr(self, '_analogy'):
            data = web.list(self.urls.naver)[4]
            data = data.set_index(keys='종목명').drop(index=['전일대비'])
            data.index.name = None
            for col in data:
                data[col] = data[col].apply(str2num)
            data = data.T
            data["종목명"] = [i.replace('*', '')[:-6] for i in data.index]
            data.index = [i[-6:] for i in data.index]
            self.__setattr__("_analogy", data)
        return self.__getattribute__("_analogy")


    @property
    def benchmarkMultiples(self) -> pandas.DataFrame:
        """
        :return:
                                                  PER  ...                           배당수익률
                  우리금융지주  코스피 금융업  코스피  ...  우리금융지주  코스피 금융업  코스피
            2021          3.56           5.94   11.08  ...          7.09           3.48    1.78
            2022          2.68           5.53   10.87  ...          9.78           4.32    2.22
            2023E         3.25           6.08   17.54  ...           NaN            NaN     NaN

        :columns: MultiIndex([(       'PER',  '우리금융지주'),
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
        """
        json = web.json(self.urls.benchmarkMultiples)
        def _get_(key: str) -> pandas.DataFrame:
            head = pandas.DataFrame(json[f'{key}_H'])[['ID', 'NAME']].set_index(keys='ID')
            head['NAME'] = head['NAME'].str.replace("'", "20")
            head = head.to_dict()['NAME']
            head.update({'CD_NM': '이름'})
            data = pandas.DataFrame(json[key])[head.keys()].rename(columns=head).set_index(keys='이름')
            data.index.name = None
            return data.replace('-', numpy.nan).T.astype(float)

        if not hasattr(self, "_benchmarkMultiples"):
            attr = pandas.concat(
                objs={
                    'PER': _get_('02'),
                    'EV/EBITDA': _get_('03'),
                    'ROE': _get_('04'),
                    '배당수익률': _get_('05')
                }, axis=1
            )
            self.__setattr__("_benchmarkMultiples", attr)
        return self.__getattribute__("_benchmarkMultiples")


    @property
    def businessSummary(self) -> str:
        """
        :return:
            동사는 2019년 1월 설립한 지주회사로 주요 종속회사들의 사업은 은행업, 신용카드업, 종합금융업 등임.
            ...
            비금융 포트폴리오를 확대하기 위해 중형급 이상 증권사를 인수하는 방안도 지속 고려하고 있음.
        """
        html = web.html(self.urls.snapshot).find('ul', id='bizSummaryContent').find_all('li')
        t = '\n\n '.join([e.text for e in html])
        w = [
            '.\n' if t[n] == '.' and not any([t[n - 1].isdigit(), t[n + 1].isdigit(), t[n + 1].isalpha()]) else t[n]
            for n in range(1, len(t) - 2)
        ]
        s = f' {t[0]}{str().join(w)}{t[-2]}{t[-1]}'
        return s.replace(' ', '').replace('\xa0\xa0', ' ').replace('\xa0', ' ').replace('\n ', '\n')


    @property
    def cashFlow(self) -> pandas.DataFrame:
        """
        :param period : [str] 연간 = 'Y', 분기 = 'Q'
        :return:
                     영업현금흐름  투자현금흐름  재무현금흐름  환율변동손익  현금및현금성자산
            2020/12        123146       -118404          2521          -563             29760
            2021/12        197976       -223923         44923          1843             50580
            2022/12        147805       -178837         28218          2005             49770
            2023/2Q         -6940        -53509         70579           508             60408
        """
        cut = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        col = {
            "영업활동으로인한현금흐름": "영업현금흐름",
            "투자활동으로인한현금흐름": "투자현금흐름",
            "재무활동으로인한현금흐름": "재무현금흐름",
            "환율변동효과": "환율변동손익",
            "기말현금및현금성자산": "현금및현금성자산"
        }
        url = self.urls.finance
        def _get_(index:int) -> pandas.DataFrame:
            data = web.list(url)[index]
            data = data.set_index(keys=[data.columns[0]])
            data = data.drop(columns=[c for c in data if not c.startswith('20')])
            data.index.name = None
            data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
            data.index = [cutString(x, cut) for x in data.index]
            data = data.T
            return data[col.keys()].rename(columns=col).fillna(0).astype(int)

        if not hasattr(self, '_cashflow'):
            self.__setattr__('_cashflow', self._two_dataframes(Y=_get_(4), Q=_get_(5)))
        return self.__getattribute__('_cashflow')


    @property
    def consensusOutstanding(self) -> pandas.Series:
        """
        :return:
            투자의견         4.0
            목표주가     15411.0
            EPS           3908.0
            PER              3.3
            추정기관수      18.0
            dtype: float64
        """
        src = web.list(self.urls.snapshot)[7]
        data = []
        for dat in src.iloc[0].tolist():
            try: data.append(float(dat))
            except ValueError: data.append(numpy.nan)
        return pandas.Series(dict(zip(src.columns.tolist(), data)))


    @property
    def consensusPrice(self) -> pandas.DataFrame:
        """
        :return:
                       투자의견  컨센서스     종가   격차
            날짜
            2022-11-23      4.0   16378.0  12300.0 -24.90
            2022-11-24      4.0   16378.0  12550.0 -23.37
            2022-11-25      4.0   16378.0  12450.0 -23.98
            ...             ...       ...      ...    ...
            2023-11-20      4.0   15411.0  12490.0 -18.95
            2023-11-21      4.0   15411.0  12720.0 -17.46
            2023-11-22      4.0   15411.0  12700.0 -17.59
        """
        cols = {'TRD_DT': '날짜', 'VAL1': '투자의견', 'VAL2': '컨센서스', 'VAL3': '종가'}
        data = web.data(self.urls.consensusPrice, "CHART")
        data = data.rename(columns=cols)
        data = data.set_index(keys='날짜')
        data.index = pandas.to_datetime(data.index)
        data = data.replace("", numpy.nan)
        data['격차'] = round(100 * (data['종가'] / data['컨센서스'] - 1), 2)
        return data.astype(float)


    @property
    def consensusProfit(self) -> pandas.DataFrame:
        """
        :return:
            [연간]
                    매출실적  매출전망  영업이익실적  영업이익전망
            기말
            2020/12  2013.35   2032.00        778.82        784.67
            2021/12  2801.67   2773.23       1171.04       1144.04
            2022/12  3224.23   3340.00       1366.35       1460.00
            2023/12      NaN   2578.67           NaN       1055.50
            2024/12      NaN   3048.83           NaN       1278.83
            2025/12      NaN   3469.00           NaN       1465.50

            [분기]
                    매출실적  매출전망  영업이익실적  영업이익전망
            기말
            2023/03   490.91    732.25        172.63         277.5
            2023/06   751.31    696.25        335.62         266.0
            2023/09   733.99    770.25        333.24         332.0
            2023/12      NaN    601.60           NaN         213.0
            2024/03      NaN    582.50           NaN         219.5
            2024/06      NaN    817.00           NaN         366.5
        """
        cols = {
            "GS_YM": "기말",
            "SALES_R": "매출실적", "SALES_F": "매출전망",
            "OP_R": "영업이익실적", "OP_F": "영업이익전망"
        }
        def _get_(url:str) -> pandas.DataFrame:
            data = web.data(url, "CHART").replace('-', numpy.nan)[cols.keys()]
            data = data.rename(columns=cols)
            return data.set_index(keys="기말").astype(float)
        return self._two_dataframes(Y=_get_(self.urls.consensusAnnualProfit), Q=_get_(self.urls.consensusQuarterProfit))


    @property
    def consensusTendency(self) -> pandas.DataFrame:
        """
        :return:
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

        :columns: ['매출', '매출(최대)', '매출(최소)', '영업이익', '영업이익(최대)', '영업이익(최소)', 'EPS',
                   'EPS(최대)', 'EPS(최소)', 'PER', 'PER(최대)', 'PER(최소)', '12M PER']
        """
        cols = {
            "STD_DT": "날짜",
            "SALES": "매출", "SALES_MAX": "매출(최대)", "SALES_MIN": "매출(최소)",
            "OP": "영업이익", "OP_MAX": "영업이익(최대)", "OP_MIN": "영업이익(최소)",
            "EPS": "EPS", "EPS_MAX": "EPS(최대)", "EPS_MIN": "EPS(최소)",
            "PER": "PER", "PER_MAX": "PER(최대)", "PER_MIN": "PER(최소)", "PER_12F": "12M PER"
        }
        def _get_(url:str) -> pandas.DataFrame:
            data = web.data(url, "CHART")
            if data.empty:
                return pandas.DataFrame(columns=list(cols.values()))
            data = data[cols.keys()].rename(columns=cols)
            data = data.set_index(keys='날짜')
            for col in data:
                data[col] = data[col].apply(str2num)
            return data
        return self._two_dataframes(
            ThisYear=_get_(self.urls.consensusForward1Y), NextYear=_get_(self.urls.consensusForward2Y)
        )


    @property
    def currentPrice(self) -> int or float:
        if not hasattr(self, '_curprc'):
            html = web.html(self.urls.naver)
            curr = [d.text for d in html.find_all("dd") if d.text.startswith("현재가")][0]
            self.__setattr__('_curprc', str2num(curr[curr.index("현재가 ") + 4: curr.index(" 전일대비")]))
        return self.__getattribute__('_curprc')


    @property
    def expenses(self) -> pandas.DataFrame:
        """
        :return:
                     판관비율  매출원가율
            기말
            2019/12     16.58       20.62
            2020/12     13.81       12.31
            2021/12     15.25       10.70
            2022/12     10.69       14.06
        """
        json = web.json(self.urls.expenses)
        def exp(period: str) -> pandas.Series:
            manage = pandas.DataFrame(json[f"05_{period}"]).set_index(keys="GS_YM")["VAL1"]
            cost = pandas.DataFrame(json[f"06_{period}"]).set_index(keys="GS_YM")["VAL1"]
            manage.index.name = cost.index.name = '기말'
            concat = pandas.concat({"판관비율": manage, "매출원가율": cost}, axis=1)
            for col in concat:
                concat[col] = concat[col].apply(str2num)
            return concat
        return self._two_dataframes(Y=exp('Y'), Q=exp('Q'))


    @property
    def financialStatement(self) -> pandas.DataFrame:
        """
        :return:
            [연결]
                     자산  유동자산  비유동자산  기타금융업자산  부채  유동부채  비유동부채  ...  이익잉여금결손금
            2020/12  3615      2577        1038             NaN   242       219          23  ...              3265
            2021/12  4664      3357        1306             NaN   487       460          27  ...              4068
            2022/12  5315      3770        1545             NaN   383       364          19  ...              4823
            2023/3Q  5773      4194        1579             NaN   460       438          22  ...              5205

        :columns: ['자산', '유동자산', '비유동자산', '기타금융업자산', '부채', '유동부채', '비유동부채', '기타금융업부채',
                   '자본', '자본금', '신종자본증권', '자본잉여금', '기타자본', '기타포괄손익누계액', '이익잉여금결손금']
        """
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        def _get_(period:str) -> pandas.DataFrame:
            data = web.list(self.urls.finance)[{"Y": 2, "Q": 3}[period]]
            data = data.set_index(keys=[data.columns[0]])
            data = data.drop(columns=[col for col in data if not col.startswith('20')])
            data.index.name = None
            data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
            data.index = [cutString(x, cutter) for x in data.index]
            return data.T.astype(float)
        return self._two_dataframes(Y=_get_("Y"), Q=_get_("Q"))


    @property
    def financialStatementSeparate(self) -> pandas.DataFrame:
        """
        :return:
            [별도]
                     유동자산  현금및단기예금  유가증권  매출채권  재고자산  임대주택자산  비유동자산  ...  투하자본
            2020/12      2577            2066       NaN       291       123           NaN        1038  ...      1235
            2021/12      3357    	     2830       NaN       354       116           NaN        1306  ...      1340
            2022/12      3770            3171       NaN       393       131           NaN        1545  ...      1740
            2023/3Q      4194            3545       NaN       433       143           NaN        1579  ...      1719

        :columns: ['유동자산', '현금및단기예금', '유가증권', '매출채권', '재고자산', '임대주택자산', '비유동자산',
                   '투자자산', '유형자산', '감가상각자산', '무형자산', '자산총계', '유동부채', '매입채무',
                   '단기차입금', '유동성장기부채', '비유동부채', '사채', '장기차입금', '이연부채', '부채총계',
                   '자본금', '자본잉여금', '자본조정', '자기주식', '기타포괄손익누계액', '이익잉여금', '자본총계',
                   '순운전자본', '순차입금', '투하자본']

        """
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        def _get_(period: str) -> pandas.DataFrame:
            data = web.list(self.urls.separateFinance)[{"Y": 2, "Q": 3}[period]]
            data = data.set_index(keys=[data.columns[0]])
            data = data.drop(columns=[col for col in data if not col.startswith('20')])
            data.index.name = None
            data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
            data.index = [cutString(x, cutter) for x in data.index]
            return data.T.astype(float)
        return self._two_dataframes(Y=_get_("Y"), Q=_get_("Q"))


    @property
    def foreignRate(self) -> pandas.DataFrame:
        """
        :return:
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
        """
        cols = {'TRD_DT': '날짜', 'J_PRC': '종가', 'FRG_RT': '비중'}
        objs = {}
        for u in [self.urls.foreignRate3M, self.urls.foreignRate1Y, self.urls.foreignRate3Y]:
            data = web.data(u, "CHART")[cols.keys()]
            data = data.rename(columns=cols).set_index(keys='날짜')
            data.index = pandas.to_datetime(data.index)
            for col in data:
                data[col] = data[col].apply(str2num)
            objs[u[u.rfind('_') + 1: u.rfind('.')]] = data
        return pandas.concat(objs=objs, axis=1)


    @property
    def growthRate(self) -> pandas.DataFrame:
        """
        :return:
                     매출액증가율  판매비와관리비증가율  영업이익증가율  EBITDA증가율  EPS증가율
            2019/12          13.3                  -4.2            11.5           9.8        8.5
            2020/12          18.2                   8.8            21.4          21.4        4.9
            2021/12          39.2                  29.7            50.4          47.0       87.5
            2022/12          15.1                  27.3            16.7          16.4       10.2
            2023/3Q         -27.0                 -24.8           -30.4         -28.0      -21.4
        """
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        data = web.list(self.urls.ratio)[0]
        cols = data[data.columns[0]].tolist()
        data = data.iloc[cols.index('성장성비율') + 1: cols.index('수익성비율')]
        data = data.set_index(keys=[data.columns[0]])
        data = data.drop(columns=[col for col in data if not col.startswith('20')])
        data.index.name = None
        data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
        data.index = [cutString(x, cutter) for x in data.index]
        return data.T.astype(float)


    @property
    def incomeStatement(self) -> pandas.DataFrame:
        """
        :return:
                     매출액 매출원가 매출총이익 판매비와관리비 영업이익 금융수익 금융원가 기타수익 기타비용 ... 당기순이익
            2020/12  319004   210898     108106          57980    50126    33279    19804      848     1716 ...      47589
            2021/12  429978   240456     189522   		 65419   124103    23775    14699     1161     1804 ...      96162
            2022/12  446216   289937     156279  		 88184    68094    37143    50916     2414    18019 ...      22417
            2023/2Q  123940   152172     -28231  		 34613   -62844    15203    25144      261      739 ...     -55734

        columns: ['매출액', '매출원가', '매출총이익', '판매비와관리비', '영업이익', '영업이익발표기준',
                  '금융수익', '금융원가', '기타수익', '기타비용', '종속기업,공동지배기업및관계기업관련손익',
                  '세전계속사업이익', '법인세비용', '계속영업이익', '중단영업이익', '당기순이익',
                  '지배주주순이익', '비지배주주순이익']
        """
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*']
        def _get_(period:str) -> pandas.DataFrame:
            data = web.list(self.urls.finance)[{"Y": 0, "Q": 1}[period]]
            data = data.set_index(keys=[data.columns[0]])
            data = data.drop(columns=[col for col in data if not col.startswith('20')])
            data.index.name = None
            data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
            data.index = [cutString(x, cutter) for x in data.index]
            return data.T.astype(float)
        return self._two_dataframes(Y=_get_("Y"), Q=_get_("Q"))


    @property
    def marketCap(self) -> pandas.Series:
        """
        :return:
            2019/03     93522
            2019/06     95563
            2019/09     89922
                ...       ...
            2023/03     83071
            2023/06     85838
            2023/09     93241
            2023/11     95497
            Name: 시가총액, dtype: int32
        """
        if not hasattr(self, '_marketcap'):
            cap = get_market_cap_by_date(
                fromdate=(datetime.today() - timedelta(365 * 5)).strftime("%Y%m%d"),
                todate=datetime.today().strftime("%Y%m%d"),
                freq='m',
                ticker=self.ticker
            )
            cap = cap[
                cap.index.astype(str).str.contains('03') | \
                cap.index.astype(str).str.contains('06') | \
                cap.index.astype(str).str.contains('09') | \
                cap.index.astype(str).str.contains('12') | \
                (cap.index == cap.index[-1])
            ]
            cap.index = cap.index.strftime("%Y/%m")
            self.__setattr__('_marketcap', pandas.Series(index=cap.index, data=cap['시가총액'], dtype=int)  / 100000000)
        return self.__getattribute__('_marketcap')


    @property
    def marketShares(self) -> pandas.DataFrame:
        """
        :return:
                    IC TEST SOCKET 류   LEENO PIN 류          상품     상품 등  의료기기 부품류          합계
                        내수     수출    내수   수출    내수  수출  내수  수출       내수  수출   내수   수출
            2020/12      NaN      NaN    NaN    NaN     NaN   NaN    NaN   NaN       NaN    NaN    NaN    NaN
            2021/12      NaN      NaN    NaN    NaN     NaN   NaN    NaN   NaN       NaN    NaN    NaN    NaN
            2022/12    10.50    89.50  27.80  72.20  100.00  0.00  95.80  4.20     99.30   0.70  24.30  75.70
        """
        src = web.list(self.urls.corp)[{'D': 10, 'B': 11}[self.urls.gb]]
        data = src[src.columns[1:]].set_index(keys=src.columns[1])
        data = data.T.copy()
        if all([i.startswith("Unnamed") for i in data.index]):
            return pandas.DataFrame(columns=["내수", "수출"])
        data.columns = [col.replace("\xa0", " ") for col in data.columns]

        domestic = data[data[data.columns[0]] == "내수"].drop(columns=data.columns[0])
        exported = data[data[data.columns[0]] == "수출"].drop(columns=data.columns[0])
        domestic.index = exported.index = [i.replace('.1', '') for i in domestic.index]
        domestic.columns.name = exported.columns.name = None
        data = pandas.concat(objs={"내수": domestic, "수출": exported}, axis=1)
        # return data  # 내수/수출 구분 우선 시
        data = pandas.concat(objs={(c[1], c[0]): data[c] for c in data}, axis=1)
        return data[sorted(data.columns, key=lambda x: x[0])]  # 상품 구분 우선 시


    @property
    def multipleBand(self) -> pandas.DataFrame:
        """
        :return:
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
        """
        json = web.json(self.urls.multipleBands)
        def _get_(key: str) -> pandas.DataFrame:
            head = pandas.DataFrame(json[key])[['ID', 'NAME']].set_index(keys='ID')
            head = head.to_dict()['NAME']
            head.update({'GS_YM': '날짜', 'PRICE': '종가'})
            data = pandas.DataFrame(json['CHART']).rename(columns=head)[head.values()]
            data["날짜"] = pandas.to_datetime(data["날짜"])
            data = data.set_index(keys='날짜')
            for col in data:
                data[col] = data[col].apply(str2num)
            return data
        return pandas.concat(objs={'PER': _get_('CHART_E'), 'PBR': _get_('CHART_B')}, axis=1)


    @property
    def multiples(self) -> pandas.DataFrame:
        """
        :return:
                      EPS  EBITDAPS  CFPS    SPS    BPS  DPS보통주  DPS1우선주  배당성향    PER    PCR    PSR  ...   FCFF
            2019/12  3463      4759  4015  11173  19848       1200         NaN      35.0  18.57  16.02   5.75  ...  252.0
            2020/12  3633      5776  4300  13209  22286       1500         NaN      41.0  37.16  31.40  10.22  ...  568.0
            2021/12  6810      8492  7620  18381  27558       2500         NaN      37.0  29.12  26.02  10.79  ...  768.0
            2022/12  7503      9886  8425  21153  32511       3000         NaN      40.0  20.72  18.46   7.35  ...  784.0
            2023/3Q  5480      6204  6164  12965  35014        NaN         NaN       NaN    NaN    NaN    NaN  ...  659.0

        :columns: ['EPS', 'EBITDAPS', 'CFPS', 'SPS', 'BPS', 'DPS보통주', 'DPS1우선주', '배당성향',
                   'PER', 'PCR', 'PSR', 'PBR', 'EV/Sales', 'EV/EBITDA', '총현금흐름', '세후영업이익',
                   '유무형자산상각비', '총투자', 'FCFF']
        """
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " ", "원", ",현금", "현금%"]
        data = web.list(self.urls.invest)[3]
        data = data[~data[data.columns[0]].isin(["Per\xa0Share", "Dividends", "Multiples", "FCF"])]
        data = data.set_index(keys=[data.columns[0]])
        data = data.drop(columns=[col for col in data if not col.startswith('20')])
        data.index.name = None
        data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
        data.index = [cutString(x, cutter) for x in data.index]
        return data.T.astype(float)


    @property
    def multiplesOutstanding(self) -> pandas.Series:
        """
        :return:
            fiscalPE         2.90
            forwardPE        3.06
            sectorPE         6.17
            priceToBook      0.32
            dividendYield    9.03
            dtype: float64
        """
        src = web.html(self.urls.snapshot).find('div', id='corp_group2')
        src = [val for val in src.text.split('\n') if val]
        return pandas.Series({
            "fiscalPE": str2num(src[src.index('PER') + 1]),
            "forwardPE": str2num(src[src.index('12M PER') + 1]),
            "sectorPE": str2num(src[src.index('업종 PER') + 1]),
            "priceToBook": str2num(src[src.index('PBR') + 1]),
            "dividendYield": str2num(src[src.index('배당수익률') + 1]),
        })


    @property
    def multiplesTrailing(self) -> pandas.Series:
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
        data = web.list(self.urls.naver)[8]
        per, eps = map(str, data.columns[-1].split('l'))
        estPE, estEps = map(str, data.iloc[0, -1].split('l'))
        pbr, bps = map(str, data.iloc[1, -1].split('l'))
        return pandas.Series({
            "trailingPE": str2num(per),
            "trailingEps": str2num(eps),
            "estimatePE": str2num(estPE),
            "estimateEps": str2num(estEps),
            "priceToBook": str2num(pbr),
            "bookValue": str2num(bps),
            "dividendYield": str2num(data.iloc[-1, -1])
        })


    @property
    def products(self) -> pandas.DataFrame:
        """
        :return:
                    유가증권평가및처분이익  이자수익  수수료수익  외환거래이익  기타(계)
            기말
            2019/12                  41.49     46.58        7.53          2.65      1.75
            2020/12                  56.93     33.26        5.92          2.65      1.24
            2021/12                  50.70     36.39        7.19          2.07      3.65
            2022/12                  54.21     34.58        5.27          3.31      2.63
        """
        json = web.json(self.urls.products)
        head = pandas.DataFrame(json['chart_H'])[['ID', 'NAME']].set_index(keys='ID').to_dict()['NAME']
        head.update({'PRODUCT_DATE': '기말'})
        data = pandas.DataFrame(json['chart']).rename(columns=head).set_index(keys='기말')
        data = data.drop(columns=[c for c in data.columns if data[c].astype(float).sum() == 0])

        i = data.columns[-1]
        data['Sum'] = data.astype(float).sum(axis=1)
        data = data[(90 <= data.Sum) & (data.Sum < 110)].astype(float)
        data[i] = data[i] - (data.Sum - 100)
        return data.drop(columns=['Sum'])


    @property
    def profitRate(self) -> pandas.DataFrame:
        """
        :return:
                     매출총이익율  세전계속사업이익률  영업이익률  EBITDA마진율   ROA   ROE  ROIC
            2019/12          43.5                41.7        37.7          42.6  17.4  18.8  44.0
            2020/12          44.1                36.5        38.7          43.7  16.1  17.4  48.6
            2021/12          46.8                49.6        41.8          46.2  25.1  27.5  69.0
            2022/12          48.0                47.8        42.4          46.7  22.9  25.1  70.6
            2023/3Q          48.3                54.7        42.6          47.9  20.1  21.7  56.0
        """
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        data = web.list(self.urls.ratio)[0]
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


    @property
    def shareHolders(self) -> pandas.Series:
        """
        :return:
            최대주주등      9.13
            5%이상주주    12.02
            임원         0.04
            자기주식       0.66
            공시제외주주    78.15
            dtype: float64
        """
        data = web.data(self.urls.shares).replace("", numpy.nan)
        return pandas.Series(index=data["NM"].values, data=data["STK_RT"].values, dtype=float).dropna()

    @property
    def shareInstitutes(self) -> pandas.Series:
        data = web.list(self.urls.snapshot)[2]
        return data.replace("관련 데이터가 없습니다.", numpy.nan)


    @property
    def shortBalance(self) -> pandas.DataFrame:
        """
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
        cols = {'TRD_DT': '날짜', 'BALANCE_RT': '대차잔고비중', 'ADJ_PRC': '종가'}
        data = web.data(self.urls.shortBalance, "CHART").rename(columns=cols)[cols.values()].set_index(keys='날짜')
        data.index = pandas.to_datetime(data.index)
        return data.replace("", numpy.nan).astype(float)


    @property
    def shortSell(self) -> pandas.DataFrame:
        """
        :return:
                        공매도비중     종가
            날짜
            2022-11-28        1.37  12150.0
            2022-12-05        5.70  12800.0
            2022-12-12        1.75  12850.0
            ...                ...      ...
            2023-11-06        8.32  12570.0
            2023-11-13        0.09  12400.0
            2023-11-20        0.13  12490.0
        """
        cols = {'TRD_DT': '날짜', 'VAL': '공매도비중', 'ADJ_PRC': '종가'}
        data = web.data(self.urls.shortSell, "CHART").rename(columns=cols).set_index(keys='날짜')
        data.index = pandas.to_datetime(data.index)
        return data.replace("", numpy.nan).astype(float)


    @property
    def snapShot(self) -> pandas.Series:
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
        if not hasattr(self, '_snapshot'):
            src = web.html(self.urls.xml).find('price')
            attr = pandas.Series({
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
            self.__setattr__('_snapshot', attr)
        return self.__getattribute__('_snapshot')


    @property
    def stabilityRate(self) -> pandas.DataFrame:
        """
        :return:
                     유동비율  당좌비율  부채비율  유보율  순차입금비율  이자보상배율  자기자본비율
            2019/12     980.4     932.0       8.5  3869.6           NaN        8094.6          92.2
            2020/12    1175.7    1119.3       7.2  4357.2           NaN       12174.7          93.3
            2021/12     730.0     704.8      11.7  5411.7           NaN       17775.4          89.6
            2022/12    1036.3    1000.2       7.8  6402.1           NaN       18929.7          92.8
            2023/3Q     956.9     924.2       8.7  6902.7           NaN       11841.9          92.0
        """
        cutter = ['계산에 참여한 계정 펼치기', '(', ')', '*', '&nbsp;', ' ', " "]
        data = web.list(self.urls.ratio)[0]
        cols = data[data.columns[0]].tolist()
        data = data.iloc[cols.index('안정성비율') + 1: cols.index('성장성비율')]
        data = data.set_index(keys=[data.columns[0]])
        data = data.drop(columns=[col for col in data if not col.startswith('20')])
        data.index.name = None
        data.columns = data.columns.tolist()[:-1] + [f"{data.columns[-1][:4]}/{int(data.columns[-1][-2:]) // 3}Q"]
        data.index = [cutString(x, cutter) for x in data.index]
        return data.T.astype(float)



class etf(_price):
    def __init__(self, ticker:str):
        super().__init__(ticker=ticker)
        self.urls = urls(ticker)
        return

    @property
    def components(self) -> pandas.DataFrame:
        """
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
        data = get_etf_portfolio_deposit_file(self.ticker)
        data['이름'] = metaData[metaData.index.isin(data.index)]['korName']
        return data[['이름', '비중']]

    @property
    def currentPrice(self) -> int or float:
        if not hasattr(self, '_curprc'):
            html = web.html(self.urls.naver)
            curr = [d.text for d in html.find_all("dd") if d.text.startswith("현재가")][0]
            self.__setattr__('_curprc', str2num(curr[curr.index("현재가 ") + 4: curr.index(" 전일대비")]))
        return self.__getattribute__('_curprc')

    @property
    def multiples(self) -> pandas.Series:
        """
        :return:
            dividendYield     1.68
            fiscalPE         12.58
            priceToBook       1.15
            dtype: float64
        """
        html = web.html(self.urls.etf)
        script = html.find_all('script')[-1].text.split('\n')
        pe = script[[n for n, h in enumerate(script) if "PER" in h][0] + 1]
        pb = script[[n for n, h in enumerate(script) if "PBR" in h][0] + 1]
        return pandas.Series({
            "dividendYield": str2num(html.find_all('td', class_='r cle')[-1].text),
            "fiscalPE" : str2num(pe[pe.index(":"): ]),
            "priceToBook": str2num(pb[pb.index(":"):])
        })

    @property
    def sectorWeights(self) -> pandas.DataFrame:
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
        n, base = 100, ""
        src = str(web.html(self.urls.etf)).split('\r\n')
        while n < len(src):
            if 'etf1StockInfoData' in src[n]:
                while not "];" in src[n + 1]:
                    base += src[n + 1]
                    n += 1
                break
            n += 1
        data = pandas.DataFrame(data=eval(base)).drop(columns=['val05'])
        data.columns = numpy.array(["섹터", metaData.loc[self.ticker, 'name'], "유사펀드", "시장"])
        return data.set_index(keys='섹터')

    @property
    def snapShot(self) -> pandas.Series:
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
        if not hasattr(self, '_snapshot'):
            src = web.html(self.urls.xml).find('price')
            attr = pandas.Series({
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
            self.__setattr__('_snapshot', attr)
        return self.__getattribute__('_snapshot')






if __name__ == "__main__":
    pandas.set_option('display.expand_frame_repr', False)

    myStock = stock(
        # '316140' # 우리금융지주
        # '051910'  # LG 화학
        # '058470'  # 리노공업
        # "323280" # 태성
        "359090"  # C&R Research
    )
    # print(myStock.price)
    # print(myStock.abstract)
    # print(myStock.analogy)
    # print(myStock.benchmarkMultiples)
    # print(myStock.businessSummary)
    # print(myStock.cashFlow)
    # print(myStock.consensusOutstanding)
    # print(myStock.consensusPrice)
    # print(myStock.consensusProfit)
    # print(myStock.consensusTendency)
    # print(myStock.currentPrice)
    # print(myStock.expenses)
    # print(myStock.financialStatement)
    # print(myStock.financialStatementSeparate)
    # print(myStock.foreignRate)
    # print(myStock.growthRate)
    # print(myStock.incomeStatement)
    # print(myStock.marketCap)
    # print(myStock.marketShares)
    print(myStock.multipleBand)
    # print(myStock.multiples)
    # print(myStock.multiplesOutstanding)
    # print(myStock.multiplesTrailing)
    # print(myStock.products)
    # print(myStock.profitRate)
    # print(myStock.shareHolders)
    # print(myStock.shareInstitutes)
    # print(myStock.shortBalance)
    # print(myStock.shortSell)
    # print(myStock.snapShot)
    # print(myStock.stabilityRate)

    myEtf = etf(
        # '102780' # KODEX 삼성그룹
        '114800' # KODEX 인버스
    )
    # print(myEtf.price)
    # print(myEtf.etfMultiples)
    # print(myEtf.etfComponents)
    # print(myEtf.etfSectors)