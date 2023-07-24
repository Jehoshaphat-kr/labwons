import labwons as lw
import pandas as pd
pd.set_option('display.expand_frame_repr', False)

lw.API.STOCK_SYMBOL = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
lw.API.ECOS = "CEW3KQU603E6GA8VX0O9"
lw.PATH.BASE = r"\\kefico\keti\ENT\Softroom\Temp\J.H.Lee\labwons"

# DGS10 = lw.Indicator('DGS10')
# print(DGS10)
# print(DGS10())
# DGS10.show()
# DGS10.Monthly.show()
# DGS10.MoM.show()
# DGS10.YoY.show()

# rReceipt = lw.Indicator("121Y002", "저축성수신")
# print(rReceipt)
# print(rReceipt())
# rReceipt.save()

# cliKR = lw.Indicator(ticker='LORSGPNO', country='KOR')
# print(cliKR)
# print(cliKR())
# cliKR.show()

equity = lw.Equity('058470', period=5)
# print(equity.longName)
# print(equity.businessSummary)
# print(equity.ohlcv)
# print(equity.benchmark)
# print(equity.drawDown)
# print(equity.sma)
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
print(equity.benchmarkMultiple)

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

# equity.foreigner.show()
# equity.products.show()
# equity.consensus.show()
# equity.short.show()
# equity.expense.show()
