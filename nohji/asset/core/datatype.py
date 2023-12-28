from pandas import DataFrame
from typing import Iterable, List


class twoFrames(DataFrame):

    __mem__ = {"A": DataFrame(), "B": DataFrame()}
    def __init__(self, frames:Iterable[DataFrame], names:List[str]):
        super().__init__()
        return