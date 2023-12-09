from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity._de.fetch import fetch
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
            unit=base.currency,
            ref=base
        )
        self['*up'] = (self['*up'] * self['up']).replace(0.0, np.nan)
        self['*down'] = (self['*down'] * self['down']).replace(0.0, np.nan)
        self['psar'] = self[['up', 'down']].apply(lambda x: x['up'] if np.isnan(x['down']) else x['down'], axis=1)
        self._ups_, self._dns_ = [], []

        data = self.join(self.ref.ohlcv.t, how='left')
        self['pct'] = 100 * (data['psar'] / data[self.ref.ohlcv.t.name] - 1)
        return

    def __tr__(self, col:str, mode:str='scatterTY', drop:bool=True, **kwargs):
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

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r3c1nsy()
        fig.add_trace(row=1, col=1, trace=self.ref.ohlcv())
        fig.add_trace(row=1, col=1, trace=self.__tr__('up'))
        fig.add_trace(row=1, col=1, trace=self.__tr__('down'))
        fig.add_trace(row=1, col=1, trace=self.__tr__('*up'))
        fig.add_trace(row=1, col=1, trace=self.__tr__('*down'))
        fig.add_trace(row=2, col=1, trace=self.ref.ohlcv.v('barTY', name='Vol.', showlegend=False, marker={"color": "grey"}))
        fig.add_trace(row=3, col=1, trace=self('pct', unit='%', showlegend=False))
        fig.update_layout(title=f"<b>{self.subject}</b> : {self.name}", **kwargs)
        fig.update_yaxes(row=1, col=1, title=f"[{self.unit}]")
        fig.update_yaxes(row=2, col=1, title="Vol.")
        fig.update_yaxes(row=3, col=1, title="Gap [%]", zerolinewidth=1.8)
        fig.update_xaxes(patch={"autorange": False, "range": [self.index[0], self.index[-1]]})
        return fig

    @property
    def currentGap(self) -> float:
        return self['pct'][-1]



