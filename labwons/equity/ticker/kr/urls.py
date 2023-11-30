from labwons.common.web import web


class urls(object):
    def __init__(self, ticker:str):
        self.ticker = ticker
        return

    def __call__(self, code:str, GB:str, menuID:str, stkGb:str) -> str:
        return self._url_(code, GB, menuID, stkGb)

    def _url_(self, code:str, GB:str, menuID:str, stkGb:str):
        return f"http://comp.fnguide.com/SVO2/ASP/{code}.asp?" \
               f"pGB=1&" \
               f"gicode=A{self.ticker}&" \
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
        return self._url_("SVD_Corp", self.gb, "102", "701")

    @property
    def finance(self) -> str:
        """
        "재무제표" 탭
        :return:
        """
        return self._url_("SVD_Finance", self.gb, "103", "701")

    @property
    def separateFinance(self) -> str:
        """
        "재무제표" 탭 (별도)
        :return:
        """
        return self._url_("SVD_Finance", 'A', "103", "701")

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
        return f"http://cdn.fnguide.com/SVO2/xml/Snapshot_all/{self.ticker}.xml"

    @property
    def products(self) -> str:
        """
        "cdn" 연간 생산 상품 종류
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2//json/chart/02/chart_A{self.ticker}_01_N.json"

    @property
    def multipleBands(self) -> str:
        """
        "cdn" PER / PBR 밴드
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_06/chart_A{self.ticker}_D.json"

    @property
    def expenses(self) -> str:
        """
        "cdn" 판관비 / 매출원가
        :return:
        """
        return f"https://cdn.fnguide.com/SVO2/json/chart/02/chart_A{self.ticker}_D.json"

    @property
    def consensusAnnualProfit(self) -> str:
        """
        "cdn" 연간 실적 전망 (매출, 영업이익)
        :return:
        """
        return f"https://cdn.fnguide.com/SVO2/json/chart/07_01/chart_A{self.ticker}_{self.gb}_A.json"

    @property
    def consensusQuarterProfit(self) -> str:
        """
        "cdn" 분기 실적 전망 (매출, 영업이익)
        :return:
        """
        return f"https://cdn.fnguide.com/SVO2/json/chart/07_01/chart_A{self.ticker}_{self.gb}_Q.json"

    @property
    def consensusPrice(self) -> str:
        """
        "cdn" 주가 컨센서스 : 1년
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_02/chart_A{self.ticker}.json"

    @property
    def consensusForward1Y(self) -> str:
        """
        "cdn" 1년 또는 당해 선행
        :return:
        """
        return f"https://cdn.fnguide.com/SVO2/json/chart/07_02/chart_A{self.ticker}_{self.gb}_FY1.json"

    @property
    def consensusForward2Y(self) -> str:
        """
        "cdn" 2년 또는 다음 해 선행
        :return:
        """
        return f"https://cdn.fnguide.com/SVO2/json/chart/07_02/chart_A{self.ticker}_{self.gb}_FY2.json"

    @property
    def foreignRate3M(self) -> str:
        """
        "cdn" 외국인 소진율 : 3개월
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_01/chart_A{self.ticker}_3M.json"

    @property
    def foreignRate1Y(self) -> str:
        """
        "cdn" 외국인 소진율 : 1년
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_01/chart_A{self.ticker}_1Y.json"

    @property
    def foreignRate3Y(self) -> str:
        """
        "cdn" 외국인 소진율 : 3년
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_01/chart_A{self.ticker}_3Y.json"

    @property
    def benchmarkMultiples(self) -> str:
        """
        "cdn" 벤치마크 배수 비교
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/01_04/chart_A{self.ticker}_{self.gb}.json"

    @property
    def shortSell(self) -> str:
        """
        "cdn" 차입 공매도 비중
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/11_01/chart_A{self.ticker}_SELL1Y.json"

    @property
    def shortBalance(self) -> str:
        """
        "cdn" 대차잔고 비중
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/json/chart/11_01/chart_A{self.ticker}_BALANCE1Y.json"

    @property
    def naver(self) -> str:
        """
        "네이버" 증권
        :return:
        """
        return  f"https://finance.naver.com/item/main.naver?code={self.ticker}"

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
        연결 또는 별도 여부
        :return: [str] "D": 연결 / "B": 별도
        """
        if not hasattr(self, '_gb'):
            tbs = web.list(self.snapshot)
            self.__setattr__('_gb', "B" if tbs[11].iloc[1].isnull().sum() > tbs[14].iloc[1].isnull().sum() else "D")
        return self.__getattribute__('_gb')