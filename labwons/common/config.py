import os


# CSS COLOR CODE
COLORS = [
    'aliceblue',
    'antiquewhite',
    'aqua',
    'aquamarine',
    'azure',
    'beige',
    'bisque',
    'black',
    'blanchedalmond',
    'blue',
    'blueviolet',
    'brown',
    'burlywood',
    'cadetblue',
    'chartreuse',
    'chocolate',
    'coral',
    'cornflowerblue',
    'cornsilk',
    'crimson',
    'cyan',
    'darkblue',
    'darkcyan',
    'darkgoldenrod',
    'darkgray',
    'darkgrey',
    'darkgreen',
    'darkkhaki',
    'darkmagenta',
    'darkolivegreen',
    'darkorange',
    'darkorchid',
    'darkred',
    'darksalmon',
    'darkseagreen',
    'darkslateblue',
    'darkslategray',
    'darkslategrey',
    'darkturquoise',
    'darkviolet',
    'deeppink',
    'deepskyblue',
    'dimgray',
    'dimgrey',
    'dodgerblue',
    'firebrick',
    'floralwhite',
    'forestgreen',
    'fuchsia',
    'gainsboro',
    'ghostwhite',
    'gold',
    'goldenrod',
    'gray',
    'grey',
    'green',
    'greenyellow',
    'honeydew',
    'hotpink',
    'indianred',
    'indigo',
    'ivory',
    'khaki',
    'lavender',
    'lavenderblush',
    'lawngreen',
    'lemonchiffon',
    'lightblue',
    'lightcoral',
    'lightcyan',
    'lightgoldenrodyellow',
    'lightgray',
    'lightgrey',
    'lightgreen',
    'lightpink',
    'lightsalmon',
    'lightseagreen',
    'lightskyblue',
    'lightslategray',
    'lightslategrey',
    'lightsteelblue',
    'lightyellow',
    'lime',
    'limegreen',
    'linen',
    'magenta',
    'maroon',
    'mediumaquamarine',
    'mediumblue',
    'mediumorchid',
    'mediumpurple',
    'mediumseagreen',
    'mediumslateblue',
    'mediumspringgreen',
    'mediumturquoise',
    'mediumvioletred',
    'midnightblue',
    'mintcream',
    'mistyrose',
    'moccasin',
    'navajowhite',
    'navy',
    'oldlace',
    'olive',
    'olivedrab',
    'orange',
    'orangered',
    'orchid',
    'palegoldenrod',
    'palegreen',
    'paleturquoise',
    'palevioletred',
    'papayawhip',
    'peachpuff',
    'peru',
    'pink',
    'plum',
    'powderblue',
    'purple',
    'red',
    'rosybrown',
    'royalblue',
    'saddlebrown',
    'salmon',
    'sandybrown',
    'seagreen',
    'seashell',
    'sienna',
    'silver',
    'skyblue',
    'slateblue',
    'slategray',
    'slategrey',
    'snow',
    'springgreen',
    'steelblue',
    'tan',
    'teal',
    'thistle',
    'tomato',
    'turquoise',
    'violet',
    'wheat',
    'white',
    'whitesmoke',
    'yellow',
    'yellowgreen'
]

# PLOTLY RANGE SELECTOR BUTTONS
PERIODS = dict(
    buttons=list([
        dict(count=1, label="1m", step="month", stepmode="backward"),
        dict(count=3, label="3m", step="month", stepmode="backward"),
        dict(count=6, label="6m", step="month", stepmode="backward"),
        dict(count=1, label="YTD", step="year", stepmode="todate"),
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all")
    ])
)

