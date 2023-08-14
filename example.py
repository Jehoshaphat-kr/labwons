import labwons as lw
import pandas as pd
pd.set_option('display.expand_frame_repr', False)

lw.API.SSYM = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
lw.API.ECOS = "CEW3KQU603E6GA8VX0O9"
# lw.PATH.BASE = r"\\kefico\keti\ENT\Softroom\Temp\J.H.Lee\labwons"

# DGS10 = lw.Indicator('DGS10')
# print(DGS10)
# print(DGS10())
# DGS10.show()
# print(DGS10.M())
# DGS10.M.show()
# print(DGS10.MoM())
# DGS10.MoM.show()
# print(DGS10.YoY())
# DGS10.YoY.show()

# rReceipt = lw.Indicator("121Y002", "저축성수신")
# print(rReceipt)
# print(rReceipt())
# rReceipt.save()

"""
1) BSCICP03: OECD Standardised BCI, Amplitude adjusted(Long term average = 100), sa
2) CSCICP03: OECD Standardised CCI, Amplitude adjusted(Long term average = 100), sa
3) LOLITOAA: Amplitude adjusted(CLI)
4) LOLITONO: Normalised(CLI)
5) LOLITOTR_STSA: Trend restored(CLI)
6) LOLITOTR_GYSA: 12 - month rate of change of the trend restored CLI
7) LORSGPRT: Ratio to trend(GDP)
8) LORSGPNO: Normalised(GDP)
9) LORSGPTD: Trend(GDP)
"""
# cliKR = lw.Indicator(ticker='LOLITONO', source='OECD', country='KOR', name='OECD CLI')
# print(cliKR)
# print(cliKR())
# cliKR.show()

# import random
# for ticker in ['SPY', 'QQQ', 'AAPL', 'AMZN', 'KO', 'NVDA', 'TSLA', 'MSFT', 'WMT', 'GOOG']:
#     date = f"{random.randint(2018, 2022)}{str(random.randint(1, 12)).zfill(2)}10"
#     print(ticker, date)
#     equity = lw.Equity(ticker, period=30)
#     equity.enddate = date
#     equity.trend.save(filename=f'TREND{date}')
#     equity.trend.save('flat', filename=f'TREND_F{date}')
#
#     equity.enddate = ''
#     equity.trend.save()

equity = lw.Equity('QQQ', period=30)
# equity = lw.Equity('005930', period=20)
# equity = lw.Equity('005930', period=10)
# equity = lw.Equity('000660', period=10)
# print(equity.longName)
# print(equity.businessSummary)
# print(equity.backtest)
# print(equity.ohlcv)
# print(equity.ohlcv.o)
# print(equity.ohlcv.h)
# print(equity.ohlcv.l)
# print(equity.ohlcv.c)
# print(equity.ohlcv.v)
# print(equity.ohlcv.t)
# print(equity.sma)
# print(equity.sma.goldenCross())
# print(equity.trend)
# print(equity.trend.flatten())
# print(equity.trend.strength())
# print(equity.trend.backTestSignal())
equity.enddate = '20080130'
equity.trend.show()
equity.trend.show('flat')


# print(equity.benchmark)
# print(equity.drawDown)

# print(equity.trend)
# print(equity.trend.flatten())
# print(equity.bollingerBand)
# print(equity.rsi)
# print(equity.moneyFlow)
# print(equity.psar)
# for up in equity.psar.upsides:
#     print(up)
# for dn in equity.psar.downsides:
#     print(dn)
# print(equity.macd)
# print(equity.foreigner)
# print(equity.products)
# print(equity.consensus)
# print(equity.short)
# print(equity.expense)
# print(equity.multipleBand)
# print(equity.benchmarkMultiple)
# print(equity.performance)
# print(equity.statement)

# equity.ohlcv.save()
# equity.ohlcv.o.save()
# equity.ohlcv.t.save()
# equity.sma.save()
# equity.trend.save()
# equity.trend.save('flat')
# equity.benchmark.save()
# equity.drawDown.save()
# equity.sma.save()
# equity.bollingerBand.save()
# equity.rsi.save()
# equity.moneyFlow.save()
# equity.psar.save()
# equity.macd.save()
# equity.foreigner.save()
# equity.expense.save()
# equity.multipleBand.save()

# equity.ohlcv.show()
# equity.trend.show()
# equity.trend.show('flat')
# equity.trend.show('flat', ['A', 'H', 'Q', '5Y', '3Y', '1Y'])
# equity.foreigner.show()
# equity.products.show()
# equity.consensus.show()
# equity.short.show()
# equity.expense.show()
# equity.benchmarkMultiple.show()
# equity.performance.show()
# equity.statement.show()

# signaled = equity.backtest.addSignal(
    # equity.sma.goldenCross['longTerm']
    # equity.trend.backTestSignal()
# )
# equity.backtest.figure('line').show()
# equity.backtest.figure('box').show()
# equity.backtest.figure('sig').show()
# df = equity.backtest.evaluate()
# print(df)

# equity.trend.show()
# import plotly.graph_objects as go
#
# backtest = pd.concat([equity.backtest['1Y'], equity.trend.backTest()], axis=1)
# print(backtest)
# print(backtest.sort_values(by='Score').dropna().head(10))
# fig = go.Figure()
# fig.add_trace(
#     go.Scatter(
#         x=backtest['Score'],
#         y=backtest['Avg.Return'],
#         mode='markers',
#         meta=backtest.index,
#         hovertemplate='%{meta:%Y/%m/%d}<br>%{y:.2f}%<extra></extra>'
#     )
# )
# fig.show()


# corr = Correlation(
#     d1=Equity('316140'),
#     d2=Indicator('121Y002', '저축성수신(금융채 제외) 1)')
# )
# equity = lw.Equity('105560')
# rx = lw.Indicator('121Y002', '저축성수신(금융채 제외) 1)', name='수신금리', unit='%')
# tx = lw.Indicator('121Y006', '대출평균 1)', name='여신금리', unit='%')
# mg = lw.Indicator(series=(tx - rx), name='예대금리차', unit='%')
# chart = lw.MultiChart(equity, rx, tx, mg)
# kbfinance = lw.Equity('105560')
# samsung = lw.Equity('005930')
# chart = lw.MultiChart(kbfinance, samsung)
# chart.show()
