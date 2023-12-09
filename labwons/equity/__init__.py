from labwons.common.metadata import metaData
from pandas import Series


class Equity(object):

    def __init__(self, ticker: str, **kwargs):
        self.ticker = ticker

        try:
            meta = metaData.loc[ticker]
        except (KeyError, ValueError):
            meta = Series(index=metaData.columns)
            meta[["country", "quoteType"]] = "KOR" if ticker.isdigit() else "USA", "EQUITY"

        if list(meta[["country", "quoteType"]]) == ["KOR", "EQUITY"]:
            from labwons.equity.fetch.kr.fetch import stock
            from labwons.equity.snap.kr.stock import snap
            self.data = data = stock(ticker)
            self.snap = snap(ticker, meta, data)
        elif list(meta[["country", "quoteType"]]) == ["KOR", "ETF"]:
            from labwons.equity.fetch.kr.fetch import etf
            from labwons.equity.snap.kr.etf import snap
            self.data = data = etf(ticker)
            self.snap = snap(ticker, meta, data)
        elif meta["country"] == "USA":
            from labwons.equity.fetch.us.fetch import equity
            from labwons.equity.snap.us import snap
            self.data = equity(ticker)
            self.snap = snap(ticker)
        else:
            raise AttributeError(f"Unidentified country: {meta['country']} for <ticker: {ticker}>")

        for key, value in kwargs.items():
            if hasattr(self.data, key):
                setattr(self.data, key, value)

        return

    def __getattr__(self, item:str):
        if item in dir(self.snap):
            return getattr(self.snap, item)
        if not item in dir(self):
            raise AttributeError

    @property
    def ohlcv(self):
        attr = self.data.attr("ohlcv")
        if not hasattr(self, attr):
            from labwons.equity.chart.tech.ohlcv import ohlcv
            self.__setattr__(attr, ohlcv(data=self.data.price, name=self.snap.name, ticker=self.ticker))
        return self.__getattribute__(attr)


if __name__ == "__main__":
    import pandas
    pandas.set_option('display.expand_frame_repr', False)
    t = Equity(
        # "005930" # SamsungElec
        # "000660" # SK hynix
        # "207940" # SAMSUNG BIOLOGICS
        # "005380" # HyundaiMtr
        "005490" # POSCO
        # "035420" # NAVER Corporation
        # "000270" # Kia Corporation
        # "051910" # LG Chem, Ltd.
        # "006400" # Samsung SDI Co., Ltd.
        # "068270" # Celltrion, Inc.
        # "035720" # Kakao Corp.
        # "028260" # Samsung C&T Corporation
        # "105560" # KB Financial Group Inc.
        # "012330" # Mobis
        # "055550" # Shinhan Financial Group Co., Ltd.
        # "066570" # LG Electronics Inc.
        # "032830" # Samsung Life Insurance Co., Ltd.
        # "096770" # SK Innovation Co., Ltd.
        # "003550" # LG Corp.
        # "015760" # Korea Electric Power Corporation
        # "017670" # SK Telecom Co.,Ltd
        # "316140" # Woori Financial Group Inc.

        # "359090"  # C&R Research
        # "042660"  # Daewoo Shipbuilding & Marine Engineering Co.,Ltd
        # "021080" # Atinum Investment
        # "130500" # GH Advanced Materials Inc.
        # "323280" # SHT-5 SPAC

        # "102780" # KODEX 삼성그룹

        # "AAPL"
    )
    print(t.name)
    # print(t.snap())
    # print(t.price)
    t.ohlcv()

    # import random
    # tickers = random.sample(metaData.equityKOR.index.tolist(), 10)
    # for ticker in tickers:
    #     print(ticker, "...." * 15)
    #     print(Equity(ticker).description)
