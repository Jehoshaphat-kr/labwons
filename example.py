import labwons as lw
import pandas as pd
import random
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
# ticker = random.sample(lw.MetaData.KRSTOCK.index.tolist(), 1)[0]
# ticker = '017670'
# equity = lw.Equity('QQQ', period=30)
equity = lw.Equity('252990')
# equity = lw.Equity('005930', period=20)
# equity = lw.Equity('000660', period=10)
# equity = lw.Equity('012330', period=10)
# equity = lw.Equity('058470', period=5)
# equity = lw.Equity(ticker, period=5)

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
# equity.ohlcv.show()
# equity.ohlcv.save()
# equity.ohlcv.c.show()
# equity.ohlcv.t.show()
# print(equity.ohlcv.continuousDays())

""" ========== < SMA > ========== """
# print(equity.sma)
# equity.sma.show()
# equity.sma.save()

""" ========== < TREND > ========== """
# print(equity.trend)
# print(equity.trend.disparate)
# print(equity.trend.intensity)
# equity.trend.show()
# equity.trend.disparate.show()
# equity.trend.save()
# equity.trend.disparate.save()

""" ========== < BENCHMARK > ========== """
# print(equity.benchmarkReturn)
# equity.benchmarkReturn.show()
# equity.benchmarkReturn.save()

""" ========== < DRAWDOWN > ========== """
# print(equity.drawDown)
# equity.drawDown.show()
# equity.drawDown.save()

""" ========== < BOLLINGER > ========== """
# print(equity.bollingerBand)
# equity.bollingerBand.show()
# equity.bollingerBand.save()

""" ========== < RSI > ========== """
# print(equity.rsi)
# equity.rsi.show()
# equity.rsi.save()

""" ========== < PSAR > ========== """
# print(equity.psar)
# equity.psar.show()
# equity.psar.save()
# print(equity.psar.pctDown2Price())

""" ========== < MACD > ========== """
# print(equity.macd)
# equity.macd.show()
# equity.macd.save()

""" ========== < MONEY FLOW > ========== """
# print(equity.moneyFlow)
# equity.moneyFlow.show()
# equity.moneyFlow.save()

""" ========== < PERFORMANCE > ========== """
# print(equity.performance)
# print(equity.performance.Q)
# equity.performance.show()
# equity.performance.Q.save()
# equity.performance.save()

""" ========== < SOUNDNESS > ========== """
# print(equity.soundness)
# print(equity.soundness.Q)
# equity.soundness.show()
# equity.soundness.save()

""" ========== < PER > ========== """
# print(equity.per)
# equity.per.show()

""" ========== < Products > ========== """
# print(equity.products)
# equity.products.show()
# equity.products.save()

""" ========== < Foreign Rate > ========== """
# print(equity.previousForeignRate)
# print(equity.foreignRate)
# equity.foreignRate.show()
# equity.foreignRate.save()

""" ========== < Consensus Price > ========== """
# print(equity.consensusPrice)
# equity.consensusPrice.show()
# equity.consensusPrice.save()

""" ========== < Consensus Profit > ========== """
# print(equity.consensusProfit)
# print(equity.consensusProfit.Q)
# equity.consensusProfit.show()
# equity.consensusProfit.save()

""" ========== < Consensus Tendency > ========== """
# print(equity.consensusTendency)
# print(equity.consensusTendency.N)
# equity.consensusTendency.show('매출')
# equity.consensusTendency.show('영업이익')
# equity.consensusTendency.show('EPS')
# equity.consensusTendency.show('PER')
# equity.consensusTendency.save()

""" ========== < Short > ========== """
# print(equity.short)
# print(equity.short._dataName_)
# print(equity.short._ticker_)
# print(equity.short._unit_)
# print(equity.short._form_)
# print(equity.short._path_)
# equity.short.show()
# equity.short.save()

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
# equity.benchmarkMultiple.show()
# equity.benchmarkMultiple.save()

""" ========== < Multiple Band > ========== """
# print(equity.multipleBand)
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
