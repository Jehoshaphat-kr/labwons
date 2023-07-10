"""
LABoratory WONS: Snowball Your Asset
Author  : LEE JE HYEUK
Web     : https://labwons.com
Contact : jhlee_0319@naver.com
License : MIT
"""
from labwons.common.metadata.metadata import MetaData
from labwons.indicator.indicator import Indicator
from labwons.equity.equity import Equity

""" API Settings """
class __apikey__(object):
    @property
    def STOCK_SYMBOL(self) -> str:
        if not hasattr(self, '__stock_symbol__'):
            raise KeyError('NOT FOUND: Stock Symbol API key')
        return self.__getattribute__('__stock_symbol__')

    @STOCK_SYMBOL.setter
    def STOCK_SYMBOL(self, key:str):
        self.__setattr__('__stock_symbol__', key)
        MetaData.API_STOCK_SYMBOL = key
        return

    @property
    def ECOS(self) -> str:
        if not hasattr(self, '__ecos__'):
            raise KeyError('NOT FOUND: ECOS API key')
        return self.__getattribute__('__ecos__')

    @ECOS.setter
    def ECOS(self, key:str):
        self.__setattr__('__ecos__', key)
        MetaData.API_ECOS = key
        return

API = __apikey__()