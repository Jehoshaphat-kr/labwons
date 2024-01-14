

import snob as sb
# from snob import Equity, ETF, Indicator


test = sb.Equity(ticker="000660", period=10, freq="d", enddate="20230731")


# Show DataFrame
print(test.ohlcv) # test.ohlcv
print(test.asset) # test.asset


# Show Status
print(test.ohlcv.status)
print(test.asset.status)


# Show Chart
test.ohlcv.chart()
test.asset.chart()


# Abbreviation
test.abbreviate()