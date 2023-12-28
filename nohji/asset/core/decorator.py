from nohji.meta import meta
from nohji.asset.core.memorize import mem


class common(property):
    def __get__(self, *args, **kwargs):
        if not hasattr(args[0], "ticker"):
            raise AttributeError("Usage of decorator @common requires 'ticker' attribute, but not found")

        if self.fget.__name__ == "ohlcv":
            __key__ = f"ohlcv_{args[0].period}_{args[0].freq}_{args[0].ticker}"
        else:
            __key__ = f"{self.fget.__name__}_{args[0].ticker}"

        if not __key__ in mem:
            mem[__key__] = super().__get__(*args, **kwargs)
        return mem[__key__]


class stockonly(property):
    def __get__(self, *args, **kwargs):
        if not hasattr(args[0], "ticker"):
            raise AttributeError("Usage of decorator @stockonly requires 'ticker' attribute, but not found")

        if not meta(args[0].ticker).quoteType.lower() == "equity":
            raise TypeError(f"Asset Type for <@ticker: {args[0].ticker}> is not Stock(Equity)")

        __key__ = f"{self.fget.__name__}_{args[0].ticker}"
        if not __key__ in mem:
            mem[__key__] = super().__get__(*args, **kwargs)
        return mem[__key__]


class etfonly(property):
    def __get__(self, *args, **kwargs):
        if not hasattr(args[0], "ticker"):
            raise AttributeError("Usage of decorator @etfonly requires 'ticker' attribute, but not found")

        if not meta(args[0].ticker).quoteType.lower() == "etf":
            raise TypeError(f"Asset Type for <@ticker: {args[0].ticker}> is not ETF")

        __key__ = f"{self.fget.__name__}_{args[0].ticker}"
        if not __key__ in mem:
            mem[__key__] = super().__get__(*args, **kwargs)
        return mem[__key__]
