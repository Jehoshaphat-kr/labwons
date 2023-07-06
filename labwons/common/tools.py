from typing import Union
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from xml.etree.ElementTree import ElementTree, fromstring
from plotly.subplots import make_subplots
from stocksymbol import StockSymbol
from bs4 import BeautifulSoup
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import requests, time, os, random


def int2won(x):
    if np.isnan(x):
        return np.nan
    x = int(x)
    return f'{x}억원' if x < 10000 else f'{str(x)[:-4]}조 {str(x)[-4:]}억원'

def xml2df(url: str) -> pd.DataFrame:
    exclude = ['row', 'P_STAT_CODE']

    resp = requests.get(url)
    root = ElementTree(fromstring(resp.text)).getroot()
    data = list()
    for tag in root.findall('row'):
        getter = dict()
        for n, t in enumerate([inner for inner in tag.iter()]):
            if t.tag in exclude:
                continue
            getter.update({t.tag: t.text})
        data.append(getter)

    return pd.DataFrame(data=data) if data else pd.DataFrame()

def normalize(series:pd.Series, lim:Union[list, tuple]=None) -> pd.Series:
    """
    :param series :
    :param lim    :
    :return:
    """
    lim = lim if lim else [0, 1]
    minima, maxima = tuple(lim)
    return (maxima - minima) * (series - series.min()) / (series.max() - series.min()) + minima

def normalDistribution(series:pd.Series or np.array) -> pd.Series:
    """
    Normal Distribution of Single Series Data
    :param series: Series data
    :return:
    """
    mean = np.mean(series)
    std = np.std(series)
    data = 1 / (std * np.sqrt(2 * np.pi)) * np.exp(-(series - mean) ** 2 / (2 * std ** 2))
    return pd.Series(data=data.values, index=series)

def splitSeries(sr) -> list:
    """
    Split pandas Series by NaN data
    :param sr:
    :return:
    """
    index = list(sr.index[sr.isnull().any(axis=1)]) + [sr.index[-1]]
    data = list()
    for i in range(len(index) - 2):
        split = sr[index[i]:index[i + 1]].dropna()
        if not split.empty:
            data.append(split)
    return data




