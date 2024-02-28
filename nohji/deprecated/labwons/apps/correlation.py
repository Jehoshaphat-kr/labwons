from typing import Union
from nohji.deprecated.labwons.equity import Equity
from labwons.indicator import Indicator
import pandas as pd



class Correlation(pd.DataFrame):
    def __init__(
        self,
        d1:Union[Equity, Indicator],
        d2:Union[Equity, Indicator],
    ):
        if isinstance(d1, Equity):
            d1frame = d1.ohlcv[['open', 'high', 'low', 'close']]
            d1series = d1.typical


        super().__init__()
        return