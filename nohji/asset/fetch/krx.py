from nohji.meta import meta
from nohji.asset.core.decorator import common, stockonly, etfonly

from datetime import datetime, timedelta
from pandas import Series, DataFrame
from pykrx.stock import get_market_ohlcv_by_date, get_market_cap_by_date, get_etf_portfolio_deposit_file


class krx:
    """
    Fetch source data from krx (through <package; pykrx>)

    @ohlcv
        constraint  : common
        type        : DataFrame
        description : stock price (open, high, low, close) and volume
        columns     : ["open", "high", "low", "close", "volume"]
        example     :
                         open   high    low  close    volume
            date
            2013-12-13  28200  28220  27800  27800    201065
            2013-12-16  27820  28080  27660  28000    179088
            2013-12-17  28340  28340  27860  27900    155248
            ...           ...    ...    ...    ...       ...
            2023-12-07  71800  71900  71100  71500   8862017
            2023-12-08  72100  72800  71900  72600  10859463
            2023-12-11  72800  73000  72200  73000   9406504

    @quarterlyMarketCap
        constraint  : stock only
        type        : Series
        description : quarterly market cap
        example     :
              month
            2019/03     93522
            2019/06     95563
            2019/09     89922
                ...       ...
            2023/03     83071
            2023/06     85838
            2023/09     93241
            2023/11     95497
            Name: marketCap, dtype: int32

    @components
        constraint  : etf only
        type        : Series
        description : etf components by weight
        example     :
                               이름   비중
            티커
            005930         삼성전자  31.24
            000660       SK하이닉스   6.72
            068270         셀트리온   2.88
            005490      POSCO홀딩스   2.86
            035420            NAVER   2.51
            ...                 ...    ...
            271940   일진하이솔루스   0.03
            105630         한세실업   0.02
            280360       롯데웰푸드   0.02
            300720       한일시멘트   0.02
            014820     동원시스템즈   0.02
    """

    def __init__(self, ticker:str, period:int=10, freq:str="d"):
        self.ticker = ticker
        self.period = period
        self.freq = freq
        return

    @common
    def ohlcv(self) -> DataFrame:
        todate = datetime.today().strftime("%Y%m%d")
        frdate = (datetime.today() - timedelta(365 * self.period)).strftime("%Y%m%d")
        ohlcv = get_market_ohlcv_by_date(
            fromdate=frdate,
            todate=todate,
            ticker=self.ticker,
            freq=self.freq
        )

        trade_stop = ohlcv[ohlcv.시가 == 0].copy()
        if not trade_stop.empty:
            ohlcv.loc[trade_stop.index, ['시가', '고가', '저가']] = trade_stop.종가
        ohlcv.index.name = 'date'
        return ohlcv.rename(columns=dict(시가='open', 고가='high', 저가='low', 종가='close', 거래량='volume'))

    @stockonly
    def marketCap(self) -> Series:
        cap = get_market_cap_by_date(
            fromdate=(datetime.today() - timedelta(365 * 8)).strftime("%Y%m%d"),
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
        cap.index.name = "month"
        return Series(index=cap.index, data=cap['시가총액'] / 100000000, dtype=int)

    @etfonly
    def components(self) -> DataFrame:
        data = get_etf_portfolio_deposit_file(self.ticker)
        data['이름'] = meta[meta.index.isin(data.index)]['korName']
        data = data[['이름', '비중']]
        return data[~data["이름"].isna()]



if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    krx = krx(
        "005930"
        # "069500"
    )
    # print(krx.ohlcv)
    print(krx.marketCap)
    # print(krx.components)
