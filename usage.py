from nohji import Asset

from pandas import set_option
set_option('display.expand_frame_repr', False)


asset = Asset(
    # "005930"
    # "000660"
    "006400" # 삼성SDI
    # "316140" # 우리금융지주
    # "058470" # 리노공업
    # "096770" # SK이노베이션
    # "252990"
)
# print(asset["meta"])
# print(asset["meta"]["products"])
# print(asset["businessSummary"])
# print(asset["resemblances"])


# asset.Ohlcv()
# asset.TypicalPrice()
# asset.Trend()
# asset.Deviation()
# asset.SMA()
# asset.BollingerBand()
# asset.RSI()
# asset.MACD()
# asset.PSAR()
# asset.MoneyFlow()
#
# asset.AssetQuality()
# asset.Profit()
# asset.ProfitExpenses()
# asset.Products()
# asset.MultipleBands()
# asset.ProfitEstimate()
# asset.PERs()
# asset.Consensus()
asset.ForeignRate()
# asset.Shorts()
# asset.BenchmarkMultiples()
# asset.Benchmarks()
# asset.DrawDowns()

# print(asset.Trend)
# print(asset.Deviation)
# print(asset.MultipleBands)
# print(asset.ProfitEstimate)
# print(asset.PERs)
# print(asset.Benchmarks)
# print(asset.ForeignRate)

# print(asset.Trend.stat)
# print(asset.Deviation.stat)