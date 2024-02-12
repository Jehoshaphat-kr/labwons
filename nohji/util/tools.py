from nohji.util.web import web
from pandas import DataFrame
from numpy import isnan, nan
from xml.etree.ElementTree import ElementTree, fromstring
from typing import Iterable, Union


def int2won(x) -> Union[str, Iterable]:
    if isnan(x) or (not x):
        return nan
    s = '-' if int(x) < 0 else ''
    x = abs(int(x))
    if x < 10000:
        return f'{s}{x}억'
    else:
        zo = str(x)[:-4]
        ek = str(x)[-4:]
        while ek.startswith('0'):
            ek = ek[1:]
        return f'{s}{zo}조 {ek}억'

def str2num(src:str) -> int or float:
    if isinstance(src, float):
        return src
    src = "".join([char for char in src if char.isdigit() or char == "."])
    if not src or src == ".":
        return nan
    if "." in src:
        return float(src)
    return int(src)

def xml2df(url: str, parser:str="") -> DataFrame:
    exclude = ['row', 'P_STAT_CODE']
    resp = web.html(url, parser)
    root = ElementTree(fromstring(str(resp))).getroot()
    data = list()
    for tag in root.findall('row'):
        getter = dict()
        for n, t in enumerate([inner for inner in tag.iter()]):
            if t.tag in exclude:
                continue
            getter.update({t.tag: t.text})
        data.append(getter)
    return DataFrame(data=data) if data else DataFrame()

def cutString(string:str, deleter:list) -> str:
    _deleter = deleter.copy()
    while _deleter:
        string = string.replace(_deleter.pop(0), '')
    return string