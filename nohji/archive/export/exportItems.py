from nohji.util.chart import image, r1c1nsy
from nohji.util.tools import int2won

from pandas import DataFrame
from plotly.graph_objects import Bar, Figure, Pie, Scatter
from numpy import nan


# <DataFrame; src>
#    - <Unit; 억불>
src = DataFrame({
    '연도': {0: 1996, 1: 1997, 2: 1998, 3: 1999, 4: 2000, 5: 2001, 6: 2002, 7: 2003, 8: 2004, 9: 2005, 10: 2006, 11: 2007, 12: 2008, 13: 2009, 14: 2010, 15: 2011, 16: 2012, 17: 2013, 18: 2014, 19: 2015, 20: 2016, 21: 2017, 22: 2018, 23: 2019, 24: 2020, 25: 2021, 26: 2022},
    '반도체': {0: 15237, 1: 17162, 2: 17008, 3: 18850, 4: 26006, 5: 14259, 6: 16631, 7: 19535, 8: 26516, 9: 29986, 10: 33236, 11: 30278, 12: 25780, 13: 24384, 14: 51464, 15: 50146, 16: 50430, 17: 57143, 18: 62426, 19: 62717, 20: 62005, 21: 97937, 22: 126706, 23: 93930, 24: 99177, 25: 127980, 26: 129229},
    '자동차': {0: 10468, 1: 10682, 2: 9947, 3: 11171, 4: 13221, 5: 13322, 6: 14779, 7: 19119, 8: 26577, 9: 29506, 10: 32924, 11: 34483, 12: 31288, 13: 22399, 14: 31782, 15: 45312, 16: 47201, 17: 48635, 18: 48924, 19: 45794, 20: 40637, 21: 41690, 22: 40887, 23: 43036, 24: 37399, 25: 46465, 26: 54067},
    '석유제품': {0: 3738, 1: 5163, 2: 4372, 3: 5468, 4: 9055, 5: 7794, 6: 6382, 7: 6623, 8: 10203, 9: 15366, 10: 20407, 11: 23342, 12: 36627, 13: 22145, 14: 31862, 15: 51600, 16: 56098, 17: 52787, 18: 50784, 19: 32002, 20: 26472, 21: 35037, 22: 46350, 23: 40691, 24: 24168, 25: 38121, 26: 62875},
    '선박및부품': {0: 7208, 1: 6652, 2: 8140, 3: 7655, 4: 8420, 5: 9909, 6: 10867, 7: 11334, 8: 15657, 9: 17727, 10: 22116, 11: 23586, 12: 34472, 13: 37223, 14: 47112, 15: 56588, 16: 39753, 17: 37168, 18: 39886, 19: 40107, 20: 34268, 21: 42182, 22: 21275, 23: 20159, 24: 19749, 25: 22988, 26: 18178},
    '무선통신기기': {0: nan, 1: nan, 2: nan, 3: 5215.0, 4: 7882.0, 5: 9854.0, 6: 13619.0, 7: 18697.0, 8: 26223.0, 9: 27495.0, 10: 27033.0, 11: 28850.0, 12: 34434.0, 13: 29531.0, 14: 37567.0, 15: 27325.0, 16: 22751.0, 17: 27578.0, 18: 29573.0, 19: 32587.0, 20: 29664.0, 21: 22099.0, 22: 17089.0, 23: 14082.0, 24: 13184.0, 25: 16194.0, 26: 17231.0},
    '자동차부품': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: 4227.0, 8: 5925.0, 9: 8453.0, 10: 10255.0, 11: 11658.0, 12: 13096.0, 13: 10926.0, 14: 18963.0, 15: 23088.0, 16: 24610.0, 17: 26079.0, 18: 26635.0, 19: 25550.0, 20: 24415.0, 21: 23134.0, 22: 23119.0, 23: 22535.0, 24: 18640.0, 25: 22776.0, 26: 23316.0},
    '철강판': {0: 3649.0, 1: 3971.0, 2: 4956.0, 3: 4138.0, 4: 4828.0, 5: 4076.0, 6: 4024.0, 7: 5841.0, 8: 8527.0, 9: 10215.0, 10: 11005.0, 11: nan, 12: nan, 13: nan, 14: nan, 15: 20972.0, 16: 19729.0, 17: 17494.0, 18: 19144.0, 19: 16458.0, 20: 15379.0, 21: 18111.0, 22: 19669.0, 23: 18606.0, 24: 15997.0, 25: 22494.0, 26: 22401.0},
    '합성수지': {0: nan, 1: 4042.0, 2: 4029.0, 3: 4086.0, 4: 5041.0, 5: 4524.0, 6: 4955.0, 7: 6260.0, 8: 8426.0, 9: 10304.0, 10: 11185.0, 11: nan, 12: nan, 13: nan, 14: 14448.0, 15: 19555.0, 16: 19558.0, 17: 21369.0, 18: 21691.0, 19: 18418.0, 20: 17484.0, 21: 20436.0, 22: 22960.0, 23: 20251.0, 24: 19202.0, 25: 29144.0, 26: 28078.0},
    '디스플레이': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: 12264.0, 11: 19641.0, 12: nan, 13: nan, 14: nan, 15: 28733.0, 16: 31291.0, 17: 28613.0, 18: 26498.0, 19: 21915.0, 20: 16582.0, 21: 27543.0, 22: 24856.0, 23: 20657.0, 24: 18151.0, 25: 21573.0, 26: 21299.0},
    '영상기기': {0: 5550.0, 1: 4066.0, 2: nan, 3: nan, 4: 3667.0, 5: 3519.0, 6: 4052.0, 7: 5618.0, 8: 7630.0, 9: 7430.0, 10: nan, 11: 8254.0, 12: nan, 13: nan, 14: nan, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: nan},
    '컴퓨터': {0: 5462.0, 1: 6220.0, 2: 5265.0, 3: 10440.0, 4: 14687.0, 5: 11245.0, 6: 12941.0, 7: 14977.0, 8: 17123.0, 9: 14117.0, 10: 12587.0, 11: 8623.0, 12: nan, 13: nan, 14: nan, 15: 9156.0, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: 9177.0, 22: 10760.0, 23: nan, 24: 13426.0, 25: 16816.0, 26: nan},
    '금은및백금': {0: 5415.0, 1: 6370.0, 2: 7294.0, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: nan, 13: nan, 14: nan, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: nan},
    '인조장섬유직물': {0: 5254.0, 1: 4958.0, 2: 3905.0, 3: 3589.0, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: nan, 13: nan, 14: nan, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: nan},
    '의류': {0: 3970.0, 1: nan, 2: 4376.0, 3: 4548.0, 4: 4652.0, 5: 3924.0, 6: 3644.0, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: nan, 13: nan, 14: nan, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: nan},
    '영상기기부분품': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: 6714.0, 12: 6253.0, 13: 5704.0, 14: nan, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: nan},
    '특수선박': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: 6436.0, 13: 5208.0, 14: nan, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: nan},
    '액정디바이스': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: 23068.0, 13: 23390.0, 14: 29577.0, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: nan},
    '사무용부분품': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: 6161.0, 13: 5075.0, 14: nan, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: nan},
    '플라스틱제품': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: nan, 13: nan, 14: 16462.0, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: 9606.0, 21: nan, 22: nan, 23: 10292.0, 24: nan, 25: nan, 26: nan},
    '가전제품': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: nan, 13: nan, 14: 13618.0, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: nan},
    '전자응용기기': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: nan, 13: nan, 14: nan, 15: nan, 16: 8583.0, 17: 10896.0, 18: 9800.0, 19: 10038.0, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: nan},
    '정밀화학원료': {0: nan, 1: nan, 2: nan, 3: nan, 4: nan, 5: nan, 6: nan, 7: nan, 8: nan, 9: nan, 10: nan, 11: nan, 12: nan, 13: nan, 14: nan, 15: nan, 16: nan, 17: nan, 18: nan, 19: nan, 20: nan, 21: nan, 22: nan, 23: nan, 24: nan, 25: nan, 26: 18799.0},
    # '총액': {0: 65951, 1: 69286, 2: 69292, 3: 75160, 4: 97459, 5: 82426, 6: 91894, 7: 112231, 8: 152807, 9: 170599, 10: 193012, 11: 195429, 12: 217615, 13: 185985, 14: 292855, 15: 332475, 16: 320004, 17: 327762, 18: 335363, 19: 305586, 20: 276513, 21: 337345, 22: 353671, 23: 304238, 24: 279093, 25: 364579, 26: 395473},
    # '비중': {0: 50.8, 1: 50.9, 2: 52.4, 3: 52.3, 4: 56.6, 5: 54.8, 6: 56.6, 7: 57.9, 8: 57.9, 9: 60.0, 10: 59.3, 11: 52.6, 12: 51.6, 13: 51.2, 14: 62.8, 15: 59.9, 16: 58.4, 17: 58.6, 18: 58.6, 19: 58.0, 20: 55.8, 21: 59.0, 22: 58.5, 23: 56.1, 24: 54.5, 25: 56.6, 26: 57.9}
})
src = src.set_index(keys="연도")
src = src / 100
key = [
    "반도체",
    "자동차",
    "석유제품",
    "선박및부품",
    "무선통신기기",
    "자동차부품",
    "철강판",
    "합성수지",
    "디스플레이"
]


