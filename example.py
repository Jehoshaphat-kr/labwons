import labwons as lw

lw.API.STOCK_SYMBOL = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
lw.API.ECOS = "CEW3KQU603E6GA8VX0O9"

DGS10 = lw.Indicator('DGS10')
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

hynix = lw.Equity('000660', period=5)
# print(hynix.ohlcv)
# print(hynix.benchmark)
# print(hynix.drawdown)
# print(hynix.sma)
# print(hynix.trend)

# hynix.ohlcv.save()
# hynix.benchmark.save()
# hynix.drawdown.save()
# hynix.sma.save()

fit = hynix.calcBound()
from plotly import graph_objects as go

fig = hynix.ohlcv.figure()
for col in fit.columns:
    fig.add_trace(
        go.Scatter(
            name=f"{col[1]}{col[0]}",
            x=fit.index,
            y=fit[col],
            visible=True if col[0] == '(A)' else 'legendonly',
            legendgroup=col[0],
            line=dict(dash='dash', color='red' if col[1] == 'Resist' else 'blue')
        )
    )
fig.show()