from nohji.meta import meta
from nohji.asset.core.mem import mem


class common(property):
    def __get__(self, *args, **kwargs):
        if hasattr(args[0], "meta"):
            _meta = args[0].meta
        elif hasattr(args[0], "ticker"):
            _meta = meta(args[0].ticker)
        else:
            raise AttributeError("Usage of decorator @common requires 'ticker' or 'meta' attribute, but not found")

        if self.fget.__name__ == "ohlcv":
            __key__ = f"ohlcv_{args[0].period}_{args[0].freq}_{_meta.ticker}"
        else:
            __key__ = f"{self.fget.__name__}_{_meta.ticker}"

        if not __key__ in mem:
            mem[__key__] = super().__get__(*args, **kwargs)
        return mem[__key__]


class stockonly(property):
    def __get__(self, *args, **kwargs):
        if hasattr(args[0], "meta"):
            _meta = args[0].meta
        elif hasattr(args[0], "ticker"):
            _meta = meta(args[0].ticker)
        else:
            raise AttributeError("Usage of decorator @stockonly requires 'ticker' or 'meta' attribute, but not found")

        if not _meta.quoteType.lower() == "equity":
            raise TypeError(f"Asset Type for <@ticker: {_meta.ticker}> is not Stock(Equity)")

        __key__ = f"{self.fget.__name__}_{_meta.ticker}"
        if not __key__ in mem:
            mem[__key__] = super().__get__(*args, **kwargs)
        return mem[__key__]


class etfonly(property):
    def __get__(self, *args, **kwargs):
        if hasattr(args[0], "meta"):
            _meta = args[0].meta
        elif hasattr(args[0], "ticker"):
            _meta = meta(args[0].ticker)
        else:
            raise AttributeError("Usage of decorator @etfonly requires 'ticker' or 'meta' attribute, but not found")

        if not _meta.quoteType.lower() == "etf":
            raise TypeError(f"Asset Type for <@ticker: {_meta.ticker}> is not ETF")

        __key__ = f"{self.fget.__name__}_{_meta.ticker}"
        if not __key__ in mem:
            mem[__key__] = super().__get__(*args, **kwargs)
        return mem[__key__]


class krmarket(property):
    def __get__(self, *args, **kwargs):
        if hasattr(args[0], "meta"):
            _meta = args[0].meta
        elif hasattr(args[0], "ticker"):
            _meta = meta(args[0].ticker)
        else:
            raise AttributeError("Usage of decorator @krmarket requires 'ticker' or 'meta' attribute, but not found")

        if not _meta.country == "KOR":
            raise TypeError(f"Asset listed Country is not KOR")
        __key__ = f"{self.fget.__name__}_{_meta.ticker}"
        if not __key__ in mem:
            mem[__key__] = super().__get__(*args, **kwargs)
        return mem[__key__]


# def memorize(cls):
#     def wrapper(*args, **kwargs):
#         inst = cls(*args, **kwargs)
#         if hasattr(inst, "meta"):
#             _meta = inst.meta
#         elif hasattr(inst, "ticker"):
#             _meta = meta(inst.ticker)
#         else:
#             raise AttributeError(f"Cannot memorize <class; {cls.__name__}>, due to missing attribute @meta or @ticker")
#
#         __key__ = f"{cls.__name__}_{_meta.ticker}"
#         if not __key__ in mem:
#             mem[__key__] = inst
#         return inst
#     return wrapper