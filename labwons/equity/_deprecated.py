from labwons.equity.ohlcv import _ohlcv
from datetime import timedelta
from scipy.stats import linregress
from ta import add_all_ta_features
import pandas as pd
import numpy as np


class _calc(_ohlcv):

    # @staticmethod
    # def _deltaDate(series: pd.Series or pd.DataFrame, delta: list) -> list:
    #     return [(series.index >= (series.index[-1] - timedelta(day)), tag, day) for tag, day in delta]
    #
    # @staticmethod
    # def _lineFit(series: pd.Series, **kwargs) -> pd.Series:
    #     series = series.copy()
    #     series.index.name = 'time'
    #     series.name = 'data'
    #     series = series.reset_index(level=0)
    #
    #     xrange = (series['time'].diff()).dt.days.fillna(1).astype(int).cumsum()
    #     slope, intercept, _, __, ___ = linregress(x=xrange, y=series['data'])
    #     fitted = slope * xrange + intercept
    #     fitted.name = kwargs['name'] if 'name' in kwargs else 'fitted'
    #     return pd.concat(objs=[series, fitted], axis=1)[['time', fitted.name]].set_index(keys='time')

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

    def _calcTrend(self) -> pd.DataFrame:
        attr = f'__trend_{self.enddate}_{self.period}_{self.freq}'
        if not hasattr(self, attr):
            ohlcv = self.getOhlcv().copy()
            typical = (ohlcv.close + ohlcv.high + ohlcv.low) / 3

            delta = self._deltaDate(typical, [('3Y', 365 * 3),('1Y', 365), ('6M', 183)])
            objs = [
               self._lineFit(typical, name='A'),
               self._lineFit(typical[int(typical.size / 2):], name='H'),
               self._lineFit(typical[int(typical.size * 3 / 4):], name='Q')
            ] + [self._lineFit(typical[c], name=tag) for c, tag, _ in delta]
            self.__setattr__(attr, round(pd.concat(objs=objs, axis=1), 2))
        return self.__getattribute__(attr)

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

    def calcBollingerBand(self) -> pd.DataFrame:
        attr = f'_band_{self.enddate}_{self.period}_{self.freq}'
        if not hasattr(self, attr):
            bb = self.getOhlcv().copy()

            bb['typical'] = _t = (bb.close + bb.high + bb.low) / 3
            bb['middle'] = _t.typical.rolling(window=20).mean()
            bb['stdev'] = _t.typical.rolling(window=20).std()
            bb['upperband'] = bb.middle + 2 * bb.stdev
            bb['uppertrend'] = bb.middle + bb.stdev
            bb['lowertrend'] = bb.middle - bb.stdev
            bb['lowerband'] = bb.middle - 2 * bb.stdev
            bb['width'] = 100 * (4 * bb.stdev) / bb.middle
            bb['pctb'] = (
                    (bb.typical - bb.lowerband) / (bb.upperband - bb.lowerband)
            ).where(bb.upperband != bb.lowerband, np.nan)
            self.__setattr__(attr, bb)
        return self.__getattribute__(attr)


    def calcStatement(self, by:str='annual') -> pd.DataFrame:
        if not self.market == 'KOR':
            return pd.DataFrame()
        if not hasattr(self, f'__state_{by}__'):
            url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?" \
                  f"pGB=1&gicode=A{self.ticker}&cID=&MenuYn=Y&ReportGB=D&NewMenuID=Y&stkGb=701"
            html = pd.read_html(url, header=0)
            if by == 'annual':
                s = html[14] if html[11].iloc[0].isnull().sum() > html[14].iloc[0].isnull().sum() else html[11]
            elif by == 'quarter':
                s = html[15] if html[11].iloc[0].isnull().sum() > html[14].iloc[0].isnull().sum() else html[12]
            else:
                raise KeyError

            cols = s.columns.tolist()
            s.set_index(keys=[cols[0]], inplace=True)
            s.index.name = None
            if isinstance(s.columns[0], tuple):
                s.columns = s.columns.droplevel()
            else:
                s.columns = s.iloc[0]
                s.drop(index=s.index[0], inplace=True)
            self.__setattr__(f'__state_{by}__', s.T.astype(float))
        return self.__getattribute__(f'__state_{by}__')



if __name__ == "__main__":
    myStock = _calc('005930', period=1)
    # print(myStock.calcBound())
    print(myStock.calcStatement())