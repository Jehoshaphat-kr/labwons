from labwons.common.basis import baseDataFrameChart, baseSeriesChart
from labwons.equity.ticker import _ticker
from labwons.equity.technical.ohlcv import ohlcv
from pykrx.stock import get_market_ohlcv_by_date
from datetime import datetime, timedelta
from pytz import timezone
from ta import add_all_ta_features
import pandas as pd
import yfinance as yf
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


class _ohlcv(_ticker):

    def __init__(self, ticker:str, **kwargs):
        super().__init__(ticker=ticker, **kwargs)

        self._period = kwargs['period'] if 'period' in kwargs else 10
        self._today = datetime.now(timezone('Asia/Seoul')).strftime("%Y%m%d")
        self._freq = kwargs['freq'] if 'freq' in kwargs else 'd' if self.market == 'KOR' else '1d'
        self._ddate = self._today
        if 'enddate' in kwargs:
            self._ddate = kwargs['enddate']
        if isinstance(self._ddate, str):
            self._ddate = datetime.strptime(self._ddate, "%Y%m%d")
        self._attr = lambda x: f"_{x}_{self._period}_{self._ddate}_{self._freq}_"
        return

    @staticmethod
    def fetchKrse(ticker: str = '', startdate: str = '', enddate: str = '', freq: str = '') -> pd.DataFrame:
        ohlcv = get_market_ohlcv_by_date(
            fromdate=startdate,
            todate=enddate,
            ticker=ticker,
            freq=freq
        )
        ohlcv = ohlcv.rename(columns=dict(시가='open', 고가='high', 저가='low', 종가='close', 거래량='volume'))

        trade_stop = ohlcv[ohlcv.open == 0].copy()
        if not trade_stop.empty:
            ohlcv.loc[trade_stop.index, ['open', 'high', 'low']] = trade_stop['close']
        ohlcv.index.name = 'date'
        return ohlcv

    @staticmethod
    def fetchNyse(ticker: str, period: int, freq: str) -> pd.DataFrame:
        columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        ohlcv = yf.Ticker(ticker).history(period=f'{period}y', interval=freq)[columns]
        ohlcv = ohlcv.rename(columns=dict(zip(columns, [n.lower() for n in columns])))
        ohlcv['date'] = pd.to_datetime(ohlcv.index)
        ohlcv['date'] = ohlcv['date'].dt.tz_convert('Asia/Seoul')
        # ohlcv['date'] = ohlcv['date'].tz_localize(timezone('Asia/Seoul'))
        ohlcv.index = ohlcv['date'].dt.date
        return ohlcv.drop(columns=['date'])

    @property
    def enddate(self) -> str:
        return self._ddate.strftime("%Y%m%d")

    @enddate.setter
    def enddate(self, enddate:str or datetime):
        if not enddate:
            self._ddate = datetime.strptime(self._today, "%Y%m%d")
        else:
            self._ddate = datetime.strptime(enddate, "%Y%m%d") if isinstance(enddate, str) else enddate

    @property
    def startdate(self) -> str:
        return (self._ddate - timedelta(365 * self.period)).strftime("%Y%m%d")

    @property
    def period(self) -> int:
        return self._period

    @period.setter
    def period(self, period:int):
        self._period = period

    @property
    def freq(self) -> str:
        return self._freq

    @freq.setter
    def freq(self, freq:str):
        if (self.market == 'KOR' and not freq in ['d', 'm', 'y']) or \
           (self.market == 'USA' and not freq in ['30m', '60m', '1h', '1d', '5d', '1wk', '1mo', '3mo']):
            raise KeyError(f"Frequency key error for market: {self.market}: {freq}")
        self._freq = freq

    @property
    def ohlcv(self) -> ohlcv:
        if not hasattr(self, self._attr('ohlcv')):
            if self.market == 'KOR':
                fetch = self.fetchKrse(self.ticker, self.startdate, self._today, self.freq)
            elif self.market == 'USA':
                fetch = self.fetchNyse(self.ticker, self.period, self.freq)
            else:
                raise AttributeError(f"Unknown Market: {self.market}({self.exchange}) is an invalid attribute.")
            fetch.index = pd.to_datetime(fetch.index)
            fetch = fetch[fetch.index <= self._ddate]
            self.__setattr__(self._attr('ohlcv'), ohlcv(fetch, **self._valid_prop))
        return self.__getattribute__(self._attr('ohlcv'))

    @property
    def ta(self) -> baseDataFrameChart:
        """
        Technical Analysis
        volume          volatility        trend                       momentum               others
        -------------   ---------------   -------------------------   --------------------   --------
        volume_adi      volatility_bbm    trend_macd                  momentum_rsi           others_dr
        volume_obv      volatility_bbh    trend_macd_signal           momentum_stoch_rsi     others_dlr
        volume_cmf      volatility_bbl    trend_macd_diff             momentum_stoch_rsi_k   others_cr
        volume_fi       volatility_bbw    trend_sma_fast              momentum_stoch_rsi_d
        volume_em       volatility_bbp    trend_sma_slow              momentum_tsi
        volume_sma_em   volatility_bbhi   trend_ema_fast              momentum_uo
        volume_vpt      volatility_bbli   trend_ema_slow              momentum_stoch
        volume_vwap     volatility_kcc    trend_vortex_ind_pos        momentum_stoch_signal
        volume_mfi      volatility_kch    trend_vortex_ind_neg        momentum_wr
        volume_nvi      volatility_kcl    trend_vortex_ind_diff       momentum_ao
                        volatility_kcw    trend_trix                  momentum_roc
                        volatility_kcp    trend_mass_index            momentum_ppo
                        volatility_kchi   trend_dpo                   momentum_ppo_signal
                        volatility_kcli   trend_kst                   momentum_ppo_hist
                        volatility_dcl    trend_kst_sig               momentum_pvo
                        volatility_dch    trend_kst_diff              momentum_pvo_signal
                        volatility_dcm    trend_ichimoku_conv         momentum_pvo_hist
                        volatility_dcw    trend_ichimoku_base         momentum_kama
                        volatility_dcp    trend_ichimoku_a
                        volatility_atr    trend_ichimoku_b
                        volatility_ui     trend_stc
                                          trend_adx
                                          trend_adx_pos
                                          trend_adx_neg
                                          trend_cci
                                          trend_visual_ichimoku_a
                                          trend_visual_ichimoku_b
                                          trend_aroon_up
                                          trend_aroon_down
                                          trend_aroon_ind
                                          trend_psar_up
                                          trend_psar_down
                                          trend_psar_up_indicator
                                          trend_psar_down_indicator
        """
        if not hasattr(self, self._attr('ta')):
            self.__setattr__(
                self._attr('ta'),
                baseDataFrameChart(
                    add_all_ta_features(self.ohlcv.copy(), 'open', 'high', 'low', 'close', 'volume'),
                    **self._valid_prop
                )
            )
        return self.__getattribute__(self._attr('ta'))



if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)
    API_ECOS = "CEW3KQU603E6GA8VX0O9"

    # test = _ohlcv(ticker='383310')
    test = _ohlcv(ticker='AAPL', period=12, enddate='20230105')
    # test = _fetch(ticker='TSLA')
    # test = _fetch(ticker='KRE')
    # test = _fetch(ticker='DGS10')
    # test = _fetch(ticker="151Y003", ecoskeys=["예금은행", "전국"])
    # test = _fetch(ticker="121Y002", ecoskeys=["저축성수신"], name='평균수신')
    # test = _fetch(ticker='LORSGPRT', market='KOR')
    # print(test.ticker)
    # print(test.exchange)
    print(test.ohlcv)
    print(len(test.ohlcv))
    # test.ohlcv.show()
    # print(test.typical)
    # test.typical.show()
    # print(test.close)
    # test.close.show()
    # print(test.ta)


