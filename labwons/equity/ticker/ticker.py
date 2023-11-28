

def _ticker(ticker:str):
    if ticker.isdigit():
        from labwons.common.metadata.metadata import MetaData

        if ticker in MetaData.KRETF.index:
            from labwons.equity.ticker.kr.etf import etf
            class __ticker__(etf):
                pass
        else:
            from labwons.equity.ticker.kr.stock import stock
            class __ticker__:
                def __init__(self, ticker:str):
                    self.ticker = ticker
                    self.source = stock(ticker)
                    return
                pass
    else:
        class __ticker__:
            def __init__(self, ticker:str):
                return
            pass
    return __ticker__(ticker)

# Alias
Ticker = _ticker

if __name__ == "__main__":

    t = Ticker("005930")
