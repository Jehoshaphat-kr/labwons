from labwons.equity.equity import Equity
from labwons.indicator.indicator import Indicator


class MultiChart(object):
    def __init__(self, *args):
        self.args = args
        return

    def _traces(self):
        traces = list()
        for elem in self.args:
            if isinstance(elem, Equity):
                traces.append(elem.typical())
            elif isinstance(elem, Indicator):
                traces.append(elem)
