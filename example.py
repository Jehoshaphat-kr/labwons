import labwons as lw

lw.API.STOCK_SYMBOL = "95012214-44b0-4664-813f-a7ef5ad3b0b4"
lw.API.ECOS = "CEW3KQU603E6GA8VX0O9"

# DGS10 = lw.Indicator('DGS10')
# print(DGS10)
# print(DGS10())

# rReceipt = lw.Indicator("121Y002", "저축성수신")
# print(rReceipt)
# print(rReceipt())
# rReceipt.save()

# cliKR = lw.Indicator(ticker='LORSGPRT', country='KOR')
# print(cliKR)
# print(cliKR())
# cliKR.show()

skhynix = lw.Equity('000660')
# print(skhynix.ohlcv)
print(skhynix.typical)
# skhynix.ohlcv.save(auto_open=True)