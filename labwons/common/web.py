from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests, json, pandas


class _web(object):

    def req(self, url:str):
        attr = f"_req_{url}_"
        if not hasattr(self, attr):
            req = requests.get(url)
            if not req.status_code == 200:
                raise ConnectionError
            self.__setattr__(attr, req)
        return self.__getattribute__(attr)

    def html(self, url:str, parser:str="") -> BeautifulSoup:
        attr = f"_html_{url}_"
        if not hasattr(self, attr):
            parser = parser if parser else 'xml' if url.endswith('.xml') else 'lxml'
            self.__setattr__(attr, BeautifulSoup(self.req(url).text, parser))
        return self.__getattribute__(attr)

    def list(self, url:str, encoding:str='utf-8') -> list:
        attr = f"_list_{url}_"
        if not hasattr(self, attr):
            encoding = "euc-kr" if "naver" in url else encoding
            self.__setattr__(attr, pandas.read_html(io=url, header=0, encoding=encoding))
        return self.__getattribute__(attr)

    def json(self, url:str) -> json:
        attr = f"_json_{url}_"
        if not hasattr(self, attr):
            data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
            self.__setattr__(attr, data)
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


# Alias
web = _web()