# METADATA WI26 CODE
WI26 = [
    dict(
        id='WI100',
        name='에너지',
        benchmarkTicker='117460',
        benchmarkName='KRX Energy & Chemicals',
    ),
    dict(
        id='WI110',
        name='화학',
        benchmarkTicker='117460',
        benchmarkName='KRX Energy & Chemicals',
    ),
    dict(
        id='WI200',
        name='비철금속',
        benchmarkTicker='069500',
        benchmarkName='KOSPI200',
    ),
    dict(
        id='WI210',
        name='철강',
        benchmarkTicker='117680',
        benchmarkName='KRX Steels',
    ),
    dict(
        id='WI220',
        name='건설',
        benchmarkTicker='117700',
        benchmarkName='KRX Constructions',
    ),
    dict(
        id='WI230',
        name='기계',
        benchmarkTicker='102960',
        benchmarkName='KRX Mechanical Equipment',
    ),
    dict(
        id='WI240',
        name='조선',
        benchmarkTicker='139230',
        benchmarkName='KRX Heavy Industry',
    ),
    dict(
        id='WI250',
        name='상사,자본재',
        benchmarkTicker='069500',
        benchmarkName='KOSPI200',
    ),
    dict(
        id='WI260',
        name='운송',
        benchmarkTicker='140710',
        benchmarkName='KRX Transportation',
    ),
    dict(
        id='WI300',
        name='자동차',
        benchmarkTicker='091180',
        benchmarkName='KRX Autos',
    ),
    dict(
        id='WI310',
        name='화장품,의류',
        benchmarkTicker='228790',
        benchmarkName='WISE Cosmetics',
    ),
    dict(
        id='WI320',
        name='호텔,레저',
        benchmarkTicker='228800',
        benchmarkName='WISE Travel and Leisure',
    ),
    dict(
        id='WI330',
        name='미디어,교육',
        benchmarkTicker='266360',
        benchmarkName='KRX IT SW',
    ),
    dict(
        id='WI340',
        name='소매(유통)',
        benchmarkTicker='069500',
        benchmarkName='KOSPI200',
    ),
    dict(
        id='WI400',
        name='필수소비재',
        benchmarkTicker='266410',
        benchmarkName='KRX Consumer Staples',
    ),
    dict(
        id='WI410',
        name='건강관리',
        benchmarkTicker='227540',
        benchmarkName='KRX Healthcare',
    ),
    dict(
        id='WI500',
        name='은행',
        benchmarkTicker='091170',
        benchmarkName='KRX Bank',
    ),
    dict(
        id='WI510',
        name='증권',
        benchmarkTicker='157500',
        benchmarkName='FnGuide Securities Company',
    ),
    dict(
        id='WI520',
        name='보험',
        benchmarkTicker='140700',
        benchmarkName='KRX Insurance',
    ),
    dict(
        id='WI600',
        name='소프트웨어',
        benchmarkTicker='157490',
        benchmarkName='FnGuide SW',
    ),
    dict(
        id='WI610',
        name='IT하드웨어',
        benchmarkTicker='266370',
        benchmarkName='KRX IT HW',
    ),
    dict(
        id='WI620',
        name='반도체',
        benchmarkTicker='091160',
        benchmarkName='KRX Semicon',
    ),
    dict(
        id='WI630',
        name='IT가전',
        benchmarkTicker='266370',
        benchmarkName='KRX IT HW',
    ),
    dict(
        id='WI640',
        name='디스플레이',
        benchmarkTicker='266370',
        benchmarkName='KRX IT HW',
    ),
    dict(
        id='WI700',
        name='통신서비스',
        benchmarkTicker='098560',
        benchmarkName='KRX Media & Telecom',
    ),
    dict(
        id='WI800',
        name='유틸리티',
        benchmarkTicker='069500',
        benchmarkName='KOSPI200',
    ),
]

# METADATA OECD CODE
OECD = [
    dict(
        ticker='BSCICP03',
        name='BCI',
        exchange='OECD',
        quoteType='INDEX',
        unit='-',
        comment='OECD Standard BCI, Amplitude adjusted (Long term average=100)'
    ),
    dict(
        ticker='CSCICP03',
        name='CCI',
        exchange='OECD',
        quoteType='INDEX',
        unit='-',
        comment='OECD Standard CCI, Amplitude adjusted (Long term average=100)'
    ),
    dict(
        ticker='LOLITOAA',
        name='CLI(AA)',
        exchange='OECD',
        quoteType='INDEX',
        unit='-',
        comment='Amplitude adjusted (CLI)'
    ),
    dict(
        ticker='LOLITONO',
        name='CLI(Norm)',
        exchange='OECD',
        quoteType='INDEX',
        unit='-',
        comment='Normalised (CLI)'
    ),
    dict(
        ticker='LOLITOTR_STSA',
        name='CLI(TR)',
        exchange='OECD',
        quoteType='INDEX',
        unit='-',
        comment='Trend restored (CLI)'
    ),
    dict(
        ticker='LOLITOTR_GYSA',
        name='CLI(%TR)',
        exchange='OECD',
        quoteType='INDEX',
        unit='%',
        comment='12-month rate of change of the trend restored CLI'
    ),
    dict(
        ticker='LORSGPNO',
        name='GDP(Norm)',
        exchange='OECD',
        quoteType='INDEX',
        unit='-',
        comment='Ratio to trend (GDP)'
    ),
    dict(
        ticker='LORSGPTD',
        name='GDP(T)',
        exchange='OECD',
        quoteType='INDEX',
        unit='-',
        comment='Normalised (GDP)'
    ),
    dict(
        ticker='LORSGPRT',
        name='GDP(%T)',
        exchange='OECD',
        quoteType='INDEX',
        unit='%',
        comment='Trend (GDP)'
    ),
]

