from pandas import DataFrame
from plotly import Bar, Scatter, Figure
from typing import Dict

class dataChart:

    def __init__(
        self,
        data:DataFrame=DataFrame(),
        trace:Dict[str, Dict]=None,
        chart:Figure=Figure()
    ):
        self.data = data
        self.trace = trace
        self.chart =chart
        return

