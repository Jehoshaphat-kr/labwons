from nohji.util.web import web
from nohji.config import api
from stocksymbol import StockSymbol
from pandas import concat, DataFrame
from typing import Any


class _nyse:
    """
    New York Stock Exchange(NYSE) provided dataset
    * API key required for this <class; StockSymbol>

    @stock:
        type        : DataFrame
        description : listed stocks with implicit information
        columns     : ['name', 'shortName', 'longName', 'exchange', 'quoteType', 'currency',
                       'country', 'benchmark', 'benchmarkTicker']
        example     :
                                         name  shortName                   longName  ...  benchmark benchmarkTicker
            ticker
            AAPL                   Apple Inc.      apple                 Apple Inc.  ...     Nasdaq             QQQ
            MSFT        Microsoft Corporation  microsoft      Microsoft Corporation  ...     Nasdaq             QQQ
            GOOG                Alphabet Inc.   alphabet              Alphabet Inc.  ...     Nasdaq             QQQ
            GOOGL               Alphabet Inc.   alphabet              Alphabet Inc.  ...     Nasdaq             QQQ
            AMZN             Amazon.com, Inc.     amazon           Amazon.com, Inc.  ...     Nasdaq             QQQ
            ...                           ...        ...                        ...  ...        ...             ...
            GNAL       Generation Alpha, Inc.                Generation Alpha, Inc.  ...     S&P500             SPY
            ZIMCF                   ZIM Corp.                             ZIM Corp.  ...     S&P500             SPY
            FLCX               flooidCX Corp.                        flooidCX Corp.  ...     S&P500             SPY
            BLEG          BRANDED LEGACY INC.                   BRANDED LEGACY INC.  ...     S&P500             SPY
            RRIF    Rainforest Resources Inc.             Rainforest Resources Inc.  ...     S&P500             SPY

    @etfNasdaq:
        type        : DataFrame
        description : listed ETFs from Nasdaq
        columns     : ['name', 'exchange', 'quoteType', 'currency', 'country',
                       'benchmarkTicker', 'benchmarkName']
        example     :
                    name exchange quoteType currency country benchmarkTicker benchmarkName
            ticker
            AADR    AADR   NASDAQ       ETF      USD     USA             QQQ        NASDAQ
            AAPB    AAPB   NASDAQ       ETF      USD     USA             QQQ        NASDAQ
            AAPB    AAPB   NASDAQ       ETF      USD     USA             QQQ        NASDAQ
            AAPD    AAPD   NASDAQ       ETF      USD     USA             QQQ        NASDAQ
            AAPD    AAPD   NASDAQ       ETF      USD     USA             QQQ        NASDAQ
            ...      ...      ...       ...      ...     ...             ...           ...
            XBIL    XBIL   NASDAQ       ETF      USD     USA             QQQ        NASDAQ
            XFIX    XFIX   NASDAQ       ETF      USD     USA             QQQ        NASDAQ
            XFIX    XFIX   NASDAQ       ETF      USD     USA             QQQ        NASDAQ
            XT        XT   NASDAQ       ETF      USD     USA             QQQ        NASDAQ
            YLDE    YLDE   NASDAQ       ETF      USD     USA             QQQ        NASDAQ

    @etfCboe:
        type        : DataFrame
        description : listed ETFs from CBOE (Chicago Board Options Exchange)
        columns     : ['name', 'exchange', 'quoteType', 'currency', 'country',
                       'benchmarkTicker', 'benchmarkName']
        example     :
                    name exchange quoteType currency country benchmarkTicker benchmarkName
            ticker
            AAAU    AAAU     CBOE       ETF      USD     USA             VXX           VIX
            AAPY    AAPY     CBOE       ETF      USD     USA             VXX           VIX
            ACIO    ACIO     CBOE       ETF      USD     USA             VXX           VIX
            ACSI    ACSI     CBOE       ETF      USD     USA             VXX           VIX
            ACWV    ACWV     CBOE       ETF      USD     USA             VXX           VIX
            ...      ...      ...       ...      ...     ...             ...           ...
            YPS      YPS     CBOE       ETF      USD     USA             VXX           VIX
            YSEP    YSEP     CBOE       ETF      USD     USA             VXX           VIX
            ZALT    ZALT     CBOE       ETF      USD     USA             VXX           VIX
            ZECP    ZECP     CBOE       ETF      USD     USA             VXX           VIX
            ZIVB    ZIVB     CBOE       ETF      USD     USA             VXX           VIX
    """
    __data__: DataFrame = DataFrame()

    def __init__(self):
        self.__data__ = DataFrame()
        return

    def __call__(self) -> DataFrame:
        return self.data

    def __str__(self) -> str:
        return str(self.data)

    def __getattr__(self, item: Any):
        if hasattr(self.data, item):
            return getattr(self.data, item)
        if not item in dir(self):
            raise AttributeError

    def __getitem__(self, item: Any):
        return self.data[item]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    @property
    def stock(self) -> DataFrame:
        data = DataFrame(StockSymbol(api.stockSymbol).get_symbol_list(market='us'))
        data = data.rename(columns={'symbol':'ticker'}).set_index(keys='ticker')
        data['name'] = data['longName']
        data[['quoteType', 'currency', 'country']] = ['EQUITY', 'USD', 'USA']
        data['benchmarkTicker'] = data['exchange'].apply(lambda x: 'QQQ' if x == 'NASDAQ' else 'SPY')
        data['benchmark'] = data['exchange'].apply(lambda x: 'Nasdaq' if x == 'NASDAQ' else 'S&P500')
        return data[[
            'name', 'shortName', 'longName',
            'exchange', 'quoteType', 'currency', 'country',
            'benchmark', 'benchmarkTicker'
        ]]

    @property
    def etfNasdaq(self) -> DataFrame:
        url = "https://www.nasdaqtrader.com/trader.aspx?id=etf_definitions"
        src = web.html(url, "html.parser")
        data = list()
        for row in src.find_all('tr')[1:]:
            ticker, comment = (d.text for d in row.find_all('td')[:2])
            data.append({
                'ticker':ticker,
                'name':ticker,
                'exchange':'NASDAQ',
                'quoteType':'ETF',
                'currency':'USD',
                'country':'USA',
                'benchmarkTicker':'QQQ',
                'benchmark':'NASDAQ'
            })
        return DataFrame(data=data).set_index(keys='ticker')

    @property
    def etfCboe(self) -> DataFrame:
        url = "https://www.cboe.com/us/equities/market_statistics/listed_symbols/xml/"
        src = web.html(url)
        data = list()
        for s in src.find_all("symbol"):
            data.append({
                "ticker":s['name'],
                "name":s['name'],
                "exchange":'CBOE',
                "quoteType":'ETF',
                "currency":'USD',
                "country":'USA',
                'benchmarkTicker': 'VXX',
                'benchmark': 'VIX'
            })
        return DataFrame(data=data).set_index(keys='ticker').drop_duplicates()

    @property
    def data(self) -> DataFrame:
        if self.__data__.empty:
            self.__data__ = concat([self.stock, self.etfNasdaq, self.etfCboe], axis=0)
        return self.__data__

# Alias
nyse = _nyse()

if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    api.stockSymbol = "95012214-44b0-4664-813f-a7ef5ad3b0b4"

    print(nyse.stock)
    print(nyse.etfNasdaq)
    print(nyse.etfCboe)
    print(nyse)