# set_layout = lambda x = None: go.Layout(
#     plot_bgcolor='white',
#     height=760,
#     hovermode='x unified',
#     legend=dict(
#         font=dict(size=18),
#         orientation="h",
#         xanchor="right", x=0.97,
#         yanchor="bottom", y=1.04,
#     ),
#     xaxis=dict(
#       title="날짜",
#       showgrid=True,
#       gridcolor='lightgrey',
#       rangeselector=periods,
#       rangeslider_visible=False,
#     ),
#     yaxis=dict(
#         title='[KRW]',
#         showgrid=False,
#         gridcolor='lightgrey'
#     ),
#     yaxis2=dict(
#         showgrid=True,
#         gridcolor='lightgrey',
#         zeroline=True,
#         zerolinecolor='lightgrey',
#         zerolinewidth=1.0,
#         autorange=True,
#     ),
# )
#
# def trace_candle(df:pd.DataFrame, **kwargs) -> go.Candlestick:
#     """
#     Trace Candle
#     :param df: DataFrame Data
#     :return:
#     """
#     trace = go.Candlestick(
#         x=df.index,
#         open=df.open,
#         high=df.high,
#         low=df.low,
#         close=df.close,
#         visible=True,
#         showlegend=True,
#         increasing_line=dict(
#             color='red'
#         ),
#         decreasing_line=dict(
#             color='royalblue'
#         ),
#         xhoverformat='%Y/%m/%d',
#         yhoverformat=kwargs['yhoverformat'] if 'yhoverformat' in kwargs else '.2f',
#     )
#     for key in kwargs:
#         if key in vars(go.Candlestick).keys():
#             setattr(trace, key, kwargs[key])
#     return trace
#
# def trace_line(series:pd.Series, **kwargs) -> go.Scatter:
#     """
#     Trace Line
#     :param series: Series Data
#     :return:
#     """
#     if series.empty or len(series) < 2:
#         return go.Scatter()
#     if "drop" in kwargs:
#         series = series.dropna()
#     trace = go.Scatter(
#         name=kwargs['name'] if 'name' in kwargs else series.name,
#         x=series.index,
#         y=series,
#         mode='lines',
#         visible=True,
#         showlegend=True,
#         connectgaps=True,
#         xhoverformat='%Y/%m/%d',
#         yhoverformat='.2f',
#         hovertemplate=f'{kwargs["name"] if "name" in kwargs else series.name}'
#                       '<br>%{y}' + f'{kwargs["unit"] if "unit" in kwargs else ""}' + '@%{x}<extra></extra>'
#     )
#     for key in kwargs:
#         if key in vars(go.Scatter).keys():
#             setattr(trace, key, kwargs[key])
#     return trace
#
# def trace_bar(series:pd.Series, **kwargs) -> go.Bar:
#     """
#     Trace Bar
#     :param series: Series Data
#     :param kwargs: keyword arguments
#     :return:
#     """
#     trace = go.Bar(
#         name=series.name,
#         x=series.index,
#         y=series,
#         visible=True,
#         showlegend=False if (kwargs['name'] if 'name' in kwargs else series.name) == 'volume' else True,
#         xhoverformat='%Y/%m/%d',
#         marker=dict(
#             dict(color=series.pct_change().apply(lambda x: 'royalblue' if x < 0 else 'red'))
#         ) if (kwargs['name'] if 'name' in kwargs else series.name) == 'volume' else None,
#         hovertemplate=f'{kwargs["name"] if "name" in kwargs else series.name}'
#                       '<br>%{y}' + f'{kwargs["unit"] if "unit" in kwargs else ""}' + '@%{x}<extra></extra>'
#     )
#     for key in kwargs:
#         if key in vars(go.Bar).keys():
#             setattr(trace, key, kwargs[key])
#     return trace
#
#
# class _corr(object):
#     def __init__(
#         self,
#         comparator: pd.Series or np.array, # Usually Indicator or Index
#         comparatee: pd.Series or np.array, # Usually Prices
#         comparator_name: str = "Comparator",
#         comparatee_name: str = "Comparatee",
#         month: int = 6
#     ):
#         self.x, self.y = comparatee, comparator
#         self.xname, self.yname = comparatee_name, comparator_name
#         self.df = pd.concat(objs=dict(x=self.x, y=self.y), axis=1).dropna()
#         self.month = month
#         return
#
#     @property
#     def coeff(self) -> float:
#         return round(self.df.x.corr(self.df.y), 6)
#
#     @property
#     def coeff_shift(self):
#         return self.coeff_frame[self.coeff_frame.shift_coeff == self.coeff_frame.shift_coeff.max()]
#
#     @property
#     def coeff_frame(self) -> pd.DataFrame:
#         if not hasattr(self, '__coeff_frame'):
#             data = list()
#             win = len(self.df[self.df.index >= (self.df.index[-1] - relativedelta(months=self.month))])
#             for n in range(-win, win + 1, 1 if win < 10 else 10):
#                 y = self.df.y.shift(n).dropna()
#                 df = pd.concat(objs=dict(x=self.df.x, y=y), axis=1).dropna()
#                 data.append(dict(
#                     shift_points=n,
#                     shift_days=-(self.df.x.index[-1 if n <= 0 else 0] - y.index[-1 if n <= 0 else 0]).days,
#                     shift_coeff=round(df.x.corr(df.y), 6),
#                     sample_size=len(df)
#                 ))
#             self.__setattr__('__coeff_frame', pd.DataFrame(data=data))
#         return self.__getattribute__('__coeff_frame')
#
#
# class corr(_corr):
#
#     def _source(self, mode:str=str(), shift:int=0) -> pd.DataFrame:
#         if mode.lower().startswith('norm'):
#             df = pd.concat(objs=dict(x=normalize(self.x, [-1, 1]), y=normalize(self.y, [-1, 1])), axis=1).dropna()
#             df = df.diff() if 'diff' in mode.lower() else df
#         elif mode.lower().startswith('diff'):
#             df = self.df.diff()
#         else:
#             df = self.df
#
#         if shift:
#             return pd.concat(objs=dict(x=df.x, y=df.y.shift(shift)), axis=1).dropna()
#         return df
#
#     def scatter(self, mode:str=str(), shift:int=0, show:bool=True) -> go.Figure:
#         df = self._source(mode=mode, shift=shift)
#         x_range = [0.95*df.x.min(), 1.05*df.x.max()]
#         y_range = [0.95*df.y.min(), 1.05*df.y.max()]
#         norm_x = normdist(df.x)
#         norm_y = normdist(df.y)
#
#         fig = make_subplots(
#             rows=2, cols=2,
#             row_heights=[0.85, 0.15],
#             column_widths=[0.08, 0.92],
#             vertical_spacing=0.0,
#             horizontal_spacing=0.0,
#             shared_xaxes=False,
#             shared_yaxes=False,
#             x_title=self.xname, y_title=f"{self.yname}{'' if not shift else f'_({shift})Shifted'}"
#         )
#
#         text = f"All : {round(df.x.corr(df.y), 4)} #{len(df)}<br>"
#         for name, n in [('All', 0), ('R-10Y', 10), ('R-5Y', 5), ('R-3Y', 3)]:
#             _df = df[df.index >= (df.index[-1] - timedelta(365 * n))].copy() if n else df
#             if n:
#                 text += f"{n}Y : {round(_df.x.corr(_df.y), 4)} #{len(_df)}<br>"
#             fig.add_trace(
#                 go.Scatter(
#                     name=name,
#                     x=_df.x,
#                     y=_df.y,
#                     showlegend=True,
#                     visible=True if not n else 'legendonly',
#                     mode='markers',
#                     marker=dict(symbol='circle-open', size=10) if n else None,
#                     text=_df.index.strftime("%Y/%m/%d"),
#                     hovertemplate="%{text}<br>x:%{x:.4f}<br>y:%{y:.4f}<extra></extra>"
#                 ), row=1, col=2
#             )
#         fig.add_vline(x=df.x.mean(), line_color='black', line_dash='dot', line_width=0.5, row=1, col=2)
#         fig.add_hline(y=df.y.mean(), line_color='black', line_dash='dot', line_width=0.5, row=1, col=2)
#         fig.add_trace(
#             go.Scatter(
#                 x=norm_x.index,
#                 y=norm_x,
#                 showlegend=False,
#                 visible=True,
#                 mode='markers',
#                 marker=dict(color='grey'),
#                 hovertemplate="x: %{x}<br>y: %{y}<extra></extra>"
#             ), row=2, col=2
#         )
#         fig.add_trace(
#             go.Scatter(
#                 x=norm_y,
#                 y=norm_y.index,
#                 showlegend=False,
#                 mode='markers',
#                 marker=dict(color='grey'),
#                 hovertemplate="y: %{y}<br>x: %{x}<extra></extra>"
#             ), row=1, col=1
#         )
#         fig.update_layout(
#             plot_bgcolor='white',
#             legend=dict(
#                 orientation='h',
#                 xanchor='right', x=1.0,
#                 yanchor='bottom', y=1.0
#             ),
#             xaxis1=dict(
#                 showticklabels=False,
#                 showgrid=False,
#                 zeroline=True,
#                 zerolinecolor='lightgrey',
#             ),
#             xaxis2=dict(
#                 showticklabels=False,
#                 showgrid=True,
#                 gridcolor='lightgrey',
#                 zeroline=True,
#                 zerolinecolor='lightgrey',
#                 showline=True,
#                 linecolor='black',
#                 range=x_range,
#                 # matches='x1',
#             ),
#             xaxis3=dict(showticklabels=False, matches='x2'),
#             xaxis4=dict(
#                 showticklabels=True,
#                 showgrid=True,
#                 gridcolor='lightgrey',
#                 zeroline=True,
#                 zerolinecolor='lightgrey',
#                 range=x_range,
#                 matches='x3',
#             ),
#             yaxis1=dict(
#                 showticklabels=True,
#                 showgrid=True,
#                 gridcolor='lightgrey',
#                 zeroline=True,
#                 zerolinecolor='lightgrey',
#                 range=y_range,
#                 matches='y2'
#             ),
#             yaxis2=dict(
#                 showticklabels=False,
#                 showgrid=True,
#                 gridcolor='lightgrey',
#                 zeroline=True,
#                 zerolinecolor='lightgrey',
#                 showline=True,
#                 linecolor='black',
#                 anchor='x2',
#                 range=y_range,
#                 matches='y1'
#             ),
#             yaxis3=dict(showticklabels=False, matches=None),
#             yaxis4=dict(
#                 showticklabels=False,
#                 showgrid=False,
#                 zeroline=True,
#                 zerolinecolor='lightgrey',
#                 anchor='x4',
#                 matches=None
#             ),
#         )
#         fig.add_annotation(
#             row=2, col=1,
#             showarrow=False,
#             # x=-0.5, y=-0.5,
#             # xanchor='left', yanchor='bottom',
#             text=text,
#             align="left"
#         )
#         if show:
#             fig.show()
#         return fig
#
#     def shift(self, show:bool=True):
#         fig = make_subplots(
#             rows=1, cols=1,
#             specs=[[{'secondary_y':True}]]
#         )
#         fig.add_trace(
#             go.Scatter(
#                 name=self.xname,
#                 x=self.df.x.index,
#                 y=self.df.x,
#                 showlegend=False,
#                 visible=True,
#                 mode='lines',
#                 line=dict(color='black'),
#                 hovertemplate=self.xname + '<br>%{y}@%{x}<extra></extra>'
#             ), secondary_y=False
#         )
#         fig.add_hline(y=self.df.x.mean(), line_dash='dot', line_width=0.8, line_color='grey', secondary_y=False)
#         fig.add_trace(
#             go.Scatter(
#                 name=self.yname,
#                 x=self.df.y.index,
#                 y=self.df.y,
#                 showlegend=True,
#                 visible=True,
#                 mode='lines',
#                 line=dict(color='grey', dash='dash'),
#                 hovertemplate=f"{self.yname}" + "<br>%{y}@%{x}<extra></extra>"
#             ), secondary_y=True
#         )
#
#         win = len(self.df[self.df.index >= (self.df.index[-1] - relativedelta(months=self.month))])
#         for n in range(-win, win + 1, 1 if win < 10 else 10):
#             if not n :
#                 continue
#             df = self._source(mode='default', shift=n)
#             fig.add_trace(
#                 go.Scatter(
#                     name=f"Shift:{n}",
#                     x=df.index,
#                     y=df.y,
#                     showlegend=True,
#                     visible=True if n == 0 else 'legendonly',
#                     mode='lines',
#                     line=dict(dash='dot', color='royalblue') if n == 0 else None,
#                     hovertemplate=f"{self.yname}({n})Shifted" + "<br>%{y}@%{x}<extra></extra>"
#                 ), secondary_y=True
#             )
#
#         fig.update_layout(
#             plot_bgcolor='white',
#             margin=dict(r=0),
#             legend=dict(
#                 orientation='h',
#                 xanchor='right', x=0.95,
#                 yanchor='bottom', y=1.0
#             ),
#             xaxis=dict(
#                 title='날짜',
#                 showticklabels=True,
#                 tickformat='%Y/%m/%d',
#                 showgrid=True,
#                 gridcolor='lightgrey',
#             ),
#             yaxis=dict(
#                 title=self.xname,
#                 showticklabels=True,
#                 showgrid=True,
#                 gridcolor='lightgrey',
#                 zeroline=True,
#                 zerolinecolor='lightgrey',
#                 zerolinewidth=1.0
#             ),
#             yaxis2=dict(
#                 title=self.yname
#             )
#         )
#
#         if show:
#             fig.show()
#         return fig
#
#     def shift_histogram(self, show:bool=True):
#         df = self.coeff_frame
#         data = go.Bar(
#             name='histogram',
#             x=df['shift_days'],
#             y=df['shift_coeff'],
#             showlegend=False,
#             visible=True,
#             text='',
#             meta=df['shift_points'],
#             hovertemplate='%{y}<br>Shifted: %{x} days(n = %{meta})<extra></extra>'
#         )
#         fig = go.Figure(
#             data=data,
#             layout=go.Layout(
#                 plot_bgcolor='white',
#                 xaxis=dict(
#                     title='(-): Lag <-- <b>Shifted Days</b> --> (+): Lead',
#                     showticklabels=True,
#                     showgrid=False,
#                 ),
#                 yaxis=dict(
#                     title='Correlation Coefficient [-]',
#                     showticklabels=True,
#                     showgrid=True,
#                     gridcolor='lightgrey',
#                     zeroline=True,
#                     zerolinecolor='lightgrey',
#                     zerolinewidth=1.0
#                 )
#             )
#         )
#         if show:
#             fig.show()
#         return fig

