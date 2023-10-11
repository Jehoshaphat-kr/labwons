import labwons as lw
import pandas as pd
pd.set_option('display.expand_frame_repr', False)

lw.API.SSYM = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
lw.API.ECOS = "CEW3KQU603E6GA8VX0O9"
# lw.PATH.BASE = r"\\kefico\keti\ENT\Softroom\Temp\J.H.Lee\labwons"


"""
TEST :: INDICATORS
"""
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


"""
TEST :: EQUITIES
"""
# equity = lw.Equity('QQQ', period=30)
equity = lw.Equity('252990')
# equity = lw.Equity('005930', period=20)
# equity = lw.Equity('058470', period=20)
# equity = lw.Equity('000660', period=10)

""" ========= < Description > =========="""
# print(equity.description())

""" ========== < OHLCV > ========== """
# print(equity.ohlcv)
# print(equity.ohlcv.o)
# print(equity.ohlcv.h)
# print(equity.ohlcv.l)
# print(equity.ohlcv.c)
# print(equity.ohlcv.v)
# print(equity.ohlcv.t)
# print(equity.ohlcv._dataName_)
# print(equity.ohlcv._ticker_)
# print(equity.ohlcv._unit_)
# print(equity.ohlcv._form_)
# print(equity.ohlcv._path_)
# print(equity.ohlcv._filename_)
equity.ohlcv.show()


""" ========== < SMA > ========== """
# print(equity.sma)
# print(equity.sma._dataName_)
# print(equity.sma._ticker_)
# print(equity.sma._unit_)
# print(equity.sma._form_)
# print(equity.sma._path_)
# print(equity.sma._filename_)
# print(equity.sma.goldenCross)
# equity.sma.show()

""" ========== < TREND > ========== """
# print(equity.trend)
# print(equity.trend._dataName_)
# print(equity.trend._ticker_)
# print(equity.trend._unit_)
# print(equity.trend._form_)
# print(equity.trend._path_)
# print(equity.trend._filename_)
# print(equity.trend.flatten())
# print(equity.trend.strength())
# print(equity.trend.gaps())
# equity.trend.show()
# equity.trend.show('flat')

""" ========== < BENCHMARK > ========== """
# print(equity.benchmarkReturn)
# print(equity.benchmarkReturn._dataName_)
# print(equity.benchmarkReturn._ticker_)
# print(equity.benchmarkReturn._unit_)
# print(equity.benchmarkReturn._form_)
# print(equity.benchmarkReturn._path_)
# print(equity.benchmarkReturn._filename_)
# equity.benchmarkReturn.save()

""" ========== < DRAWDOWN > ========== """
# print(equity.drawDown)
# print(equity.drawDown._dataName_)
# print(equity.drawDown._ticker_)
# print(equity.drawDown._unit_)
# print(equity.drawDown._form_)
# print(equity.drawDown._path_)
# equity.drawDown.show()

""" ========== < BOLLINGER > ========== """
# print(equity.bollingerBand)
# print(equity.bollingerBand._dataName_)
# print(equity.bollingerBand._ticker_)
# print(equity.bollingerBand._unit_)
# print(equity.bollingerBand._form_)
# print(equity.bollingerBand._path_)
# equity.bollingerBand.show()

""" ========== < RSI > ========== """
# print(equity.rsi)
# print(equity.rsi._dataName_)
# print(equity.rsi._ticker_)
# print(equity.rsi._unit_)
# print(equity.rsi._form_)
# print(equity.rsi._path_)
# equity.rsi.show()
# equity.rsi.save()

""" ========== < PSAR > ========== """
# print(equity.psar)
# print(equity.psar._dataName_)
# print(equity.psar._ticker_)
# print(equity.psar._unit_)
# print(equity.psar._form_)
# print(equity.psar._path_)
# equity.psar.show()
# equity.psar.save()

""" ========== < MACD > ========== """
# print(equity.macd)
# print(equity.macd._dataName_)
# print(equity.macd._ticker_)
# print(equity.macd._unit_)
# print(equity.macd._form_)
# print(equity.macd._path_)
# equity.macd.show()
# equity.macd.save()

""" ========== < Financial Statement > ========== """
# print(equity.statement)
# print(equity.statement._dataName_)
# print(equity.statement._ticker_)
# print(equity.statement._unit_)
# print(equity.statement._form_)
# print(equity.statement._path_)
# equity.statement.show()
# equity.statement.save()

""" ========== < Earnings > ========== """
# print(equity.earnings)
# print(equity.earnings._dataName_)
# print(equity.earnings._ticker_)
# print(equity.earnings._unit_)
# print(equity.earnings._form_)
# print(equity.earnings._path_)
# equity.earnings.show()
# equity.statement.save()

""" ========== < Foreign Rate > ========== """
# print(equity.foreignHold)
# print(equity.foreignHold._dataName_)
# print(equity.foreignHold._ticker_)
# print(equity.foreignHold._unit_)
# print(equity.foreignHold._form_)
# print(equity.foreignHold._path_)
# equity.foreignHold.show()
# equity.foreignHold.save()

""" ========== < Consensus > ========== """
# print(equity.consensus)
# print(equity.consensus._dataName_)
# print(equity.consensus._ticker_)
# print(equity.consensus._unit_)
# print(equity.consensus._form_)
# print(equity.consensus._path_)
# equity.consensus.show()
# equity.consensus.save()

""" ========== < Short > ========== """
# print(equity.short)
# print(equity.short._dataName_)
# print(equity.short._ticker_)
# print(equity.short._unit_)
# print(equity.short._form_)
# print(equity.short._path_)
# equity.short.show()
# equity.short.save()

""" ========== < Products > ========== """
# print(equity.products)
# print(equity.products._dataName_)
# print(equity.products._ticker_)
# print(equity.products._unit_)
# print(equity.products._form_)
# print(equity.products._path_)
# equity.products.show()
# equity.products.save()

""" ========== < Expenses > ========== """
# print(equity.expense)
# print(equity.expense._dataName_)
# print(equity.expense._ticker_)
# print(equity.expense._unit_)
# print(equity.expense._form_)
# print(equity.expense._path_)
# equity.expense.show()
# equity.expense.save()

""" ========== < Benchmark Multiples > ========== """
# print(equity.benchmarkMultiple)
# print(equity.benchmarkMultiple._dataName_)
# print(equity.benchmarkMultiple._ticker_)
# print(equity.benchmarkMultiple._unit_)
# print(equity.benchmarkMultiple._form_)
# print(equity.benchmarkMultiple._path_)
# equity.benchmarkMultiple.show()
# equity.expense.save()

""" ========== < Multiple Band > ========== """
# print(equity.multipleBand)
# print(equity.multipleBand._dataName_)
# print(equity.multipleBand._ticker_)
# print(equity.multipleBand._unit_)
# print(equity.multipleBand._form_)
# print(equity.multipleBand._path_)
# equity.multipleBand.show()
# equity.expense.save()

""" ========== < Similarities > ========== """
# print(equity.similarities)
# equity.similarities.figure().show()



# print(lw.MetaData)
# print(lw.MetaData[lw.MetaData['industry'] == 'WI26 반도체'])

# print(equity.backtest)
# print(equity.trend.backTestSignal())
# equity.enddate = '20080130'
# equity.trend.show()
# equity.trend.show('flat')


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
