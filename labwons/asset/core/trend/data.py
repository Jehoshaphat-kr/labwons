from datetime import timedelta
from pandas import concat, DataFrame, Series
from scipy.stats import linregress


def gen(data:Series) -> DataFrame:
    def _regression_(subdata:Series, newName:str='') -> Series:
        newName = newName if newName else subdata.name
        subdata.index.name = 'date'
        subdata = subdata.reset_index(level=0)
        xrange = (subdata['date'].diff()).dt.days.fillna(1).astype(int).cumsum()

        slope, intercept, _, _, _ = linregress(x=xrange, y=subdata[subdata.columns[-1]])
        fitted = slope * xrange + intercept
        fitted.name = newName
        return concat(objs=[subdata, fitted], axis=1).set_index(keys='date')[fitted.name]

    objs = [data, _regression_(data, 'All')]
    for yy in [5, 2, 1, 0.5, 0.25]:
        col = f"{yy}Y" if isinstance(yy, int) else f"{int(yy * 12)}M"
        date = data.index[-1] - timedelta(int(yy * 365))
        if data.index[0] > date:
            objs.append(Series(name=col, index=data.index))
        else:
            objs.append(_regression_(data[data.index >= date], col))
    return concat(objs=objs, axis=1)
