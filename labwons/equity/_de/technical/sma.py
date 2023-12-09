from labwons.common.basis import baseDataFrameChart
from labwons.equity._de.fetch import fetch
from plotly import graph_objects as go
import pandas as pd


class sma(baseDataFrameChart):

    def __init__(self, base:fetch):
        underlying = base.ohlcv.t.copy()
        objs = {
            "MA5D" : underlying.rolling(5).mean(),
            "MA1M": underlying.rolling(21).mean(),
            "MA3M": underlying.rolling(63).mean(),
            "MA6M": underlying.rolling(126).mean(),
            "MA1Y": underlying.rolling(200).mean(),
        }
        super(sma, self).__init__(
            data=pd.concat(objs=objs, axis=1),
            name="SMA",
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            form='.1f',
            unit=base.currency,
            ref=base
        )
        return

    def addMA(self, col:str, window:int):
        if not col in self and col.startswith('MA'):
            self[col] = self.ref.ohlcv.t.rolling(window).mean()
        return

    def addGC(self, col:str, bottom:str, top:str):
        # DEPRECATED
        return

    def addDC(self, col:str, bottom:str, top:str):
        # DEPRECATED
        return

    def figure(self, **kwargs) -> go.Figure:
        fig = self.ref.ohlcv.figure()
        for col in self:
            if col.startswith('MA'):
                fig.add_trace(row=1, col=1, trace=self(col, visible='legendonly', line={"dash": "dot", "width": 1.0}))
        fig.update_layout(title=f"<b>{self.subject}</b> : {self.name}", **kwargs)
        return fig