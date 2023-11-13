from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from datetime import timedelta
import plotly.graph_objects as go
import pandas as pd


class _bars(baseDataFrameChart):

    settings = None
    def __init__(self, slots:dict, data:pd.DataFrame, settings:dict):
        self.settings = settings
        base = list(slots.values())[0]
        super(_bars, self).__init__(
            data=data,
            name="RETURNS",
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            form='.2f',
            unit='%',
            ref=base
        )
        return