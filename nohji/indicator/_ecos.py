from nohji.util.tools import xml2df

from pandas import DataFrame, Series, to_datetime
from typing import Any


class _ecos:
    """
    ECOS (Bank of Korea, Economic Statistics System) Provided data
    * API key required for this <class; ecos>

    @data:
        type        : DataFrame
        description : listed economic index with implicit information
        example     :
                                                       name  cycle        by
            symbol
            102Y004   본원통화 구성내역(평잔, 계절조정계열)      M      None
            102Y002         본원통화 구성내역(평잔, 원계열)      M      None
            102Y003   본원통화 구성내역(말잔, 계절조정계열)      M      None
            102Y001         본원통화 구성내역(말잔, 원계열)      M  한국은행
            101Y018  M1 상품별 구성내역(평잔, 계절조정계열)      M      None
            ...                                         ...    ...       ...
            251Y003                                    총량      A      None
            251Y002                          한국/북한 배율      A      None
            251Y001            북한의 경제활동별 국내총생산      A  한국은행
            252Y001                            시장물가지수      Q  한국은행
            252Y002                                시장환율      Q  한국은행

    @contains:
        type        : Callable
        description : layered list of @data
        example     :
            ''' self.contains("252Y001") '''
                  이름     코드  주기    시점    종점  개수
            0   총지수  A110000     A    2006    2022    17
            1   총지수  A110000     Q  2006Q1  2022Q4    68
            2   식료품  A111000     A    2006    2022    17
            3   식료품  A111000     Q  2006Q1  2022Q4    68
            4     곡물  A111100     A    2006    2022    17
            ..     ...      ...    ..     ...     ...    ..
            83    석탄  B121200     Q  2006Q1  2022Q4    68
            84  휘발유  B121300     A    2006    2022    17
            85  휘발유  B121300     Q  2006Q1  2022Q4    68
            86    경유  B121400     A    2006    2022    17
            87    경유  B121400     Q  2006Q1  2022Q4    68

    @fetch:
        type        : Callable
        description : time-series data of given symbol
                      return priority to the data majority (the number of dataset), not controllable
        example     :
            ''' self.fetch("252Y001", "총지수") '''
            time
            2006-03-31      0.073
            2006-06-30      0.077
            2006-09-30      0.075
            2006-12-31      0.082
            2007-03-31      0.101
                           ...
            2021-12-31    116.100
            2022-03-31    107.600
            2022-06-30    127.600
            2022-09-30    121.700
            2022-12-31    120.600
            Freq: Q-DEC, Name: 총지수, Length: 68, dtype: float64
    """
    _api_:str = ""
    _src_:DataFrame = DataFrame()
    def __init__(self):
        return

    def __call__(self, symbol:str, *args) -> Series:
        return self.fetch(symbol, *args)

    def __contains__(self, item):
        return item in self.src.index

    def __repr__(self) -> str:
        return repr(self.src)

    def __getitem__(self, item:Any):
        return self.src[item]

    def __iter__(self):
        return iter(self.src)

    def __len__(self):
        return len(self.src)

    @property
    def api(self) -> str:
        return self._api_

    @api.setter
    def api(self, key: str):
        self._api_ = key

    @property
    def src(self) -> DataFrame:
        if self._src_.empty:
            columns = {
                "STAT_CODE": "symbol",
                "STAT_NAME": "name",
                "CYCLE": "cycle",
                "ORG_NAME": "by"
            }
            url = f'http://ecos.bok.or.kr/api/StatisticTableList/{self.api}/xml/kr/1/10000/'
            data = xml2df(url=url, parser="xml")
            data = data[data.SRCH_YN == 'Y'].copy()
            data['STAT_NAME'] = data["STAT_NAME"].apply(lambda x: x[x.find(' ') + 1:])
            data = data.rename(columns=columns)
            self._src_ = data[columns.values()].set_index(keys='symbol')
        return self._src_

    def contains(self, symbol: str) -> DataFrame:
        columns = {
            "ITEM_NAME":'이름',
            "ITEM_CODE":'코드',
            "CYCLE":'주기',
            "START_TIME":'시점',
            "END_TIME":'종점',
            "DATA_CNT":'개수'
        }
        url = f"http://ecos.bok.or.kr/api/StatisticItemList/{self.api}/xml/kr/1/10000/{symbol}"
        return xml2df(url=url, parser="xml")[columns.keys()].rename(columns=columns)

    def fetch(self, symbol: str, *args) -> Series:
        contained = self.contains(symbol)

        keys = list(args)
        key = contained[contained.이름 == keys.pop(0)]
        if len(key) > 1:
            cnt = key['개수'].astype(int).max()
            key = key[key.개수 == str(cnt)]
        name, code, c, s, e, _ = tuple(key.values[0])
        code += ('/' + '/'.join([contained[(contained.이름 == l) & (contained.주기 == c)].iat[0, 1] for l in keys]))

        url = f'http://ecos.bok.or.kr/api/StatisticSearch/{self.api}/xml/kr/1/100000/{symbol}/{c}/{s}/{e}/{code}'
        fetch = xml2df(url=url, parser="xml")
        if c == "Y":
            index = to_datetime(fetch.TIME, format="%Y")
        elif c == "Q":
            split = fetch.TIME.str.split("Q", expand=True).astype(int)
            split["time"] = split[0].astype(str) + (3 * split[1]).astype(str).str.zfill(2)
            index = to_datetime(split.time, format="%Y%m")
        elif c == "M":
            index = to_datetime(fetch.TIME, format="%Y%m")
        else:
            index = to_datetime(fetch.TIME, format="%Y%m%d")
        series = Series(name=name, index=index, data=fetch.DATA_VALUE.tolist(), dtype=float)
        if c in ["Y", "Q", "M"]:
            series.index = series.index.to_period('M').to_timestamp('M')
        return series


# Alias
ecos = _ecos()


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    ecos.api = "CEW3KQU603E6GA8VX0O9"

    print(ecos)
    print(ecos.contains("252Y001"))
    print(ecos("252Y001", "총지수"))