# METADATA FRED CODE
FRED = [
    # Bond and Interest Rate
    dict(
        ticker='FEDFUNDS',
        name='Federal Funds Effective Rate(M)',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='Federal Funds Effective Rate (Monthly)'
    ),
    dict(
        ticker='DFF',
        name='Federal Funds Effective Rate(D)',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='Federal Funds Effective Rate (Daily)'
    ),
    dict(
        ticker='DGS10',
        name='10-Year Constant Maturity(IB)',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis (Daily)'
    ),
    dict(
        ticker='DGS5',
        name='5-Year Constant Maturity(IB)',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='Market Yield on U.S. Treasury Securities at 5-Year Constant Maturity, Quoted on an Investment Basis (Daily)'
    ),
    dict(
        ticker='DGS2',
        name='2-Year Constant Maturity(IB)',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='Market Yield on U.S. Treasury Securities at 2-Year Constant Maturity, Quoted on an Investment Basis (Daily)'
    ),
    dict(
        ticker='DGS1',
        name='1-Year Constant Maturity(IB)',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='Market Yield on U.S. Treasury Securities at 1-Year Constant Maturity, Quoted on an Investment Basis (Daily)'
    ),
    dict(
        ticker='T10Y2Y',
        name='Treasury Yield Difference(10Y-2Y)',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity (Daily)'
    ),
    dict(
        ticker='T10Y3M',
        name='Treasury Yield Difference(10Y-3M)',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='10-Year Treasury Constant Maturity Minus 3-Month Treasury Constant Maturity (Daily)'
    ),
    dict(
        ticker='BAMLH0A0HYM2',
        name='High Yield Spread',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='ICE BofA US High Yield Index Option-Adjusted Spread (Daily)'
    ),
    dict(
        ticker='MORTGAGE30US',
        name='30-Year Fixed Rate Mortgage',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='30-Year Fixed Rate Mortgage Average in the United States (Weekly)'
    ),

    # Monetary
    dict(
        ticker='M2SL',
        name='M2',
        exchange='FRED',
        quoteType='INDEX',
        unit='USD(xB)',
        comment='M2: Billions of Dollars (Monthly)'
    ),
    dict(
        ticker='M2V',
        name='Velocity of M2 Money Stock',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='Velocity of M2 Money Stock (Seasonally Adjusted, Quarterly)'
    ),

    # Inflation
    dict(
        ticker='CPIAUCSL',
        name='CPI(SA)',
        exchange='FRED',
        quoteType='INDEX',
        unit='-',
        comment='Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (Seasonally Adjusted, Monthly)'
    ),
    dict(
        ticker='CPIAUCNS',
        name='CPI(Not SA)',
        exchange='FRED',
        quoteType='INDEX',
        unit='-',
        comment='Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (Not Seasonally Adjusted, Monthly)'
    ),
    dict(
        ticker='CORESTICKM159SFRBATL',
        name='CPI(Sticky Price, YoY)',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='Sticky Price Consumer Price Index less Food and Energy (Monthly)'
    ),
    dict(
        ticker='CPILFESL',
        name='CPI(without Food, Energy)',
        exchange='FRED',
        quoteType='INDEX',
        unit='-',
        comment='Consumer Price Index for All Urban Consumers: All Items Less Food and Energy in U.S. City Average (Seasonally Adjusted, Monthly)'
    ),
    dict(
        ticker='T10YIE',
        name='10-Year Breakeven Inflation Rate',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='10-Year Breakeven Inflation Rate (Daily, Not Seasonally Adjusted)'
    ),
    dict(
        ticker='T5YIE',
        name='5-Year Breakeven Inflation Rate',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='5-Year Breakeven Inflation Rate (Daily, Not Seasonally Adjusted)'
    ),
    dict(
        ticker='T5YIFR',
        name='5-Year Forward Inflation Expectation Rate',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='5-Year, 5-Year Forward Inflation Expectation Rate (Not Seasonally Adjusted, Daily)'
    ),

    # Labor, GDP, Saving and Others
    dict(
        ticker='UNRATE',
        name='Unemployment Rate',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='Unemployment Rate(Seasonally Adjusted, Monthly)'
    ),
    dict(
        ticker='ICSA',
        name='Initial Claims',
        exchange='FRED',
        quoteType='INDEX',
        unit='-',
        comment='Initial Claims, individual claims for Unemployment Insurance Program (Seasonally Adjusted, Weekly)'
    ),
    dict(
        ticker='GDP',
        name='Gross Domestic Product',
        exchange='FRED',
        quoteType='INDEX',
        unit='USD(xB)',
        comment='Gross Domestic Product (Seasonally Adjusted, Quarterly)'
    ),
    dict(
        ticker='GDPC1',
        name='Real Gross Domestic Product',
        exchange='FRED',
        quoteType='INDEX',
        unit='USD(xB)',
        comment='Real Gross Domestic Product (Seasonally Adjusted, Quarterly)'
    ),
    dict(
        ticker='PSAVERT',
        name='Personal Saving Rate',
        exchange='FRED',
        quoteType='INDEX',
        unit='%',
        comment='Personal Saving Rate (Monthly)'
    ),
    dict(
        ticker='UMCSENT',
        name='Consumer Sentiment',
        exchange='FRED',
        quoteType='INDEX',
        unit='-',
        comment='University of Michigan: Consumer Sentiment (Monthly)'
    ),
    dict(
        ticker='VIXCLS',
        name='VIX',
        exchange='FRED',
        quoteType='INDEX',
        unit='-',
        comment='CBOE Volatility Index: VIX (Daily)'
    ),
]

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), rf'Desktop/labwons')
os.makedirs(DESKTOP, exist_ok=True)

MAX_TRY_COUNT = 5
