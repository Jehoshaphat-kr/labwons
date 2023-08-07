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

equity = lw.Equity('005930', period=10)
# print(equity.longName)
# print(equity.businessSummary)
# print(equity.ohlcv)
# print(equity.benchmark)
# print(equity.drawDown)
# print(equity.sma)
print(equity.trend)
# from datetime import timedelta
# equity.trend['5Y'] = equity.trend.add(equity.trend.index[-1] - timedelta(5 * 365), name='5Y')
# print(equity.trend)
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
