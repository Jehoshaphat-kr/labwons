from labwons.equity.fetch import fetch
from datetime import timedelta
from scipy.stats import linregress
from ta import add_all_ta_features
import pandas as pd
import numpy as np


class _calc(fetch):

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

    def calcBound(self, minInterval:int=-1, samplePoint:int=-1) -> pd.DataFrame:
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
