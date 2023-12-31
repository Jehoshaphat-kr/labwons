# """
# LABoratory WONS: Snowball Your Asset
# Author  : LEE JE HYEUK
# Web     : https://labwons.com
# Contact : jhlee_0319@naver.com
# License : MIT
# """
# from labwons.common.metadata import metaData
# from labwons.common.config import PATH
# from labwons.common.chart import Chart
# from labwons.indicator import Indicator
# from labwons.equity import Equity
# from labwons.apps.correlation import Correlation
# from labwons.apps.market import Market
#
#
# """ API Settings """
# class __apikey__(object):
#     @property
#     def SSYM(self) -> str:
#         if not hasattr(self, '__stock_symbol__'):
#             raise KeyError('NOT FOUND: Stock Symbol API key')
#         return self.__getattribute__('__stock_symbol__')
#
#     @SSYM.setter
#     def SSYM(self, key:str):
#         self.__setattr__('__stock_symbol__', key)
#         metaData.API_STOCK_SYMBOL = key
#         return
#
#     @property
#     def ECOS(self) -> str:
#         if not hasattr(self, '__ecos__'):
#             raise KeyError('NOT FOUND: ECOS API key')
#         return self.__getattribute__('__ecos__')
#
#     @ECOS.setter
#     def ECOS(self, key:str):
#         self.__setattr__('__ecos__', key)
#         metaData.API_ECOS = key
#         return
#
# API = __apikey__()