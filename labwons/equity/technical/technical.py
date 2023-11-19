from labwons.equity.technical._ohlcv import ohlcv
from ta import add_all_ta_features
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


class technical(object):
    def __init__(self, ohlcv:pd.DataFrame, ticker:str, name:str, path:str, language:str):
        self.ticker = ticker
        self._name = name
        self._path = path
        self.language = language
        self._ohlcv = ohlcv
        if language == "kor":
            ohlcv = ohlcv.rename(
                columns={"시가":"open", "고가":"high", "저가":"low", "종가":"close", "거래량":"volume"}
            )
        # self.typicalPrice = self.TP = (ohlcv["high"] + ohlcv["low"] + ohlcv["close"]) / 3
        # self.TA = add_all_ta_features(ohlcv, 'open', 'high', 'low', 'close', 'volume')
        return

    @property
    def ohlcvt(self) -> ohlcv:
        return ohlcv(self._ohlcv, self.ticker, self._name, self._path, self.language)