def timeSeries(data:DataFrame):
    data = data.copy()
    data.loc[(data.index > 2007) & (data.index <= 2010), :] = nan

    traces = []
    for col in data:
        if not col in key:
            continue
        traces.append(Scatter(
            name=col,
            x=data.index,
            y=data[col],
            hovertemplate=col + ": %{y:.2f}억불<extra></extra>"
        ))

    fig = r1c1nsy()
    fig.add_traces(traces)
    fig.add_vrect(
        x0=2007,
        x1=2011,
        fillcolor="lightgrey",
        opacity=0.5,
        line_width=0,
    )
    fig.add_annotation(
        text="제외된 데이터<br>(분류 기준 상이)",
        x=2009,
        y=600,
        showarrow=False
    )
    fig.update_layout(
        xaxis={"title": "연도"},
        yaxis={"title": "수출액 [억불]"}
    )
    fig.show()
    return

def stackedBar(data:DataFrame):
    data = data.copy()
    data["기타"] = data[[col for col in data if not col in key]].fillna(0).sum(axis=1)
    data = data[key + ["기타"]]

    sums = data.sum(axis=1)
    data = data.div(sums, axis=0) * 100
    data.loc[(data.index > 2007) & (data.index <= 2010), :] = nan

    trace = []
    for col in data:
        dat = data[col]
        trace.append(Bar(
            name=col,
            x=dat.index,
            y=dat,
            hovertemplate=col + ": %{y:.2f}%<extra></extra>"
        ))
    fig = r1c1nsy()
    fig.add_traces(trace)
    fig.add_shape(
        type="rect",
        x0=2007.5, y0=0,
        x1=2010.5, y1=100,
        fillcolor="lightgrey",
        opacity=0.5,
        line_width=0,
    )
    fig.add_annotation(
        text="제외된 데이터<br>(분류 기준 상이)",
        x=2009,
        y=50,
        showarrow=False
    )
    fig.update_layout(
        barmode="stack",
        xaxis={"title": "연도", "tickmode":"linear"},
        yaxis={"title": "비중[%]"}
    )
    fig.show()
    return

def pie(data:DataFrame):
    data = data.copy()
    data["기타"] = data[[col for col in data if not col in key]].fillna(0).sum(axis=1)
    data = data[key + ["기타"]]

    sums = data.sum(axis=1)
    data = (data.div(sums, axis=0) * 100).iloc[-1]
    fig = Figure()
    fig.add_trace(Pie(
        labels=data.index,
        values=data,
        showlegend=False,
        visible=True,
        automargin=True,
        opacity=0.85,
        textfont=dict(color='black'),
        textinfo='label+percent',
        insidetextorientation='radial',
        hoverinfo='label+percent',
    ))
    fig.add_layout_image(image())
    fig.show()
    return

if __name__ == "__main__":
    from pandas import set_option
    set_option('display.expand_frame_repr', False)
    # print(src)

    timeSeries(src)
    stackedBar(src)
    pie(src)