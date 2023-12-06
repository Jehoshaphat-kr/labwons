from labwons.common.metadata import metaData
from labwons.equity.ticker.us import fetch
from typing import Union
import pandas, numpy


class Ticker(object):

    def __init__(self, ticker:str, **kwargs):
        R = fetch.equity(ticker)
        for key, value in kwargs.items():
            if hasattr(R, key):
                setattr(R, key, value)

        self.ticker = ticker
        self.R = R
        return

    @property
    def description(self) -> pandas.Series:
        return self.R.info.copy()

    def __getattr__(self, item:str):
        if not item in dir(self):
            if item in self.description.index:
                return self.description[item]
            raise AttributeError
        return getattr(self, item)




if __name__ == "__main__":

    t = Ticker(
        "AAPL" # Apple Inc.
    )
    print(t.name)
    print(t.description)