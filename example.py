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

rReceipt = lw.Indicator("121Y002", "저축성수신")
# print(rReceipt)
# print(rReceipt())
rReceipt.save()

# cliKR = lw.Indicator(ticker='LORSGPNO', country='KOR')
# print(cliKR)
# print(cliKR())
# cliKR.show()

hynix = lw.Equity('000660', period=5)
# print(hynix.ohlcv)
# print(hynix.benchmark)
# print(hynix.drawDown)
# print(hynix.sma)
# print(hynix.trend)
# print(hynix.bollingerBand)
print(hynix.rsi)
# print(hynix.moneyFlow)

# hynix.ohlcv.save()
# hynix.benchmark.save()
# hynix.drawDown.save()
# hynix.sma.save()
# hynix.bollingerBand.save()
# hynix.rsi.save()

# fit = hynix.calcBound()
# from plotly import graph_objects as go
#
# fig = hynix.ohlcv.figure()
# for col in fit.columns:
#     fig.add_trace(
#         go.Scatter(
#             name=f"{col[1]}{col[0]}",
#             x=fit.index,
#             y=fit[col],
#             visible=True if col[0] == '(A)' else 'legendonly',
#             legendgroup=col[0],
#             line=dict(dash='dash', color='red' if col[1] == 'Resist' else 'blue')
#         )
#     )
# fig.show()