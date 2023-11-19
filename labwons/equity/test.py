from labwons.common.metadata.metadata import MetaData
from labwons.equity.source.krstock import krstock
from labwons.equity.technical.technical import technical


def Ticker(ticker:str, **kwargs):
    if ticker.isalpha():
        class _ticker(object):
            pass
    elif ticker.isdigit() and ticker in MetaData.KRETF.index:
        class _ticker(object):
            pass
    elif ticker.isdigit():
        class _ticker(krstock, technical):
            def __init__(self, ticker:str, period:int=10, enddate:str="", freq:str="d", language:str="eng"):
                krstock.__init__(self, ticker, period, enddate, freq, language)
                technical.__init__(self, self.ohlcv, ticker, self.name, self.path, language)
                return
    else:
        raise KeyError(f"Unidentify ticker: {ticker}")
    return _ticker(ticker, **kwargs)


if __name__ == "__main__":

    myStock = Ticker(
        ticker="005930"
    )
    print(myStock.describe("series"))
    myStock.ohlcvt.show()