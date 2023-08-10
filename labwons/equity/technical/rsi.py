from labwons.common.config import PATH
from labwons.equity._deprecated import _calc
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from pandas import DataFrame
import numpy as np
import warnings

warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in scalar divide"
)
warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in cast"
)


class rsi(DataFrame):
    """
    1) Stochastic Oscillator
    Stochastic Oscillator는 주식 시장에서 많이 사용되는 기술적 분석 도구 중 하나로,
    주식의 가격 움직임을 분석하여 과매수와 과매도 상태를 판단하는 데 도움을 줍니다.
    이를 계산하는 방법은 간단하지만 일반적으로 두 개의 값으로 판단합니다: %K 값과 %D 값입니다.

    일반적으로 Stochastic Oscillator의 설정은 주로 14일 기간을 사용합니다.
    하지만 설정은 트레이더의 개별적인 상황에 따라 다를 수 있습니다.

    %K 값 (K-line): 주식의 최근 종가가 일정 기간의 최고가와 최저가 사이의 상대적 위치를
    백분율로 표시한 값입니다. 공식은 다음과 같습니다.

        %K = ((현재 종가 - 최저가) / (최고가 - 최저가)) * 100

    일반적으로 %K 값이 80을 넘어서면 주식이 과매수 상태로 간주될 수 있습니다.

    %D 값 (D-line): %K 값의 3일 이동 평균입니다. 일반적으로 Slow Stochastic Oscillator라고도
    부릅니다. %D 값은 주식 가격의 부드러운 변화를 보여주며, 주식 시장에서의 트렌드를
    파악하는 데 도움을 줍니다.

        %D = 3일 동안의 %K 값의 평균

    일반적으로 %D 값이 80을 넘어서면 주식이 과매수 상태로 간주될 수 있습니다.

    과매수와 과매도 상태는 주식의 가격이 일시적으로 과도한 상태에 도달하여 가격 조정이
    예상될 수 있음을 나타냅니다. 따라서 %K 값과 %D 값이 80을 초과하면 주식이 과매수 상태에
    있을 가능성이 높으며, 반대로 20 미만의 값이 나오면 과매도 상태에 있을 가능성이 높습니다.
    그러나 이러한 값은 트레이더의 분석 방식이나 상황에 따라 다르게 해석될 수 있으므로
    다른 기술적 분석 지표와 함께 사용하는 것이 중요합니다.

    ----------------------------------------------------------------------------------------------

    2) Stochastic RSI
    스토캐스틱 RSI(Stochastic RSI)는 상대강도지수(Relative Strength Index, RSI)와
    스토캐스틱 오실레이터(Stochastic Oscillator)를 결합한 기술적 분석 지표입니다.
    RSI는 주식이나 다른 자산의 가격 움직임을 분석하고 추세의 강도를 측정하는 데 사용되는
    인기 있는 지표 중 하나이며, 스토캐스틱은 주식 가격이 일정 기간 동안 상대적으로 어디에
    위치하는지를 나타내는 데 사용됩니다. 스토캐스틱 RSI는 주식 시장이나 다른 금융 시장에서
    다음과 같은 방법으로 활용될 수 있습니다:

        1. 과매수와 과매도 신호 확인: 스토캐스틱 RSI는 0과 1 사이의 값을 갖기 때문에,
        0에 가까울수록 과매도 상태를 나타내며 1에 가까울수록 과매수 상태를 나타냅니다.
        주식 가격이 과매수 또는 과매도 지역에 도달하면 반전의 가능성이 높아지므로
        투자자는 해당 시점에 주의를 기울여야 합니다.

        2. 다이버전스 감지: 주가와 스토캐스틱 RSI 사이에 다이버전스가 발생하는 경우,
        가격 반전의 신호로 해석될 수 있습니다. 예를 들어, 주가가 상승하는데 스토캐스틱 RSI가
        하락하는 경우, 상승 흐름의 약화를 의미할 수 있습니다.

        3. 지속적인 추세 확인: 스토캐스틱 RSI는 주가 추세의 지속 여부를 확인하는 데 사용될
        수 있습니다. 오랜 기간 동안 스토캐스틱 RSI가 과매수 또는 과매도 지역에 머무르는 경우,
        현재 추세가 강력할 수 있습니다.

        4. 시그널 제공: 스토캐스틱 RSI가 특정 기준선을 넘어서거나 이를 교차하는 시점은
        매수 또는 매도 시그널을 제공하는 지점으로 활용될 수 있습니다.

    주의해야 할 점은 기술적 분석 지표가 항상 정확한 결과를 제공하지 않을 수 있다는 점입니다.
    따라서 스토캐스틱 RSI를 사용할 때는 다른 지표나 분석 방법과 함께 사용하고, 추가적인 검토와
    이해를 통해 결정을 내리는 것이 중요합니다. 또한, 과도한 트레이딩을 피하고 투자 전략에 따라
    활용하는 것이 좋습니다.
    """

    def __init__(self, base:_calc):
        COLUMNS = dict(
            momentum_rsi = 'rsi',
            momentum_stoch = 'stoch-osc',
            momentum_stoch_signal = 'stoch-osc-sig',
            momentum_stoch_rsi = 'stoch-rsi',
            momentum_stoch_rsi_k = 'stoch-rsi-k',
            momentum_stoch_rsi_d = 'stoch-rsi-d'
        )
        baseData = base.calcTA()[COLUMNS.keys()].rename(columns=COLUMNS)
        super().__init__(
            index=baseData.index,
            columns=baseData.columns,
            data=baseData.values
        )
        self._base_ = base
        return

    def __call__(self, col:str) -> go.Scatter:
        return self.trace(col)

    def trace(self, col:str) -> go.Scatter:
        basis = self[col].dropna()
        unit = '%' if col == 'rsi' else ''
        return go.Scatter(
            name=col.upper(),
            x=basis.index,
            y=basis,
            visible=True,
            showlegend=True,
            mode='lines',
            xhoverformat="%Y/%m/%d",
            yhoverformat=".2f",
            hovertemplate=col + "<br>%{y} " + unit + " @%{x}<extra></extra>"
        )

    def figure(self) -> go.Figure:
        fig = make_subplots(
            rows=5,
            cols=1,
            shared_xaxes=True,
            row_width=[0.15, 0.15, 0.15, 0.1, 0.45],
            vertical_spacing=0.01
        )
        fig.add_traces(
            data=[
                self._base_.ohlcv('candle'),
                self._base_.ohlcv('volume'),
                self.trace('rsi'),
                self.trace('stoch-osc'),
                self.trace('stoch-osc-sig'),
                self.trace('stoch-rsi'),
                self.trace('stoch-rsi-k'),
                self.trace('stoch-rsi-d'),
            ],
            rows=[1, 2, 3, 4, 4, 5, 5, 5],
            cols=[1, 1, 1, 1, 1, 1, 1, 1]
        )
        fig.add_hrect(y0=70, y1=100, line_width=0, fillcolor='red', opacity=0.2, row=3, col=1)
        fig.add_hrect(y0=0, y1=30, line_width=0, fillcolor='green', opacity=0.2, row=3, col=1)
        fig.add_hrect(y0=80, y1=100, line_width=0, fillcolor='red', opacity=0.2, row=4, col=1)
        fig.add_hrect(y0=0, y1=20, line_width=0, fillcolor='green', opacity=0.2, row=4, col=1)
        fig.add_hrect(y0=0.8, y1=1.0, line_width=0, fillcolor='red', opacity=0.2, row=5, col=1)
        fig.add_hrect(y0=0, y1=0.2, line_width=0, fillcolor='green', opacity=0.2, row=5, col=1)
        fig.update_layout(
            title=f"{self._base_.name}({self._base_.ticker}) RSI Family",
            plot_bgcolor="white",
            legend=dict(tracegroupgap=5),
            xaxis_rangeslider=dict(visible=False),
            xaxis_rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=2, label="3Y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            xaxis=dict(
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            xaxis2=dict(
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            xaxis3=dict(
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            xaxis4=dict(
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            xaxis5=dict(
                title="DATE",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            yaxis=dict(
                title=f"[{self._base_.unit}]",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            yaxis2=dict(
                title=f"",
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            yaxis3=dict(
                title='RSI [%]',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                mirror=False,
                autorange=True
            ),
            yaxis4=dict(
                title='STOCH-OSC[%]',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.5,
                mirror=False,
                autorange=True
            ),
            yaxis5=dict(
                title='STOCH-RSI[-]',
                showgrid=True,
                gridwidth=0.5,
                gridcolor="lightgrey",
                showline=True,
                linewidth=1,
                linecolor="grey",
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.5,
                mirror=False,
                autorange=True
            ),
        )
        return fig

    def show(self):
        self.figure().show()
        return

    def save(self, **kwargs):
        setter = kwargs.copy()
        kwargs = dict(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{self._base_.path}/RSI.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return



