from nohji.indicator import Indicator, ecos
from nohji.util.chart import r1c1sy1

from plotly.offline import plot


ecos.api = "CEW3KQU603E6GA8VX0O9"
def BalanceAndKospi():

    balance = Indicator("301Y013", "경상수지", sum_by="Y")
    kospi = Indicator("802Y001", "KOSPI지수", by="Y")

    fig = r1c1sy1(x_title="날짜")
    x1 = max(balance.index[0], kospi.index[0])
    x2 = min(balance.index[-1], kospi.index[-1])

    fig.add_trace(trace=kospi.bar(marker={"color": "rgb(255,0,0)", "opacity":0.6}), secondary_y=True)
    # fig.add_trace(trace=kospi.line(line={"color": "#ff0000"}), secondary_y=True)
    fig.add_trace(trace=balance.line(line={"color": "#4169e1"}), secondary_y=False)

    fig.update_layout(
        height=750,
        xaxis={
            "autorange": False,
            "range": [x1, x2]
        },
        yaxis={
            "title": "경상수지[백만달러]",
            "zerolinewidth":1.5
        },
        yaxis2={"title": "KOSPI[-]"}
    )
    fig.show()

    with open(r"C:\Users\wpgur\Downloads\plotly\div-oid.html", mode="w", encoding="utf-8") as file:
        tag = fig.to_html(
            include_plotlyjs=False,
            full_html=False,
            div_id="snob-plotly"
        )
        file.write(tag)


    return



if __name__ == "__main__":

    BalanceAndKospi()

