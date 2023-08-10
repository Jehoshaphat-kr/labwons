from labwons.common.basis import baseDataFrameChart
from labwons.equity.technical.ohlcv import ohlcv
import pandas as pd
import numpy as np


class backtest(baseDataFrameChart):
    def __init__(self, ohlcvt:ohlcv, **kwargs):
        def perform(window:np.array):
            return round(100 * (window[-1] / window[0] - 1), 2)
        def mx(window:pd.Series):
            return round(100 * (ohlcvt.loc[window.index]['high'].max() / window[0] - 1), 2)
        objs = {'close': ohlcvt.c}
        for label, win in [('1M', 21), ('3M', 63), ('6M', 126), ('1Y', 252)]:
            objs[f'R{label}'] = ohlcvt['close'].rolling(window=win).apply(perform, raw=True).shift(-win + 1)
        for label, win in [('1M', 21), ('3M', 63), ('6M', 126), ('1Y', 252)]:
            objs[f'MX{label}'] = ohlcvt['close'].rolling(window=win).apply(mx, raw=False).shift(-win + 1)
        frame = pd.concat(objs=objs, axis=1)

        # span = ohlcv_ans[['시가', '고가', '저가', '종가']].values.flatten()
        # returns = [round(100 * (p / span[0] - 1), 2) for p in span]
        # ohlcv_ans['최대'] = max(returns)
        # ohlcv_ans['최소'] = min(returns)
        # return ohlcv_ans[columns]
        super(backtest, self).__init__(frame, **kwargs)