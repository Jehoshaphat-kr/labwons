from nohji.meta import meta

from datetime import datetime, timedelta
from pandas import (
    DataFrame,
    concat,
    to_datetime,
    read_html
)
from pykrx.stock import (
    get_nearest_business_day_in_a_week,
    get_market_cap_by_ticker,
    get_market_fundamental
)


class _TreeData:

    _tradingDates:DataFrame = DataFrame()
    _marketCap:DataFrame = DataFrame()
    _multiples:DataFrame = DataFrame()
    _ipo:DataFrame = DataFrame()
    _shares:DataFrame = DataFrame()
    def __init__(self):
        self._td_ = get_nearest_business_day_in_a_week(datetime.today().strftime("%Y%m%d"))
        return

    @property
    def dates(self) -> DataFrame:
        if self._tradingDates.empty:
            self._tradingDates.index = [
                "recent",
                "1Day",
                "1Week",
                "1Month",
                "3Month",
                "6Month",
                "1Year"
            ]
            _recent = datetime.strptime(self._td_, "%Y%m%d")
            self._tradingDates["datetime"] = [_recent] + [_recent - timedelta(d) for d in  [1, 7, 30, 91, 183, 365]]

        return self._tradingDates

    @property
    def marketCap(self) -> DataFrame:
        if self._marketCap.empty:
            columns = {
                "종가": "close",
                "시가총액": "marketCap",
                "거래량": "volume"
            }
            self._marketCap = get_market_cap_by_ticker(date=self._td_, market="ALL", alternative=True).drop_duplicates()
            self._marketCap = self._marketCap.rename(columns=columns)
            self._marketCap = self._marketCap[columns.values()]
        return self._marketCap

    @property
    def multiples(self) -> DataFrame:
        if self._multiples.empty:
            self._multiples = get_market_fundamental(date=self._td_, market="ALL", alternative=True).drop_duplicates()
        return self._multiples

    @property
    def initialPublicOffer(self) -> DataFrame:
        if self._ipo.empty:
            columns = {
                '회사명': '종목명',
                '종목코드': 'ticker',
                '상장일': 'ipo'
            }
            self._ipo = read_html(
                io='http://kind.krx.co.kr/corpgeneral/corpList.do?method=download',
                header=0,
                encoding='euc-kr'
            )[0][list(columns.keys())]
            self._ipo = self._ipo.rename(columns=columns).set_index(keys='ticker')
            self._ipo.index = self._ipo.index.astype(str).str.zfill(6)
            self._ipo['ipo'] = to_datetime(self._ipo['ipo'])
            self._ipo = self._ipo[self._ipo['ipo'] <= datetime.strptime(self._td_, "%Y%m%d")].drop_duplicates()
        return self._ipo

    # @property
    # def shares(self) -> DataFrame:
    #     if self._shares.empty:
    #
    #         self._shares = concat(
    #             objs={
    #                 self._td_: get_market_cap_by_ticker(date=self.dates['1Y'], market='ALL')['상장주식수'],
    #             'curr': get_market_cap_by_ticker(date=self.dates['0D'], market='ALL')['상장주식수']
    #         }, axis=1)

if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    treeData = _TreeData()
    # print(treeData.marketCap)
    # print(treeData.multiples)
    print(treeData.initialPublicOffer)