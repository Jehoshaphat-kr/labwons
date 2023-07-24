from datetime import datetime, timedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup as Soup
from pykrx import stock
import requests, json
import pandas as pd
import numpy as np


def get_benchmark_multiple(ticker:str) -> pd.DataFrame:
    url = f"http://cdn.fnguide.com/SVO2/json/chart/01_04/chart_A{ticker}_D.json"
    data = json.loads(urlopen(url=url).read().decode('utf-8-sig', 'replace'))
    objs = dict()
    for label, index in (('PER', '02'), ('EV/EBITDA', '03'), ('ROE', '04')):
        header1 = pd.DataFrame(data[f'{index}_H'])[['ID', 'NAME']].set_index(keys='ID')
        header1['NAME'] = header1['NAME'].astype(str).str.replace("'", "20")
        header1 = header1.to_dict()['NAME']
        header1.update({'CD_NM': '이름'})

        inner1 = pd.DataFrame(data[index])[list(header1.keys())].rename(columns=header1).set_index(keys='이름')
        inner1.index.name = None
        for col in inner1.columns:
            inner1[col] = inner1[col].apply(lambda x: np.nan if x == '-' else x)
        objs[label] = inner1.T
    return pd.concat(objs=objs, axis=1).astype(float)
