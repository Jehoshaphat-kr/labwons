from datetime import datetime, timedelta
from bs4 import BeautifulSoup as Soup
from pykrx.stock import get_market_cap_by_date
from urllib.request import urlopen
import pandas as pd
import requests, json


class fnguide(object):

    def __init__(self, ticker:str):
        self._t = ticker
        self._u = f"http://comp.fnguide.com/SVO2/ASP/SVD_%s.asp?" \
                  f"pGB=1&" \
                  f"gicode=A{ticker}&" \
                  f"cID=&" \
                  f"MenuYn=Y&" \
                  f"ReportGB=%s&" \
                  f"NewMenuID=%s&" \
                  f"stkGb=701"
        return

    def __url__(self, page:str, hold:str='') -> str:
        """
        :param page : [str]
        :param hold : [str] 연결 - "D" 또는 "" / 별도 - "B"
        :return:
        """
        pages = {
            "Main": {
                "ReportGB": "",
                "NewMenuID": "Y"
            },
            "Corp": {
                "ReportGB": "",
                "NewMenuID": "102"
            },
            "Finance": {
                "ReportGB": hold,
                "NewMenuID": "103"
            },
            "FinanceRatio": {
                "ReportGB": hold,
                "NewMenuID": "104"
            },
            "Invest": {
                "ReportGB": "",
                "NewMenuID": "105"
            },
        }
        if not page in pages or not hold in ['', 'D', 'B']:
            raise KeyError
        return self._u % (page, pages[page]["ReportGB"], pages[page]["NewMenuID"])

    def __html__(self, page:str, hold:str='') -> list:
        if not hasattr(self, f"_u{page}{hold}"):
            self.__setattr__(f'_u{page}{hold}', pd.read_html(self.__url__(page, hold), header=0))
        return self.__getattribute__(f'_u{page}{hold}')

    def __hold__(self) -> str:
        if not hasattr(self, f"_hold"):
            html = self.__html__('Main')
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
        html = Soup(requests.get(self.__url__('Main')).content, 'lxml').find('ul', id='bizSummaryContent').find_all('li')
        t = '\n\n '.join([e.text for e in html])
        w = [
            '.\n' if t[n] == '.' and not any([t[n - 1].isdigit(), t[n + 1].isdigit(), t[n + 1].isalpha()]) else t[n]
            for n in range(1, len(t) - 2)
        ]
        s = ' ' + t[0] + ''.join(w) + t[-2] + t[-1]
        return s.replace(' ', '').replace('\xa0\xa0', ' ').replace('\xa0', ' ').replace('\n ', '\n')

    @property
    def annualOverview(self) -> pd.DataFrame:
        return self._overview(self.__html__('Main')[11] if self.__hold__() == 'D' else self.__html__('Main')[14])

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
        html = self.__html__('Corp')
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
        data = self.__html__('Corp')[10 if self.__hold__() == 'D' else 11]
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
        data = self.__html__('Corp')[12]
        data = data.set_index(keys=[data.columns[0]])
        data.index.name = None
        return data.T

    @property
    def annualProfitLoss(self) -> pd.DataFrame:
        return self._finance(self.__html__('Finance', self.__hold__())[0])

    @property
    def annualAsset(self) -> pd.DataFrame:
        return self._finance(self.__html__('Finance', self.__hold__())[2])

    @property
    def annualCashFlow(self) -> pd.DataFrame:
        return self._finance(self.__html__('Finance', self.__hold__())[4])

    @property
    def annualGrowthRate(self) -> pd.DataFrame:
        data = self.__html__('FinanceRatio', self.__hold__())[0]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('성장성비율') + 1 : index.index('수익성비율')])
    
    @property
    def annualProfitRate(self) -> pd.DataFrame:
        data = self.__html__('FinanceRatio', self.__hold__())[0]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('수익성비율') + 1: index.index('활동성비율')])

    @property
    def annualMultiples(self) -> pd.DataFrame:
        data = self.__html__('Invest', self.__hold__())[3]
        data = data[~data[data.columns[0]].isin(["Per\xa0Share", "Dividends", "Multiples", "FCF"])]
        return self._finance(data)

    @property
    def quarterOverview(self) -> pd.DataFrame:
        return self._overview(self.__html__('Main')[12] if self.__hold__() == 'D' else self.__html__('Main')[15])

    @property
    def quarterProfitLoss(self) -> pd.DataFrame:
        return self._finance(self.__html__('Finance', self.__hold__())[1])

    @property
    def quarterAsset(self) -> pd.DataFrame:
        return self._finance(self.__html__('Finance', self.__hold__())[3])

    @property
    def quarterCashFlow(self) -> pd.DataFrame:
        return self._finance(self.__html__('Finance', self.__hold__())[5])

    @property
    def quarterGrowthRate(self) -> pd.DataFrame:
        data = self.__html__('FinanceRatio', self.__hold__())[1]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('성장성비율') + 1: index.index('수익성비율')])

    @property
    def quarterProfitRate(self) -> pd.DataFrame:
        data = self.__html__('FinanceRatio', self.__hold__())[1]
        index = data[data.columns[0]].tolist()
        return self._finance(data.iloc[index.index('수익성비율') + 1: ])




if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)
    # ticker = '000660' # SK하이닉스
    # ticker = '003800' # 에이스침대
    ticker = '058470' # 리노공업

    guide = fnguide(ticker)
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
    print(guide.annualMultiples)
    # print(guide.quarterOverview)
    # print(guide.quarterProfitLoss)
    # print(guide.quarterAsset)
    # print(guide.quarterCashFlow)
    # print(guide.quarterGrowthRate)
    # print(guide.quarterProfitRate)
