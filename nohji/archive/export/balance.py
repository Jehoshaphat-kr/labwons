from nohji.indicator import Indicator, ecos
from nohji.util.chart import r1c1sy1


ecos.api = "CEW3KQU603E6GA8VX0O9"
def BalanceAndIndicator():

    balance = Indicator("301Y013", "경상수지", sum_by="Y")
    gdp = Indicator("200Y004", "국내총생산(시장가격, GDP)", by="Y")
    kospi = Indicator("802Y001", "KOSPI지수", by="Y")

    fig = r1c1sy1(x_title="날짜")
    # fig.add_trace(trace=balance.bar(opacity=0.8), secondary_y=False)
    # fig.add_trace(trace=gdp.line("yoy", unit="%"), secondary_y=True)
    # fig.add_trace(trace=kospi.line(), secondary_y=True)

    fig.add_trace(trace=balance.line(), secondary_y=False)
    fig.add_trace(trace=kospi.bar(opacity=0.8), secondary_y=True)

    fig.update_layout(
        yaxis={
            "title": "경상수지[백만달러]",
            "zerolinewidth":1.5
        },
        # yaxis2={"title": "실질 GDP 성장률[%]"}
        yaxis2={"title": "KOSPI[-]"}
    )
    # fig.show()

    with open(r"C:\Users\Administrator\Downloads\plotly\div-oid.html", mode="w", encoding="utf-8") as file:
        tag = fig.to_html(full_html=False, div_id="snob-plotly")
        file.write(tag)


    return



if __name__ == "__main__":

    BalanceAndIndicator()

