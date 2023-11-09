from labwons.common.service.tools import stringDel
from datetime import datetime
import pandas as pd
import numpy as np
import re


class naver(object):

    def __init__(self, ticker:str):
        self._t = ticker
        return

    @property
    def _tables(self) -> list:
        if not hasattr(self, '__tables'):
            self.__setattr__(
                '__tables',
                pd.read_html(
                    io=f"https://finance.naver.com/item/main.naver?code={self._t}",
                    header=0,
                    encoding='euc-kr'
                )
            )
        return self.__getattribute__('__tables')


    @property
    def trailingPE(self) -> float:
        """
        직전 4분기 EPS 총합 대비 현재가(종가)
        :return:
        """
        src, _ = map(str, self._tables[8].columns[-1].split('l'))
        return np.nan if src.startswith('N/A') else float(src.replace('배', '').replace(' ', ''))

    @property
    def trailingEps(self) -> int:
        """
        직전 4분기 EPS 총합
        :return:
        """
        _, src = map(str, self._tables[8].columns[-1].split('l'))
        return int(src.replace(',', '').replace('원', ''))

    @property
    def estimatePE(self) -> float:
        """
        당해 연말 추정 PER(Consensus)
        :return:
        """
        src, _ = map(str, self._tables[8].iloc[0].values[-1].split('l'))
        per = np.nan if src.startswith('N/A') else float(src.replace('배', '').replace(' ', ''))
        return np.nan if per < 0 else per

    @property
    def estimateEps(self) -> int:
        """
        당해 연말 추정 EPS(Consensus)
        :return:
        """
        _, src = map(str, self._tables[8].iloc[0].values[-1].split('l'))
        return int(src.replace(',', '').replace('원', ''))

    @property
    def trailingDate(self) -> datetime.date:
        src = self._tables[8].columns[0]
        ymd = datetime.strptime(src[src.index("(") + 1 : src.index(")")], "%Y.%m")
        return ymd.date()

    @property
    def estimateDate(self) -> datetime.date:
        return datetime(datetime.today().year, 12, 31).date()

    @property
    def similarity(self) -> pd.DataFrame:
        sim = self._tables[4]
        sim = sim.set_index(keys='종목명')
        sim = sim.drop(index=['전일대비'])
        sim.index.name = None
        for col in sim:
            sim[col] = sim[col].apply(lambda x: stringDel(str(x), ['하향', '상향', '%', '+', ' ']))
        tickers = [c.replace('*', '')[-6:] for c in sim.columns]
        labels = [c.replace('*', '')[:-6] for c in sim.columns]
        sim.columns = tickers
        return pd.concat(objs=[pd.DataFrame(columns=tickers, index=['종목명'], data=[labels]), sim], axis=0).T


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)

    # ticker = '005930'
    ticker = '000660' # SK하이닉스
    # ticker = '003800' # 에이스침대
    # ticker = '058470' # 리노공업
    # ticker = '102780' # KODEX 삼성그룹

    nav = naver(ticker)
    # print(nav.trailingPE)
    # print(nav.trailingEps)
    # print(nav.estimatePE)
    # print(nav.estimateEps)
    # print(nav.trailingDate)
    # print(nav.estimateDate)
    # print(nav.similarity)