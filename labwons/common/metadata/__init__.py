from labwons.common.config import WI26, FRED, OECD
from labwons.common.metadata import fetch
from pykrx.stock import get_index_portfolio_deposit_file
from typing import Union, Hashable
import pandas, os

class _metadata(pandas.DataFrame):

    class _api(object):
        _ss, _es = "", ""
        @property
        def SS(self) -> str:
            return self._ss
        @SS.setter
        def SS(self, api:str):
            self._ss = api
        @property
        def ES(self) -> str:
            return self._es
        @ES.setter
        def ES(self, api:str):
            self._es = api
        pass

    icm:pandas.DataFrame = pandas.DataFrame()
    api:_api = None
    def __init__(self):
        # src = "https://github.com/Jehoshaphat-kr/labwons/raw/master/labwons/common/metadata/metadata.pkl"
        src = os.path.join(os.path.dirname(__file__), r"metadata.pkl")
        dat = pandas.read_pickle(src)
        super().__init__(data=dat.values, index=dat.index, columns=dat.columns)
        self.api = self._api()
        return

    def __call__(self, ticker:Union[str, Hashable]) -> pandas.Series:
        try:
            return self.loc[ticker]
        except KeyError:
            meta = pandas.Series(index=self.columns, name=ticker)
            meta["name"] = ticker
            meta["country"] = "KOR" if ticker.isdigit() and len(ticker) == 6 else "USA"
            return meta

    @property
    def oecd(self) -> pandas.DataFrame:
        return pandas.DataFrame(OECD).set_index(keys="ticker")

    @property
    def fred(self) -> pandas.DataFrame:
        return pandas.DataFrame(FRED).set_index(keys="ticker")

    @property
    def ecos(self) -> pandas.DataFrame:
        return fetch.ecos(self.api.ES)

    @property
    def equityKOR(self) -> pandas.DataFrame:
        return self[(self['quoteType'] == 'EQUITY') & (self['country'] == 'KOR')]

    @property
    def equityUSA(self) -> pandas.DataFrame:
        return self[(self['quoteType'] == 'EQUITY') & (self['country'] == 'USA')]

    @property
    def etfKOR(self) -> pandas.DataFrame:
        return self[(self['quoteType'] == 'ETF') & (self['country'] == 'KOR')]

    @property
    def etfUSA(self) -> pandas.DataFrame:
        return self[(self['quoteType'] == 'ETF') & (self['country'] == 'USA')]

    @property
    def icmKOR(self) -> pandas.DataFrame:
        if self.icm.empty:
            self.icm = self.equityKOR.drop(columns=["IPO"]).join(fetch.krxMarketCapMultipleIpo(), how='left')
        return self.icm

    def ecosContains(self, symbol:str):
        return fetch.ecosContains(self.api.ES, symbol)

    def getKrse(self) -> pandas.DataFrame:
        """
        Korean Stock Exchange(KRSE) Listed Company
        """

        # ------------------------------------------------------------------------------------
        # WISE WI26 Industry-Configured by ticker
        # [DataFrame *index]   : 'ticker'
        # [DataFrame *columns] : ['korName', 'sector']
        # ------------------------------------------------------------------------------------
        meta = pandas.DataFrame(data=WI26).set_index(keys='id')
        date = fetch.wiseDate()
        data = pandas.concat(objs=[fetch.wiseIndustry(date, cd) for cd in meta.index], axis=0)

        # ------------------------------------------------------------------------------------
        # Stock Symbol API: Get English Name of Listed Companies
        # [DataFrame *index]   : 'ticker'
        # [DataFrame *columns] : ['shortName', 'longName', 'quoteType', 'country']
        # ------------------------------------------------------------------------------------
        data = data.join(fetch.krxNames(self.api.SS), how='left')

        # ------------------------------------------------------------------------------------
        # Post Process
        # 1) Join English Name: ['name', 'korName', 'shortName', 'longName']
        # 2) Set Representative Name: ['name'] ('shortName' is prior to 'korName')
        # 3) Set Exchange: KOSPI / KOSDAQ
        # 4) Set Benchmark
        # ------------------------------------------------------------------------------------
        ks = get_index_portfolio_deposit_file('1001', alternative=True)
        kq = get_index_portfolio_deposit_file('2001', alternative=True)

        fdef = lambda x: x['korName'] if pandas.isna(x['shortName']) else x['shortName']
        data['name'] = data[['shortName', 'korName']].apply(fdef, axis=1)
        data['exchange'] = ['KOSPI' if t in ks else 'KOSDAQ' if t in kq else 'Unknown' for t in data.index]
        data[['country', 'currency']] = 'KOR', 'KRW'

        bench = meta[['name', 'benchmarkTicker', 'benchmarkName']].set_index(keys='name').to_dict(orient='index')
        data['benchmarkTicker'] = data['industry'].apply(lambda x:bench[x.replace("WI26 ", "")]['benchmarkTicker'])
        data['benchmarkName'] = data['industry'].apply(lambda x:bench[x.replace("WI26 ", "")]['benchmarkName'])
        data = data.join(self.icmKOR[['IPO']].copy(), how='left')
        return data.drop_duplicates()

    def getNyse(self) -> pandas.DataFrame:
        """
        New-York Stock Exchange(NYSE) Listed Company
        """
        return fetch.nyseEquity(self.api.SS).drop_duplicates()

    def save(self):
        """
        Update and Save all tickers
        :return:
        """
        df = pandas.concat(
            objs=[
                self.getKrse(),
                self.getNyse(),
                fetch.krxEtf(),
                fetch.nyseEtfFromNasdaq(),
                fetch.nyseEtfFromWikipedia(),
                fetch.nyseEtfFromCBOE()
            ], axis=0
        )
        df = df[~df.index.duplicated(keep='last')]
        df.to_pickle(r'./metadata.pkl')
        super().__init__(data=df.values, index=df.index, columns=df.columns)
        return

# Alias
metaData = _metadata()


if __name__ == "__main__":
    pandas.set_option('display.expand_frame_repr', False)
    metaData.api.SS = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
    metaData.api.ES = "CEW3KQU603E6GA8VX0O9"

    # print(metaData)
    # print(metaData.ecos)
    # print(metaData.fred)
    # print(metaData.oecd)
    # print(metaData.equityKOR)
    # print(metaData.equityUSA)
    # print(metaData.etfKOR)
    # print(metaData.etfUSA)
    # print(metaData.icmKOR)
    # print(metaData.getKrse())
    # print(metaData.getNyse())

    metaData.save()
    print(metaData)