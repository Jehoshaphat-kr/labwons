from typing import Union
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests, json, pandas


class urls(object):
    def __init__(self, ticker:str):
        self.t = ticker

        #
        return

    def __call__(self, code:str, GB:str, menuID:str, stkGb:str) -> str:
        return self._url_(code, GB, menuID, stkGb)

    def _url_(self, code:str, GB:str, menuID:str, stkGb:str):
        return f"http://comp.fnguide.com/SVO2/ASP/{code}.asp?" \
               f"pGB=1&" \
               f"gicode=A{self.t}&" \
               f"cID=&" \
               f"MenuYn=Y" \
               f"&ReportGB={GB}" \
               f"&NewMenuID={menuID}" \
               f"&stkGb={stkGb}"

    @property
    def snapshot(self) -> str:
        """
        "Snapshot" 탭
        :return:
        """
        return self._url_("SVD_Main", "", 'Y', "701")

    @property
    def corp(self) -> str:
        """
        "기업개요" 탭
        :return:
        """
        return self._url_("SVD_Corp", "", "102", "701")

    @property
    def finance(self) -> str:
        """
        "재무제표" 탭
        :return:
        """
        return self._url_("SVD_Finance", self.gb, "103", "701")

    @property
    def ratio(self) -> str:
        """
        "재무비율" 탭
        :return:
        """
        return self._url_("SVD_FinanceRatio", self.gb, "104", "701")

    @property
    def invest(self) -> str:
        """
        "투자지표" 탭
        :return:
        """
        return self._url_("SVD_Invest", "", "105", "701")

    @property
    def xml(self) -> str:
        """
        공통 xml
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/xml/Snapshot_all/{self.t}.xml"

    @property
    def products(self) -> str:
        """
        "cdn" 연간 생산 상품 종류
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2//json/chart/02/chart_A{self.t}_01_N.json"

    @property
    def multipleBands(self) -> str:
        """
        "cdn" PER / PBR 밴드
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_06/chart_A{self.t}_D.json"

    @property
    def consensusAnnualProfit(self) -> str:
        """
        "cdn" 연간 실적 전망 (매출, 영업이익)
        :return:
        """
        return f"https://cdn.fnguide.com/SVO2/json/chart/07_01/chart_A{self.t}_{self.gb}_A.json"

    @property
    def consensusQuarterProfit(self) -> str:
        """
        "cdn" 분기 실적 전망 (매출, 영업이익)
        :return:
        """
        return f"https://cdn.fnguide.com/SVO2/json/chart/07_01/chart_A{self.t}_{self.gb}_Q.json"

    @property
    def consensusPrice(self) -> str:
        """
        "cdn" 주가 컨센서스 : 1년
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_02/chart_A{self.t}.json"

    @property
    def foreignRate3M(self) -> str:
        """
        "cdn" 외국인 소진율 : 3개월
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_01/chart_A{self.t}_3M.json"

    @property
    def foreignRate1Y(self) -> str:
        """
        "cdn" 외국인 소진율 : 1년
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_01/chart_A{self.t}_1Y.json"

    @property
    def foreignRate3Y(self) -> str:
        """
        "cdn" 외국인 소진율 : 3년
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_01/chart_A{self.t}_3Y.json"

    @property
    def benchmarkMultiples(self) -> str:
        """
        "cdn" 벤치마크 배수 비교
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_04/chart_A{self.t}_{self.gb}.json"

    @property
    def shortSell(self) -> str:
        """
        "cdn" 차입 공매도 비중
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/11_01/chart_A{self.t}_SELL1Y.json"

    @property
    def shortBalance(self) -> str:
        """
        "cdn" 대차잔고 비중
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/11_01/chart_A{self.t}_BALANCE1Y.json"

    @property
    def etf(self) -> str:
        """
        "ETF Snapshot" 탭
        :return:
        """
        return self._url_("ETF_Snapshot", "", "401", "770")

    @property
    def gb(self) -> str:
        """
        연결 또는 별도 기업 여부
        :return: [str] "D": 연결 / "B": 별도
        """
        if not hasattr(self, '_gb'):
            tbs = self.req(self.snapshot, 'list')
            self.__setattr__('_gb', "B" if tbs[11].iloc[1].isnull().sum() > tbs[14].iloc[1].isnull().sum() else "D")
        return self.__getattribute__('_gb')

    def req(self, url:str, by:str, **kwargs) -> Union[list, pandas.DataFrame, BeautifulSoup]:
        attr = f"_{url}_{by}"
        if not hasattr(self, attr):
            if by == 'list':
                self.__setattr__(attr, pandas.read_html(io=url, header=0))
            elif by == 'json' or by == 'dataframe':
                self.__setattr__(attr, json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace')))
            elif by == 'scrap':
                resp = requests.get(url)
                if resp.status_code == 200:
                    self.__setattr__(attr, BeautifulSoup(resp.content, 'xml' if url.endswith('.xml') else 'lxml'))
                else:
                    raise ConnectionError
            else:
                raise KeyError
            if by == 'dataframe':
                kv = kwargs['key'] if 'key' in kwargs else 'CHART'
                self.__setattr__(attr, pandas.DataFrame(self.__getattribute__(attr)[kv]))
        return self.__getattribute__(attr)

    # def reqTables(self, url:str) -> list:
    #     """
    #     url에 대한 html table의 [pandas.DataFrame] list
    #     :param url: [str]
    #     :return:
    #     """
    #     if not hasattr(self, f'_{url}_tables'):
    #         self.__setattr__(f'_{url}_tables', pandas.read_html(io=url, header=0))
    #     return self.__getattribute__(f'_{url}_tables')
    #
    # def reqXml(self) -> BeautifulSoup:
    #     """
    #     공통 xml의 스크래퍼 응답
    #     :return: [BeatifulSoup]
    #     """
    #     if not hasattr(self, '_basis'):
    #         response = requests.get(url=)
    #         if response.status_code == 200:
    #             self.__setattr__('_basis', BeautifulSoup(response.content, 'xml'))
    #         else:
    #             raise ConnectionError
    #     return self.__getattribute__('_basis')
    #
    # def reqSnapshot(self) -> BeautifulSoup:
    #     """
    #     "Snapshot" 탭의 스크래퍼 응답
    #     :return: [BeautifulSoup]
    #     """
    #     if not hasattr(self, '_ssnap'):
    #         response = requests.get(url=self.snapshot)
    #         if response.status_code == 200:
    #             self.__setattr__('_ssnap', BeautifulSoup(response.content, 'lxml'))
    #         else:
    #             raise ConnectionError
    #     return self.__getattribute__('_ssnap')
    #
    # def reqEtfSnapshot(self) -> BeautifulSoup:
    #     """
    #     "ETF_Snapshot" 탭의 스크래퍼 응답
    #     :return: [BeautifulSoup]
    #     """
    #     if not hasattr(self, '_esnap'):
    #         response = requests.get(url=self.etf)
    #         if response.status_code == 200:
    #             self.__setattr__('_esnap', BeautifulSoup(response.content, 'lxml'))
    #         else:
    #             raise ConnectionError
    #     return self.__getattribute__('_esnap')