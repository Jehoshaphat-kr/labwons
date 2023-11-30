from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests, json, pandas


class _web(object):

    def html(self, url:str) -> BeautifulSoup:
        attr = f"_html_{url}_"
        if not hasattr(self, attr):
            feature = 'xml' if url.endswith('.xml') else 'lxml'
            self.__setattr__(attr, BeautifulSoup(requests.get(url).text, feature))
        return self.__getattribute__(attr)

    def list(self, url:str) -> list:
        attr = f"_list_{url}_"
        if not hasattr(self, attr):
            encoding = "euc-kr" if "naver" in url else "utf-8"
            self.__setattr__(attr, pandas.read_html(io=url, header=0, encoding=encoding))
        return self.__getattribute__(attr)

    def json(self, url:str) -> json:
        attr = f"_json_{url}_"
        if not hasattr(self, attr):
            self.__setattr__(attr, json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace')))
        return self.__getattribute__(attr)

    def data(self, url:str, key:str=""):
        if url.endswith('.json'):
            return pandas.DataFrame(self.json(url)[key] if key else self.json(url))
        elif url.endswith('.csv'):
            return pandas.read_csv(url, encoding='utf-8')
        elif url.endswith('.pkl'):
            return pandas.read_pickle(url)
        else:
            raise KeyError(f"Unknown data type: {url}")

    def json2data(self, url:str, key:str="CHART") -> pandas.DataFrame:
        return pandas.DataFrame(self.json(url)[key])


# Alias
web = _web()