"""
This app is recommended to run on .ipynb file
"""
from typing import Union, Tuple, List
from datetime import datetime
from tqdm.notebook import tqdm
# from tqdm import tqdm
from labwons.common.metadata.metadata import MetaData
from labwons.equity.equity import Equity
from pykrx import stock
import pandas as pd
import plotly.graph_objects as go
import time


class market(pd.DataFrame):
    _slot_ = {}
    _proc_ = True
    def __init__(self, tickers:Union[Tuple, List, pd.Series, pd.Index], proc:bool=True, **kwargs):
        for n, t in enumerate(tqdm(tickers, desc='initialize...')):
            self._slot_[t] = Equity(t, **kwargs)
            if not n % 20:
                time.sleep(0.5)
        self._proc_ = proc
        meta = MetaData[MetaData.index.isin(tickers)][[
            'name', 'quoteType', 'market', 'korName'
        ]].copy()
        meta = meta[meta['market'] == 'KOR']
        caps = stock.get_market_cap_by_ticker(datetime.today().strftime("%Y%m%d"))[
            ['종가', '시가총액']
        ].rename(columns=dict(종가='close', 시가총액='marketCap'))
        meta = meta.join(caps, how='left')
        super().__init__(data=meta.values, index=meta.index, columns=meta.columns)
        return

    @staticmethod
    def _check_prop(prop:str):
        from labwons.equity import equity

        props = prop.split('.')
        obj = equity if len(props) > 1 else Equity
        for _prop in props:
            if not hasattr(obj, _prop):
                raise AttributeError(f'No Such attribute: {prop}')
            obj = getattr(obj, _prop)
        return obj

    def append(self, prop:str):
        prop = prop[:prop.find('(')] if prop.endswith(')') else prop
        self._check_prop(prop)

        data = []
        for ticker, slot in self._slot_.items():
            data.append(getattr)





if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)

    # indices = MetaData[MetaData['industry'] == 'WI26 반도체']
    # bubble = market(indices.index)
    # print(bubble)
    bubble = market(['005930'])
    # bubble.append('gapFiftyTwoWeekHigh')
    bubble.append('trend.gaps()')

