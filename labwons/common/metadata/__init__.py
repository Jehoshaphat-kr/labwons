from labwons.common.config import WI26, FRED, OECD
from labwons.common.metadata.fetch import (
    fetchWiseDate,
    fetchWiseIndustry,
    fetchKrxEnglish,
    fetchKrxEtf,
    fetchNyse,
    fetchNyseEtfWikipedia,
    fetchNyseEtfNasdaq,
    fetchNyseEtfCBOE,
    fetchECOS,
    fetchKrseMarketCapMultipleIpo,
    getEcosContains,

)
from pykrx.stock import get_index_portfolio_deposit_file
import pandas as pd
import os


class metadata(pd.DataFrame):
    _api_ss = ''
    _api_ec = ''
    _icm_kr = pd.DataFrame()
    _col = [
        'name',
        'quoteType',
        'country',
        'exchange',
        'currency',
        'shortName',
        'longName',
        'korName',
        'sector',
        'industry',
        'benchmarkTicker',
        'benchmarkName',
    ]
    def __init__(self):
        data = pd.read_pickle(
            # "https://github.com/Jehoshaphat-kr/labwons/raw/master/labwons/common/metadata/metadata.pkl"
            os.path.join(os.path.dirname(__file__), r"metadata.pkl")
        )
        super().__init__(data=data.values, index=data.index, columns=data.columns)
        return

    @property
    def API_STOCK_SYMBOL(self) -> str:
        return self._api_ss

    @API_STOCK_SYMBOL.setter
    def API_STOCK_SYMBOL(self, api:str):
        self._api_ss = api

    @property
    def API_ECOS(self) -> str:
        return self._api_ec

    @API_ECOS.setter
    def API_ECOS(self, api:str):
        self._api_ec = api

    @property
    def OECD(self) -> pd.DataFrame:
        return self[self['exchange'] == 'OECD']

    @property
    def FRED(self) -> pd.DataFrame:
        return self[self['exchange'] == 'FRED']

    @property
    def ECOS(self) -> pd.DataFrame:
        return self[self['exchange'] == 'ECOS']

    @property
    def KRSTOCK(self) -> pd.DataFrame:
        return self[(self['quoteType'] == 'EQUITY') & (self['country'] == 'KOR')]

    @property
    def USSTOCK(self) -> pd.DataFrame:
        return self[(self['quoteType'] == 'EQUITY') & (self['country'] == 'USA')]

    @property
    def KRETF(self) -> pd.DataFrame:
        return self[(self['quoteType'] == 'ETF') & (self['country'] == 'KOR')]

    @property
    def USETF(self) -> pd.DataFrame:
        return self[(self['quoteType'] == 'ETF') & (self['country'] == 'USA')]

    @property
    def KRSTOCKwMultiples(self):
        if self._icm_kr.empty:
            self._icm_kr = self.KRSTOCK.join(fetchKrseMarketCapMultipleIpo(), how='left')
        return self._icm_kr

    def ecosContains(self, ticker:str):
        return getEcosContains(self.API_ECOS, ticker)

    def getKrse(self) -> pd.DataFrame:
        """
        Korean Stock Exchange(KRSE) Listed Company
        """

        # ------------------------------------------------------------------------------------
        # WISE WI26 Industry-Configured by ticker
        # [DataFrame *index]   : 'ticker'
        # [DataFrame *columns] : ['korName', 'sector']
        # ------------------------------------------------------------------------------------
        meta = pd.DataFrame(data=WI26).set_index(keys='id')
        date = fetchWiseDate()
        data = pd.concat(objs=[fetchWiseIndustry(date, cd) for cd in meta.index], axis=0)

        # ------------------------------------------------------------------------------------
        # Stock Symbol API: Get English Name of Listed Companies
        # [DataFrame *index]   : 'ticker'
        # [DataFrame *columns] : ['shortName', 'longName', 'quoteType', 'country']
        # ------------------------------------------------------------------------------------
        data = data.join(fetchKrxEnglish(self.API_STOCK_SYMBOL), how='left')

        # ------------------------------------------------------------------------------------
        # Post Process
        # 1) Join English Name: ['name', 'korName', 'shortName', 'longName']
        # 2) Set Representative Name: ['name'] ('shortName' is prior to 'korName')
        # 3) Set Exchange: KOSPI / KOSDAQ
        # 4) Set Benchmark
        # ------------------------------------------------------------------------------------
        ks = get_index_portfolio_deposit_file('1001', alternative=True)
        kq = get_index_portfolio_deposit_file('2001', alternative=True)

        fdef = lambda x: x['korName'] if pd.isna(x['shortName']) else x['shortName']
        data['name'] = data[['shortName', 'korName']].apply(fdef, axis=1)
        data['country'] = 'KOR'
        data['exchange'] = ['KOSPI' if t in ks else 'KOSDAQ' if t in kq else 'Unknown' for t in data.index]
        data['currency'] = 'KRW'

        bench = meta[['name', 'benchmarkTicker', 'benchmarkName']].set_index(keys='name').to_dict(orient='index')
        data['benchmarkTicker'] = data['industry'].apply(lambda x:bench[x.replace("WI26 ", "")]['benchmarkTicker'])
        data['benchmarkName'] = data['industry'].apply(lambda x:bench[x.replace("WI26 ", "")]['benchmarkName'])
        return data.drop_duplicates()

    def getNyse(self) -> pd.DataFrame:
        """
        New-York Stock Exchange(NYSE) Listed Company
        """
        return fetchNyse(self.API_STOCK_SYMBOL).drop_duplicates()

    def save(self):
        """
        Update and Save all tickers
        :return:
        """
        df = pd.concat(
            objs=[
                self.getKrse(),
                self.getNyse(),
                fetchKrxEtf(),
                fetchNyseEtfWikipedia(),
                fetchNyseEtfNasdaq(),
                fetchNyseEtfCBOE(),
                fetchECOS(self.API_ECOS),
                pd.DataFrame(data=FRED).set_index(keys='ticker'),
                pd.DataFrame(data=OECD).set_index(keys='ticker')
            ],
            axis=0
        )[self._col]
        df = df[~df.index.duplicated(keep='last')]
        df.to_pickle(r'./metadata.pkl')
        super().__init__(data=df.values, index=df.index, columns=df.columns)
        return

# Alias
metaData = metadata()


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)

    print(metaData)
    # print(metaData.ECOS)
    # print(metaData.FRED)
    # print(metaData.OECD)
    # print(metaData.KRSTOCK)
    # print(metaData.KRETF)
    # print(metaData.USSTOCK)
    # print(metaData.USETF)
    # print(metaData.KRSTOCKwMultiples)

    # metaData.API_STOCK_SYMBOL = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
    # metaData.API_ECOS = "CEW3KQU603E6GA8VX0O9"
    # metaData.save()
    # print(metaData.index.value_counts())