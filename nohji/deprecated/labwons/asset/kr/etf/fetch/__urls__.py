from labwons.common.web import web
from typing import Union, Hashable


class urls(object):
    def __init__(self, ticker:Union[str, Hashable]):
        self.ticker = ticker
        return

    def __call__(self, code:str, GB:str, menuID:str, stkGb:str) -> str:
        return self._url_(code, GB, menuID, stkGb)

    def _url_(self, code:str, GB:str, menuID:str, stkGb:str):
        return f"http://comp.fnguide.com/SVO2/ASP/etf_{code}.asp?" \
               f"pGB=1&" \
               f"gicode=A{self.ticker}&" \
               f"cID=&" \
               f"MenuYn=Y" \
               f"&ReportGB={GB}" \
               f"&NewMenuID={menuID}" \
               f"&stkGb={stkGb}"

    @property
    def xml(self) -> str:
        """
        공통 xml
        :return:
        """
        return f"http://cdn.fnguide.com/SVO2/xml/Snapshot_all/{self.ticker}.xml"

    @property
    def etf(self) -> str:
        """
        "ETF/ETN 개요" 탭
        :return:
        """
        return self._url_("snapshot", "", "401", "770")

    @property
    def naver(self) -> str:
        """
        "네이버" 증권
        :return:
        """
        return  f"https://finance.naver.com/item/main.naver?code={self.ticker}"



if __name__ == "__main__":
    url = urls(
        "102780"
    )
    print(url.xml)
