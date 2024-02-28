from nohji.deprecated.labwons.equity import fetch
import pandas


class Ticker(object):

    def __init__(self, ticker:str, **kwargs):
        data = fetch.equity(ticker)
        for key, value in kwargs.items():
            if hasattr(data, key):
                setattr(data, key, value)

        self.ticker = ticker
        self.data = data
        return

    @property
    def description(self) -> pandas.Series:
        return self.data.info.copy()

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