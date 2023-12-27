import os

class __path__:
    user     : str = os.environ["USERPROFILE"]
    desktop  : str = os.path.join(user, "Desktop")
    downloads: str = os.path.join(user, "Downloads")


class __key__:
    _ss_: str = ""
    _es_: str = ""

    @property
    def stockSymbol(self) -> str:
        if not self._ss_:
            raise KeyError("Invalid api key for <stock symbol>")
        return self._ss_

    @stockSymbol.setter
    def stockSymbol(self, key:str):
        self._ss_ = key

    @property
    def ecos(self) -> str:
        if not self._es_:
            raise KeyError("Invalid api key for <ecos>")
        return self._es_

    @ecos.setter
    def ecos(self, key:str):
        self._es_ = key


# Alias
path = __path__()
api = __key__()