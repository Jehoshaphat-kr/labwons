from nohji.meta import meta
from nohji.util.chart import r1c1nsy
from nohji.util.tools import int2won

from datetime import datetime
from pandas import DataFrame
from plotly.graph_objects import Scatter
from pykrx.stock import get_market_cap_by_ticker


def KoreanMarket():
    src = meta.data.copy()
    src = src[(src["country"] == "KOR") & (src["quoteType"] == "EQUITY")]
    src = src.join(get_market_cap_by_ticker(date=datetime.today().strftime("%Y%m%d"), alternative=True), how="left")

    objs = []
    for ind in src["industry"].drop_duplicates():
        data = src[src["industry"] == ind]
        exchange = data["exchange"].value_counts()
        cap = (data["시가총액"] / 100000000).sum()
        objs.append({
            "sector": ind.replace("WI26 ", ""),
            "kospi": exchange["KOSPI"] if "KOSPI" in exchange else 0,
            "kosdaq": exchange["KOSDAQ"] if "KOSDAQ" in exchange else 0,
            "marketCap": cap,
            "marketCapT": int2won(cap)
        })
    data = DataFrame(objs)
    data = data.sort_values(by="marketCap", ascending=False)

    trace = []
    for _, row in data.iterrows():
        trace.append(
            Scatter(
                name=row["sector"],
                x=[row["kospi"]],
                y=[row["kosdaq"]],
                meta=[row["marketCapT"]],
                mode="markers",
                marker={
                    "size": row["marketCap"] / 20000
                },
                hovertemplate=row["sector"] + "<br>시가총액: %{meta}원<br>KOSPI: %{x}개<br>KOSDAQ: %{y}개<extra></extra>"
            )
        )
    fig = r1c1nsy()
    fig.add_traces(trace)
    fig.update_layout(
        hovermode="closest",
        legend={
            "orientation": "v",
            "xanchor": "auto",
            "yanchor": "auto",
            "x": 1.00, "y": 1.0
        },
        xaxis={"title": "KOSPI 상장 기업 수"},
        yaxis={"title": "KOSDAQ 상장 기업 수"}
    )
    fig.show()
    return

if __name__ == "__main__":
    KoreanMarket()


