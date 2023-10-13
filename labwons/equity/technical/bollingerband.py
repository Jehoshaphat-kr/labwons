from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
import pandas as pd
import numpy as np


class bollingerband(baseDataFrameChart):
    def __init__(self, base:fetch):
        data = pd.DataFrame()
        data['typical'] = base.ohlcv.t.copy()
        data['middle'] = base.ohlcv.t.rolling(window=20).mean()
        data['stdev'] = base.ohlcv.t.rolling(window=20).std()
        data['upperband'] = data.middle + 2 * data.stdev
        data['lowerband'] = data.middle - 2 * data.stdev
        data['uppertrend'] = data.middle + data.stdev
        data['lowertrend'] = data.middle - data.stdev
        data['width'] = 100 * (4 * data.stdev) / data.middle
        data['pctb'] = (
                (data.typical - data.lowerband) / (data.upperband - data.lowerband)
        ).where(data.upperband != data.lowerband, np.nan)

        super(bollingerband, self).__init__(
            data=data,
            name="BOLLINGERBAND",
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            form=',.1f',
            unit=base.unit,
            ref=base
        )
        return


    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r4c1nsy()
        fig.add_trace(row=1, col=1, trace=self.ref.ohlcv())
        fig.add_trace(row=1, col=1, trace=self.lineTY('middle'))
        fig.add_trace(row=1, col=1, trace=self.lineTY(
            'upperband', name='x2 Band', legendgroup='x2', line={"dash":"dash", "color":"maroon"}
        ))
        fig.add_trace(row=1, col=1, trace=self.lineTY(
            'lowerband', name='x2 Band', legendgroup='x2', showlegend=False, line={"dash": "dash", "color": "maroon"}
        ))
        fig.add_trace(row=1, col=1, trace=self.lineTY(
            'uppertrend', name='x1 Band', legendgroup='x1', line={"dash": "dot", "color": "lightgreen"}
        ))
        fig.add_trace(row=1, col=1, trace=self.lineTY(
            'lowertrend', name='x1 Band', legendgroup='x1', showlegend=False, line={"dash": "dot", "color": "lightgreen"}
        ))
        fig.add_trace(row=2, col=1, trace=self.ref.ohlcv.v('barTY', name='거래량', showlegend=False))
        fig.add_trace(row=3, col=1, trace=self.lineTY('width', name='Width', unit='%', form='.2f'))
        fig.add_trace(row=4, col=1, trace=self.lineTY('pctb', name='%B', unit='', form='.2f'))

        fig.update_layout(title=f"<b>{self.subject}</b> : BOLLINGER-BAND")
        fig.update_yaxes(row=1, col=1, patch={"title":f"[{self.unit}]"})
        fig.update_yaxes(row=2, col=1, patch={"title": f"Vol."})
        fig.update_yaxes(row=3, col=1, patch={"title": f"Width [%]"})
        fig.update_yaxes(row=4, col=1, patch={"title": f"%B [-]"})
        return fig
