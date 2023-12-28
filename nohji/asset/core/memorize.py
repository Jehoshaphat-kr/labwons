from typing import Any, Dict


class _mem(object):
    __mem__:Dict[str, Any] = {}

    def __call__(self, *args, **kwargs):
        val = [self[arg] for arg in args]
        return val[0] if len(val) == 1 else val

    def __contains__(self, item:str):
        return item in self.__mem__

    def __setattr__(self, key:str, value:Any):
        self.__mem__[key] = value

    def __getattr__(self, item:str) -> Any:
        return self.__mem__[item]

    def __setitem__(self, key:str, value:Any):
        self.__mem__[key] = value

    def __getitem__(self, item) -> Any:
        return self.__mem__[item]

    def __iter__(self):
        return iter(self.__mem__)

    def __len__(self) -> int:
        return len(self.__mem__)

# Alias
mem = _mem()