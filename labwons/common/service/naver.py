from labwons.common.service.tools import stringDel

import pandas as pd


class naver(object):

    def __init__(self, ticker:str):
        self._t = ticker
        self._html_ = pd.read_html(
            io=f"https://finance.naver.com/item/main.naver?code={ticker}",
            header=0,
            encoding='euc-kr'
        )
        return


    @property
    def similarity(self) -> pd.DataFrame:
        sim = self._html_[4]
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

    ticker = '005930'
    # ticker = '000660' # SK하이닉스
    # ticker = '003800' # 에이스침대
    # ticker = '058470' # 리노공업
    # ticker = '102780' # KODEX 삼성그룹

    nav = naver(ticker)
    print(nav.similarity)