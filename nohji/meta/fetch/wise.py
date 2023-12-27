from nohji.util.web import web
from pandas import concat, DataFrame
from typing import Any, Dict, List
import time


class _wise:
    """
    Wise Index (FnGuide) Provided Industry/Sector Classification

    @date:
        type        : str
        description : Date of source data. Mostly recent trading date in format %Y%m%d
        example     : 231227

    @data:
        type        : DataFrame
        description : DataFrame of Wise-Classification, including ["ticker", "name", "korName", "sector", "industry"]
        example     :
                             korName     sector       industry
            ticker
            096770      SK이노베이션     에너지    WI26 에너지
            009830        한화솔루션     에너지    WI26 에너지
            010950             S-Oil     에너지    WI26 에너지
            267250            HD현대     에너지    WI26 에너지
            078930                GS     에너지    WI26 에너지
            ...                  ...        ...            ...
            053050          지에스이   유틸리티  WI26 유틸리티
            016710        대성홀딩스   유틸리티  WI26 유틸리티
            003480  한진중공업홀딩스   유틸리티  WI26 유틸리티
            017390          서울가스   유틸리티  WI26 유틸리티
            034590      인천도시가스   유틸리티  WI26 유틸리티
    """

    MAX_TRY: int = 5
    __date__: str = ""
    __data__: DataFrame = DataFrame()
    __root__: str = "http://www.wiseindex.com/Index/Index#/G1010.0.Components"
    __base__: List[Dict] = [
        dict(
            code='WI100',
            name='에너지',
            benchmarkTicker='117460',
            benchmarkName='KRX 에너지화학',
        ),
        dict(
            code='WI110',
            name='화학',
            benchmarkTicker='117460',
            benchmarkName='KRX 에너지화학',
        ),
        dict(
            code='WI200',
            name='비철금속',
            benchmarkTicker='069500',
            benchmarkName='코스피 200',
        ),
        dict(
            code='WI210',
            name='철강',
            benchmarkTicker='117680',
            benchmarkName='KRX 철강',
        ),
        dict(
            code='WI220',
            name='건설',
            benchmarkTicker='117700',
            benchmarkName='KRX 건설',
        ),
        dict(
            code='WI230',
            name='기계',
            benchmarkTicker='102960',
            benchmarkName='KRX 기계',
        ),
        dict(
            code='WI240',
            name='조선',
            benchmarkTicker='139230',
            benchmarkName='KRX 중장비조선',
        ),
        dict(
            code='WI250',
            name='상사,자본재',
            benchmarkTicker='069500',
            benchmarkName='코스피 200',
        ),
        dict(
            code='WI260',
            name='운송',
            benchmarkTicker='140710',
            benchmarkName='KRX 운송',
        ),
        dict(
            code='WI300',
            name='자동차',
            benchmarkTicker='091180',
            benchmarkName='KRX 자동차',
        ),
        dict(
            code='WI310',
            name='화장품,의류',
            benchmarkTicker='228790',
            benchmarkName='WISE 화장품',
        ),
        dict(
            code='WI320',
            name='호텔,레저',
            benchmarkTicker='228800',
            benchmarkName='WISE 여행레저',
        ),
        dict(
            code='WI330',
            name='미디어,교육',
            benchmarkTicker='266360',
            benchmarkName='KRX IT',
        ),
        dict(
            code='WI340',
            name='소매(유통)',
            benchmarkTicker='069500',
            benchmarkName='코스피 200',
        ),
        dict(
            code='WI400',
            name='필수소비재',
            benchmarkTicker='266410',
            benchmarkName='KRX 필수소비재',
        ),
        dict(
            code='WI410',
            name='건강관리',
            benchmarkTicker='227540',
            benchmarkName='KRX 헬스케어',
        ),
        dict(
            code='WI500',
            name='은행',
            benchmarkTicker='091170',
            benchmarkName='KRX 은행',
        ),
        dict(
            code='WI510',
            name='증권',
            benchmarkTicker='157500',
            benchmarkName='FnGuide 증권',
        ),
        dict(
            code='WI520',
            name='보험',
            benchmarkTicker='140700',
            benchmarkName='KRX 보험',
        ),
        dict(
            code='WI600',
            name='소프트웨어',
            benchmarkTicker='157490',
            benchmarkName='FnGuide SW',
        ),
        dict(
            code='WI610',
            name='IT하드웨어',
            benchmarkTicker='266370',
            benchmarkName='KRX IT HW',
        ),
        dict(
            code='WI620',
            name='반도체',
            benchmarkTicker='091160',
            benchmarkName='KRX 반도체',
        ),
        dict(
            code='WI630',
            name='IT가전',
            benchmarkTicker='266370',
            benchmarkName='KRX IT HW',
        ),
        dict(
            code='WI640',
            name='디스플레이',
            benchmarkTicker='266370',
            benchmarkName='KRX IT HW',
        ),
        dict(
            code='WI700',
            name='통신서비스',
            benchmarkTicker='098560',
            benchmarkName='KRX 통신서비스',
        ),
        dict(
            code='WI800',
            name='유틸리티',
            benchmarkTicker='069500',
            benchmarkName='코스피 200',
        ),
    ]

    def __init__(self):
        self.__data__ = DataFrame()
        self.__date__ = ""
        return

    def __call__(self) -> DataFrame:
        return self.data

    def __str__(self) -> str:
        return str(self.data)

    def __getattr__(self, item:Any):
        if hasattr(self.data, item):
            return getattr(self.data, item)
        if not item in dir(self):
            raise AttributeError

    def __getitem__(self, item:Any):
        return self.data[item]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def _url_(self, code:str):
        return f'http://www.wiseindex.com/Index/GetIndexComponets?' \
               f'ceil_yn=0&' \
               f'dt={self.date}&' \
               f'sec_cd={code}'

    def _sector_(self, code:dict) -> DataFrame:
        columns = {"CMP_CD": 'ticker', "CMP_KOR": 'korName', "SEC_NM_KOR": 'sector', "IDX_NM_KOR": 'industry'}
        for try_count in range(self.MAX_TRY):
            try:
                data = web.req(self._url_(code["code"])).json()["list"]
                data = DataFrame(data).rename(columns=columns)[columns.values()].set_index(keys='ticker')
                data["name"] = data["korName"]
                data[["benchmark", "benchmarkTicker"]] = [code["benchmarkName"], code["benchmarkTicker"]]
                return data
            except ConnectionError:
                time.sleep(3)
        return DataFrame(columns=list(columns.values()))

    @property
    def date(self) -> str:
        if not self.__date__:
            for p in web.html(self.__root__).find_all("p"):
                if "기준일" in p.text:
                    self.__date__ = p.text.replace("기준일 : 20", "").replace(".", "")
                    return self.__date__
        return self.__date__

    @property
    def data(self) -> DataFrame:
        if self.__data__.empty:
            self.__data__ = concat(objs=[self._sector_(cd) for cd in self.__base__], axis=0)
        return self.__data__

# Alias
wise = _wise()

if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)

    print(wise.date)
    print(wise.data)