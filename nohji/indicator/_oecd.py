from datetime import datetime, timedelta
from pandas import DataFrame, Series, to_datetime
from requests import get


class _oecd:

    _base_ = DataFrame([
        dict(
            symbol='BSCICP03',
            name='BCI',
            quoteType='INDICATOR',
            unit='-',
            comment='OECD Standard BCI, Amplitude adjusted (Long term average=100)'
        ),
        dict(
            symbol='CSCICP03',
            name='CCI',
            quoteType='INDICATOR',
            unit='-',
            comment='OECD Standard CCI, Amplitude adjusted (Long term average=100)'
        ),
        dict(
            symbol='LOLITOAA',
            name='CLI(AA)',
            quoteType='INDICATOR',
            unit='-',
            comment='Amplitude adjusted (CLI)'
        ),
        dict(
            symbol='LOLITONO',
            name='CLI(Norm)',
            quoteType='INDICATOR',
            unit='-',
            comment='Normalised (CLI)'
        ),
        dict(
            symbol='LOLITOTR_STSA',
            name='CLI(TR)',
            quoteType='INDICATOR',
            unit='-',
            comment='Trend restored (CLI)'
        ),
        dict(
            symbol='LOLITOTR_GYSA',
            name='CLI(%TR)',
            quoteType='INDICATOR',
            unit='%',
            comment='12-month rate of change of the trend restored CLI'
        ),
        dict(
            symbol='LORSGPNO',
            name='GDP(Norm)',
            quoteType='INDICATOR',
            unit='-',
            comment='Ratio to trend (GDP)'
        ),
        dict(
            symbol='LORSGPTD',
            name='GDP(T)',
            quoteType='INDICATOR',
            unit='-',
            comment='Normalised (GDP)'
        ),
        dict(
            symbol='LORSGPRT',
            name='GDP(%T)',
            quoteType='INDICATOR',
            unit='%',
            comment='Trend (GDP)'
        ),
    ])

    def __call__(self, symbol:str, country:str, period:int=10):
        return self.fetch(symbol, country, period)

    def __contains__(self, item):
        return item in self._base_["symbol"].values

    def __repr__(self):
        return repr(self._base_)

    def __getitem__(self, item):
        return self._base_[self._base_["symbol"] == item].iloc[0]

    def fetch(self, symbol: str, country: str, period:int=10) -> Series:
        """
        :param symbol  : OECD provided data symbol
        :param country : [str] DEU@Germany, FRA@France, JPN@Japan, KOR@Korea, USA@United States, G7M@G7, G-20@G20 ...
        :param period  : [int]
        :return:
        1990-01-31     99.80950
        1990-02-28     99.74467
        1990-03-31     99.69218
                            ...
        2022-12-31     99.81123
        2023-01-31     99.72019
        2023-02-28     99.64526
        Freq: M, Name: LORSGPNO, Length: 398, dtype: float64
        """
        if not symbol in self:
            raise KeyError(f"<symbol; {symbol}> is Unknown")
        curr = datetime.today()
        prev = curr - timedelta(365 * period)
        url = f"https://stats.oecd.org/SDMX-JSON/data/MEI_CLI/" \
              f"{symbol}.{country}.M/all?" \
              f"startTime={prev.strftime('%Y-%m')}&endTime={curr.strftime('%Y-%m')}"
        load = get(url).json()

        times = [d['id'] for d in load['structure']['dimensions']['observation'][0]['values']]
        value = [v[0] for v in load['dataSets'][0]['series']['0:0:0']['observations'].values()]
        series = Series(data=value, index=times, name=symbol, dtype=float)
        series.index = to_datetime(series.index).to_period('M').to_timestamp('M')
        return series


# Alias
oecd = _oecd()


if __name__ == "__main__":
    print(oecd("LORSGPNO", "KOR"))