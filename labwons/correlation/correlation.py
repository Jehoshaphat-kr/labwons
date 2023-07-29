from typing import Union
from labwons.equity.equity import Equity
from labwons.indicator.indicator import Indicator
import pandas as pd



class Correlation(pd.DataFrame):
    def __init__(
        self,
        d1:Union[Equity, Indicator],
        d2:Union[Equity, Indicator],
        d1property:str='ohlc',
        d2property:str=''
    ):


        super().__init__()
        return