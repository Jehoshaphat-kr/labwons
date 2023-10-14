from labwons.common.basis import baseDataFrameChart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
import numpy as np


class psar(baseDataFrameChart):
    _ups_, _dns_ = [], []
    def __init__(self, base:fetch):
        sampler = {
            "trend_psar_up" : "up",
            "trend_psar_down" : "down",
            "trend_psar_up_indicator" : "*up",
            "trend_psar_down_indicator" : "*down"
        }
        super().__init__(
            data=base.ta[sampler.keys()].rename(columns=sampler),
            name="PSAR",
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            form='.1f',
            unit=base.unit,
            ref=base
        )
        self['*up'] = (self['*up'] * self['up']).replace(0.0, np.nan)
        self['*down'] = (self['*down'] * self['down']).replace(0.0, np.nan)
        self._ups_, self._dns_ = [], []
        return

    def __call__(self, col:str, mode:str='scatterTY', drop:bool=True, **kwargs):
        trace = self.scatterTY(col)
        trace.name = 'Signal' if col == '*up' else col
        trace.showlegend = True if col == '*up' else False
        trace.legendgroup = None if col in ['up', 'down'] else 'signal'
        trace.marker.symbol = "triangle-up" if col == '*up' else "triangle-down" if col == '*down' else "circle"
        trace.marker.color = "red" if col == "*up" else "blue" if col == "*down" else "#999"
        trace.marker.size = 7 if col.startswith('*') else 5
        return trace

    @property
    def upsides(self) -> list:
        if not self._ups_:
            copy = self.copy().reset_index()
            mask = copy['down'].isna()
            for _, val in copy[mask].groupby((mask != mask.shift()).cumsum()):
                self._ups_.append(val.set_index(keys='date'))
        return self._ups_

    @property
    def downsides(self) -> list:
        if not self._dns_:
            copy = self.copy().reset_index()
            mask = copy['up'].isna()
            for _, val in copy[mask].groupby((mask != mask.shift()).cumsum()):
                self._dns_.append(val.set_index(keys='date'))
        return self._dns_

    def figure(self) -> go.Figure:
        fig = self.ref.ohlcv.figure()
        fig.add_trace(row=1, col=1, trace=self('up'))
        fig.add_trace(row=1, col=1, trace=self('down'))
        fig.add_trace(row=1, col=1, trace=self('*up'))
        fig.add_trace(row=1, col=1, trace=self('*down'))
        fig.update_layout(title=f"<b>{self.subject}</b> : {self.name}")
        return fig

