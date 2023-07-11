from labwons.equity.fetch import _fetch
from datetime import timedelta
from scipy.stats import linregress
import pandas as pd
import numpy as np


class _refine(_fetch):

    @staticmethod
    def _deltaDate(timeseries: pd.Series or pd.DataFrame, delta: list) -> list:
        return [(timeseries.index >= (timeseries.index[-1] - timedelta(day)), tag, day) for tag, day in delta]

    @staticmethod
    def _lineFit(timeseries: pd.Series, **kwargs) -> pd.Series:
        timeseries = timeseries.copy()
        timeseries.index.name = 'time'
        timeseries.name = 'data'
        timeseries = timeseries.reset_index(level=0)

        xrange = (timeseries['time'].diff()).dt.days.fillna(1).astype(int).cumsum()
        slope, intercept, _, __, ___ = linregress(x=xrange, y=timeseries['data'])
        fitted = slope * xrange + intercept
        fitted.name = kwargs['name'] if 'name' in kwargs else 'fitted'
        return pd.concat(objs=[timeseries, fitted], axis=1)[['time', fitted.name]].set_index(keys='time')

    @staticmethod
    def _boundFit(ohlcv: pd.DataFrame, price:str, minInterval:int=-1, samplePoint:int=-1):
        if minInterval == -1:
            minInterval = 20 if len(ohlcv) > 252 else 10 if len(ohlcv) > 60 else 5
        if samplePoint == -1:
            samplePoint = 5 if len(ohlcv) > 252 else 4 if len(ohlcv) > 60 else 3
        locals()[price] = ohlcv.sort_values(by=price, ascending=False if price == 'high' else True)[['x', price]].copy()
        locals()[f"{price}s"] = [
            dict(date=locals()[price].index[0], x=locals()[price]['x'][0], value=locals()[price][price][0])
        ]
        for d in locals()[price].index[1:]:
            if all([abs((d - d2['date']).days) > minInterval for d2 in locals()[f"{price}s"]]):
                locals()[f"{price}s"].append(
                    dict(date=d, x=locals()[price].loc[d, 'x'], value=locals()[price].loc[d, price])
                )
            if len(locals()[f"{price}s"]) >= samplePoint:
                break

        slope, intercept, _, __, ___ = linregress(
            x=[h['x'] for h in locals()[f"{price}s"]], y=[h['value'] for h in locals()[f"{price}s"]]
        )
        fitted = slope * ohlcv['x'] + intercept
        fitted.name = 'resist' if price == 'high' else 'support'
        return fitted

    def calcBenchmark(self) -> pd.DataFrame:
        attr = f'__benchmark_{self.enddate}_{self.period}_{self.freq}'
        if not hasattr(self, attr):
            if self.market == 'KOR' and self.benchmarkTicker:
                df = self.fetchKrse(self.benchmarkTicker, self.startdate, self.enddate, self.freq)
            elif self.market == 'USA' and self.benchmarkTicker:
                df = self.fetchNyse(self.benchmarkTicker, self.period, self.freq)
            else:
                df = pd.DataFrame(columns=['open', 'close', 'high', 'low', 'volume'])

            ohlcv = self.getOhlcv().copy()
            objs = dict()
            for col in ohlcv.columns:
                objs[(col, self.name)] = ohlcv[col]
                objs[(col, self.benchmarkName)] = df[col]
            self.__setattr__(attr, pd.concat(objs=objs, axis=1))
        return self.__getattribute__(attr)

    def calcMA(self) -> pd.DataFrame:
        attr = f'__sma_{self.enddate}_{self.period}_{self.freq}'
        if not hasattr(self, attr):
            ohlcv = self.getOhlcv().copy()
            _t = (ohlcv.close + ohlcv.high + ohlcv.low) / 3
            self.__setattr__(
                attr,
                pd.concat(objs={f'MA({w}D)': _t.rolling(w).mean() for w in [5, 10, 20, 60, 120, 200]}, axis=1)
            )
        return self.__getattribute__(attr)

    def calcTrend(self) -> pd.DataFrame:
        attr = f'__trend_{self.enddate}_{self.period}_{self.freq}'
        if not hasattr(self, attr):
            ohlcv = self.getOhlcv().copy()
            typical = (ohlcv.close + ohlcv.high + ohlcv.low) / 3

            delta = self._deltaDate(typical, [('1Y', 365), ('6M', 183), ('3M', 92)])
            objs = [
               self._lineFit(typical, name='TL(A)'),
               self._lineFit(typical[int(typical.size / 2):], name='TL(H)'),
               self._lineFit(typical[int(typical.size * 3 / 4):], name='TL(Q)')
            ] + [self._lineFit(typical[c], name=f'TL({tag})') for c, tag, _ in delta]
            self.__setattr__(attr, round(pd.concat(objs=objs, axis=1), 2))
        return self.__getattribute__(attr)

    def calcBound(self, minInterval:int=-1, samplePoint:int=-1):
        attr = f'_bound_{self.enddate}_{self.period}_{self.freq}'
        if not hasattr(self, attr):
            ohlcv = self.getOhlcv().copy()
            ohlcv['date'] = ohlcv.index
            ohlcv['x'] = (ohlcv['date'].diff()).dt.days.fillna(1).astype(int).cumsum()

            delta = self._deltaDate(ohlcv, [('1Y', 365), ('6M', 183), ('3M', 92)])
            objs = {
                ('(A)', 'Resist'): self._boundFit(ohlcv, 'high', minInterval, samplePoint),
                ('(A)', 'Support'): self._boundFit(ohlcv, 'low', minInterval, samplePoint),
                ('(H)', 'Resist'): self._boundFit(ohlcv.tail(int(len(ohlcv) / 2)), 'high', minInterval, samplePoint),
                ('(H)', 'Support'): self._boundFit(ohlcv.tail(int(len(ohlcv) / 2)), 'low', minInterval, samplePoint),
                ('(Q)', 'Resist'): self._boundFit(ohlcv.tail(int(len(ohlcv) / 4)), 'high', minInterval, samplePoint),
                ('(Q)', 'Support'): self._boundFit(ohlcv.tail(int(len(ohlcv) / 4)), 'low', minInterval, samplePoint),
            }
            for c, tag, _ in delta:
                objs[(f'({tag})', 'Resist')] = self._boundFit(ohlcv[c], 'high', minInterval, samplePoint)
                objs[(f'({tag})', 'Support')] = self._boundFit(ohlcv[c], 'low', minInterval, samplePoint)
            self.__setattr__(attr, pd.concat(objs=objs, axis=1))
        return self.__getattribute__(attr)


if __name__ == "__main__":
    myStock = _refine('TSLA', period=1)
    print(myStock.calcBound())