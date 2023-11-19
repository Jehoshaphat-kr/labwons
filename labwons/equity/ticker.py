from labwons.common.metadata.metadata import MetaData
from labwons.equity.source.krstock import krstock


def _ticker(ticker:str):
    if ticker.isalpha():
        class ticker(object):
            pass
    elif ticker.isdigit() and ticker in MetaData.KRETF.index:
        class ticker(object):
            pass
    elif ticker.isdigit():
        class ticker(krstock):
            pass
    else:
        raise KeyError(f"Unidentify ticker: {ticker}")
    return ticker
