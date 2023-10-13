from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in scalar divide"
)
warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in cast"
)


class rsi(baseDataFrameChart):
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

    def __init__(self, base:fetch):
        sampler = dict(
            momentum_rsi = 'rsi',
            momentum_stoch = 'stoch-osc',
            momentum_stoch_signal = 'stoch-osc-sig',
            momentum_stoch_rsi = 'stoch-rsi',
            momentum_stoch_rsi_k = 'stoch-rsi-k',
            momentum_stoch_rsi_d = 'stoch-rsi-d'
        )

        super().__init__(
            data=base.ta[sampler.keys()].rename(columns=sampler),
            name="RSI",
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            form='.2f',
            unit=base.unit,
            ref=base
        )
        return

    def figure(self) -> go.Figure:
        fig = Chart.r5c1nsy()
        fig.add_trace(row=1, col=1, trace=self.ref.ohlcv())
        fig.add_trace(row=2, col=1, trace=self.ref.ohlcv.v('barTY', name='거래량', showlegend=False))
        fig.add_trace(row=3, col=1, trace=self.lineTY('rsi', unit='%'))
        fig.add_hrect(row=3, col=1, y0=70, y1=100, line_width=0, fillcolor='red', opacity=0.2)
        fig.add_hrect(row=3, col=1, y0=0, y1=30, line_width=0, fillcolor='green', opacity=0.2)
        fig.add_trace(row=4, col=1, trace=self.lineTY('stoch-osc', unit='%'))
        fig.add_trace(row=4, col=1, trace=self.lineTY('stoch-osc-sig', unit='%', line_dash='dash'))
        fig.add_hrect(row=4, col=1, y0=80, y1=100, line_width=0, fillcolor='red', opacity=0.2)
        fig.add_hrect(row=4, col=1, y0=0, y1=20, line_width=0, fillcolor='green', opacity=0.2)
        fig.add_trace(row=5, col=1, trace=self.lineTY('stoch-rsi', unit=''))
        fig.add_trace(row=5, col=1, trace=self.lineTY('stoch-rsi-k', unit=''))
        fig.add_trace(row=5, col=1, trace=self.lineTY('stoch-rsi-d', unit=''))
        fig.add_hrect(row=5, col=1, y0=0.8, y1=1.0, line_width=0, fillcolor='red', opacity=0.2)
        fig.add_hrect(row=5, col=1, y0=0, y1=0.2, line_width=0, fillcolor='green', opacity=0.2)

        fig.update_layout(title=f"<b>{self.subject}</b> : RSI FAMILY")
        fig.update_yaxes(row=1, col=1, patch={"title": f"[{self.unit}]"})
        fig.update_yaxes(row=2, col=1, patch={"title": f"Vol."})
        fig.update_yaxes(row=3, col=1, patch={"title": f"RSI [%]"})
        fig.update_yaxes(row=4, col=1, patch={"title": f"S.OSC [%]"})
        fig.update_yaxes(row=5, col=1, patch={"title": f"S.RSI [-]"})
        return fig



