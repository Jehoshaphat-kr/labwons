from nohji.util.chart import r1c2nsy
from pandas import DataFrame
from plotly.graph_objects import Pie


# 202312
# Unit:
src = DataFrame({
    '국가명': {0: "미국", 1: "중국", 2: "베트남", 3: "홍콩", 4: "일본", 5: "대만", 6: "싱가포르", 7: "마샬제도", 8: "인도", 9: "호주", 10: "기타국(222개)"},
    '수출액': {0: 11267382749, 1: 10847203820, 2: 4629936831, 3: 3332828166, 4: 2488509831, 5: 2169142315, 6: 1958267674, 7: 1845438805, 8: 1586813263, 9: 1435817445, 10: 15850330314},
    '수입액': {0: 6273397907, 1: 10881731037, 2: 2104001757, 3: 130568819, 4: 3919919418, 5: 1935912149, 6: 797609070, 7: 22905, 8: 540425640, 9: 3076284188, 10: 23481866352},
    '수출비중': {0: 19.62559617, 1: 18.89372595, 2: 8.064452285, 3: 5.80514048, 4: 4.334501641, 5: 3.778225349, 6: 3.41092261, 7: 3.214396596, 8: 2.763921045, 9: 2.500915606, 10: 27.60820227},
    '수입비중': {0: 11.80502934, 1: 20.47680635, 2: 3.959226377, 3: 0.245699183, 4: 7.37634762, 5: 3.642922073, 6: 1.500908855, 7: 4.31017E-05, 8: 1.01695136, 9: 5.788828578, 10: 44.18723716},
})
print(src)

def pie(data:DataFrame):
    fig = r1c2nsy(specs=[[{"type": 'pie'}, {"type": "pie"}]], subplot_titles=["수출", "수입"])
    fig.add_trace(
        row=1, col=1,
        trace=Pie(
            labels=data["국가명"],
            values=data["수출비중"],
            meta=data["수출액"] / 100000000,
            showlegend=False,
            visible=True,
            automargin=True,
            opacity=0.85,
            textfont=dict(color='black'),
            textinfo='label+percent',
            insidetextorientation='radial',
            hoverinfo='label+percent',
        )
    )
    fig.add_trace(
        row=1, col=2,
        trace=Pie(
            labels=data["국가명"],
            values=data["수입비중"],
            meta=data["수입액"] / 100000000,
            showlegend=False,
            visible=True,
            automargin=True,
            opacity=0.85,
            textfont=dict(color='black'),
            textposition="inside",
            textinfo='label+percent',
            insidetextorientation='radial',
            hoverinfo='label+percent',
        )
    )
    fig.update_layout(
        font=dict(size=16),
        uniformtext_minsize=16, uniformtext_mode='hide'
    )
    fig.show()
    return


if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)
    # print(src)

    pie(src)