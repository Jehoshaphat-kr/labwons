from nohji.indicator._ecos import ecos
from nohji.indicator._fred import fred
from nohji.indicator._oecd import oecd

from datetime import datetime
from pandas import to_datetime
from plotly.graph_objects import Bar, Scatter


class Indicator:

    def __init__(self, symbol: str, *args, period: int = 10, **kwargs):
        self.symbol = symbol
        self.period = period

        if symbol in oecd:
            if not "country" in kwargs:
                raise KeyError(f"<oecd symbol; {symbol}> requires <country:str> code, but not found.")
            self.name = oecd[symbol]["name"]
            self.data = oecd(symbol=symbol, country=kwargs["country"], period=period)
        elif symbol in ecos:
            if not args:
                raise KeyError(f"<ecos symbol; {symbol} requires subset code, but not found.")
            self.name = args[0] if not "name" in kwargs else kwargs["name"]
            self.data = ecos(symbol, *args)
        elif symbol in fred:
            self.name = fred[symbol]['name']
            self.data = fred(symbol=symbol, period=period)
        else:
            self.name = symbol
            try:
                self.data = fred(symbol=symbol, period=period)
            except IOError:
                raise IOError(f"No Such Symbol as <symbol; {symbol}> in ECOS, FRED or OECD")

        self.unit = kwargs["unit"] if "unit" in kwargs else ""

        if "by" in kwargs:
            self.data = self.data.resample(kwargs["by"]).ffill()
        if "sum_by" in kwargs:
            if kwargs["sum_by"] == "Y":
                self.data = self.data.groupby(self.data.index.year).sum()
                self.data.index = [to_datetime(f"{i}-12-31") for i in self.data.index]

        self.YoY = 100 * self.data.pct_change(12)
        self.MoM = 100 * self.data.pct_change()

        return

    def __repr__(self):
        return repr(self.data)

    def line(self, src:str="original", **kwargs) -> Scatter:
        data = self.YoY if src == "yoy" else self.MoM if src == "mom" else self.data
        name = f"{self.name}(YoY)" if src == "yoy" else f"{self.name}(MoM)" if src == "mom" else self.name
        trace = Scatter(
            name=name,
            x=data.index,
            y=data,
            visible=True,
            showlegend=True,
            hovertemplate=name + ": %{y}" + self.unit + "<extra></extra>"
        )
        for key, value in kwargs.items():
            setattr(trace, key, value)
        return trace

    def bar(self, src:str="oroginal", **kwargs) -> Bar:
        data = self.YoY if src == "yoy" else self.MoM if src == "mom" else self.data
        name = f"{self.name}(YoY)" if src == "yoy" else f"{self.name}(MoM)" if src == "mom" else self.name
        trace = Bar(
            name=name,
            x=data.index,
            y=data,
            visible=True,
            showlegend=True,
            hovertemplate=name + ": %{y}" + self.unit + "<extra></extra>"
        )
        for key, value in kwargs.items():
            setattr(trace, key, value)
        return trace

if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)
    ecos.api = "CEW3KQU603E6GA8VX0O9"


    ind = Indicator("301Y013", "경상수지", sum_by="Y")
    print(ind)
    print(ind.YoY)



# from labwons.common.metadata import metaData
# from labwons.common.config import PATH
# from labwons.common.tools import xml2df
# from labwons.common.basis import baseSeriesChart
# from pandas_datareader import get_data_fred
# from datetime import datetime, timedelta
# import pandas as pd
# import requests
#
#
# # class _fetch(pd.Series):
# class Indicator(baseSeriesChart):
#     def __init__(
#         self,
#         ticker: str,
#         *args,
#         name: str='',
#         source: str='',
#         country: str='',
#         period: int=20,
#         enddate: str='',
#         dformat: str='.2f',
#         unit: str='',
#     ):
#         if not ticker in MetaData.index and not source:
#             raise KeyError(f'@ticker: "{ticker}" NOT FOUND in metadata, @source must be specified')
#
#         source = source if source else MetaData.loc[ticker, 'exchange']
#         if source.lower() == 'oecd' and not country:
#             raise KeyError(f"OECD data requires @country symbol: ex) KOR, USA, G-20...")
#         if source.lower() == 'ecos' and not args:
#             raise KeyError(f"ECOS data requires specific parameters")
#
#         enddate = enddate if enddate else datetime.today().strftime("%Y%m%d")
#         startdate = (datetime.strptime(enddate, "%Y%m%d") - timedelta(20 * 365)).strftime("%Y%m%d")
#         name = name if name else args[-1] if args else ticker
#         if not unit and ticker in MetaData.index:
#             unit = MetaData.loc[ticker, 'unit']
#             if pd.isna(unit):
#                 unit = ''
#
#         if source.lower() == 'ecos':
#             series = self.fetchEcos(MetaData.API_ECOS, ticker, startdate, *args)
#         elif source.lower() == 'oecd':
#             series = self.fetchOecd(ticker, startdate, enddate, country)
#         elif source.lower() == 'fred':
#             series = self.fetchFred(ticker, startdate, enddate)
#         else:
#             raise KeyError(f'Invalid @source: "{source}", possible source is ["fred", "ecos", "oecd"]')
#         M = series.resample('M').ffill()
#         super().__init__(series, name=name, dtype=dformat, unit=unit, path=PATH())
#
#         self.ticker = ticker
#         self.name = name
#         self.startdate = startdate
#         self.enddate = enddate
#         self.period = period
#         self.source = source
#         self.dformat = dformat
#         self.unit = unit
#         self.M = baseSeriesChart(M, name=f'{ticker}(M)', dtype=dformat, unit=unit, path=PATH())
#         self.MoM = baseSeriesChart(100 * M.pct_change(), name=f'{ticker}(MoM)', dtype='.2f', unit='%', path=PATH())
#         self.YoY = baseSeriesChart(100 * M.pct_change(12), name=f'{ticker}(YoY)', dtype='.2f', unit='%', path=PATH())
#         return
