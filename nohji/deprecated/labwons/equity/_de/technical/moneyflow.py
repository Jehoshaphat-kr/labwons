from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from nohji.deprecated.labwons.equity import fetch
from plotly import graph_objects as go
import warnings
warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in scalar divide"
)
warnings.filterwarnings(
    "ignore",
    message="invalid value encountered in cast"
)


class moneyflow(baseDataFrameChart):
    """
    1) MFI: Money Flow Index
    MFI를 활용한 전략은 과매수와 과매도 신호를 기반으로 주식의 상승과 하락을 예측하거나
    거래 시점을 결정하는 데 도움을 주는 전략입니다. 아래는 MFI를 활용한 두 가지 전략 예시입니다.

        1. 과매수 및 과매도 신호로 매매 시점 결정:
        MFI가 80 이상이면 과매수 상태로 간주합니다. 즉, 시장이 너무 많이 상승하여 조정할
        가능성이 높습니다. 이때는 매도 포지션을 고려할 수 있습니다. MFI가 20 이하이면 과매도
        상태로 간주합니다. 즉, 시장이 너무 많이 하락하여 반등할 가능성이 높습니다.
        이때는 매수 포지션을 고려할 수 있습니다. 주의해야 할 점은, MFI가 80 이상이거나 20 이하일 때
        단순히 매수 또는 매도 결정을 하지 않는 것이 좋습니다. 추가적인 기술적 분석이나 다른 지표들과
        함께 고려하는 것이 중요합니다.

        2. MFI와 가격의 다이버전스 검출:
        MFI와 주식 가격 간의 다이버전스를 검출하여 추세의 반전을 파악하는 전략입니다.
        다이버전스란 가격과 기술적 지표 간의 불일치를 의미합니다. 상승하는 주가에 비해 MFI가
        하락하면, 강세가 약해질 가능성이 있습니다. 이는 주가의 상승이 둔화되고 하락할 수 있다는
        신호로 볼 수 있습니다. 이때는 매도 포지션을 고려할 수 있습니다. 반대로 하락하는 주가에
        비해 MFI가 상승하면, 약세가 약해질 가능성이 있습니다. 이는 주가의 하락이 둔화되고 반등할
        수 있다는 신호로 볼 수 있습니다. 이때는 매수 포지션을 고려할 수 있습니다.

    위 전략들은 MFI를 활용한 간단한 예시에 불과하며, 실제 투자나 거래 전략을 구성할 때에는 추가적인
    연구와 기술적 분석이 필요합니다. 또한 주식 시장은 변동성이 크고 예측이 어려운 특성이 있으므로
    투자자들은 항상 적절한 리스크 관리를 고려하고 전략을 구성해야 합니다.

    ----------------------------------------------------------------------------------------------

    2) CMF: Chaikin Money Flow
        1. 크로스오버 전략:
        CMF는 주식 시장에서 자금 흐름을 나타내는 값이므로, CMF가 0보다 큰지 작은지에 따라 주식의
        강세와 약세를 판단할 수 있습니다. 따라서 CMF가 0을 상향 돌파하는 경우 강세 신호로 간주하고,
        CMF가 0을 하향 돌파하는 경우 약세 신호로 간주합니다.

        2. CMF와 이동평균선(Moving Averages) 조합
        전략 개요: 단기 이동평균선과 장기 이동평균선을 활용하여 시그널을 생성하는 전략입니다.
        구현 방법: 예를 들어, 20일 이동평균선과 50일 이동평균선을 사용합니다. CMF가 0을 상향 돌파하고,
        20일 이동평균선이 50일 이동평균선을 상향 돌파하면 매수 신호로 간주할 수 있습니다. 반대로,
        CMF가 0을 하향 돌파하고, 20일 이동평균선이 50일 이동평균선을 하향 돌파하면 매도 신호로
        간주할 수 있습니다.

        3. CMF 다이버전스(Divergence)
        전략 개요: 가격과 CMF 지표 간의 다이버전스를 찾아내는 전략입니다. 다이버전스는 가격과 지표 간의
        상반된 움직임을 의미합니다. 예를 들어, 주식 가격이 상승하는데 CMF가 하락하는 경우, 다이버전스가
        발생한 것입니다.
        구현 방법: 다이버전스가 발생한 경우 가격 반전의 가능성이 높아질 수 있으므로, 매수 또는 매도 신호로
        활용할 수 있습니다.

        4. CMF와 볼린저 밴드(Bollinger Bands) 조합
        전략 개요: CMF 지표와 볼린저 밴드를 함께 사용하여 변동성과 자금 흐름의 상태를 확인하는 전략입니다.
        구현 방법: 볼린저 밴드와 CMF 지표를 함께 보면서, 볼린저 밴드의 너비가 확대되는 동시에 CMF 값이
        상승하는 경우 강세 신호로 간주할 수 있습니다. 반대로, 볼린저 밴드의 너비가 수축되는 동시에
        CMF 값이 하락하는 경우 약세 신호로 간주할 수 있습니다.

        5. CMF와 상대강도지수(Relative Strength Index, RSI) 조합
        전략 개요: CMF와 RSI 지표를 조합하여 과매수 및 과매도 구간에서 매매 신호를 발생시키는 전략입니다.
        구현 방법: RSI가 70을 상향 돌파하여 과매수 구간에 진입하는 동시에 CMF가 0을 상향 돌파하면 매도
        신호로 간주할 수 있습니다. 반대로, RSI가 30을 하향 돌파하여 과매도 구간에 진입하는 동시에
        CMF가 0을 하향 돌파하면 매수 신호로 간주할 수 있습니다.

    ----------------------------------------------------------------------------------------------

    3) OBV: On-Balance Volume
    OBV(On-Balance Volume) 기술적 분석은 주가와 거래량의 관계를 분석하여 추세를 파악하는 데 사용되는
    도구입니다. OBV는 거래량의 움직임을 주가 움직임과 비교하여 추세의 강도와 방향을 파악하는 데
    도움을 줍니다. 다음은 OBV를 활용한 매매 전략의 예시입니다.

        1. OBV의 상승과 하락 패턴 파악:
        OBV가 상승하는 동안 주가가 상승하는 경우 긍정적인 신호로 간주할 수 있습니다. 주가가 하락하는데
        OBV가 상승한다면 매수 신호로 간주할 수 있습니다. 마찬가지로, OBV가 하락하는 동안 주가가 상승하는
        경우 부정적인 신호로 판단할 수 있습니다.

        2. OBV의 추세선 분석:
        OBV의 추세선은 OBV의 평균값을 나타내는 선입니다. 추세선의 방향이 상승하면 상승 추세로, 하락하면
        하락 추세로 간주할 수 있습니다. 추세선이 상승하면 매수, 하락하면 매도 신호로 활용할 수 있습니다.

        3. OBV와 주가의 발산 현상 분석:
        OBV와 주가가 발산하는 현상은 추세의 전환 신호로 간주될 수 있습니다. 예를 들어, 주가가 상승하는데
        OBV가 하락하거나, 주가가 하락하는데 OBV가 상승하는 경우에는 추세의 반전이 예상될 수 있습니다.

        4. OBV와 다른 기술적 분석 지표의 조합:
        OBV를 단독으로 사용하는 것보다 다른 기술적 분석 지표와 조합하여 사용하는 것이 효과적일 수 있습니다.
        예를 들어, OBV와 이동평균선(Moving Average)을 함께 사용하면 추세의 강도와 방향을 더욱 정확하게
        분석할 수 있습니다.

    매매 전략은 개별 투자자의 투자 스타일과 선호하는 시장 조건에 따라 달라질 수 있습니다. 따라서, 위 전략은
    참고용으로 활용되어야 하며 실제 투자 결정에 앞서 추가적인 연구와 검증이 필요합니다. 항상 적절한 리스크
    관리를 포함하여 투자 결정을 내리는 것이 중요합니다.
    """

    def __init__(self, base:fetch):
        sampler = dict(
            volume_obv = 'obv',
            volume_cmf = 'cmf',
            volume_mfi = 'mfi',
        )
        super().__init__(
            data = base.ta[sampler.keys()].rename(columns=sampler),
            name = "MONEYFLOW INDEX",
            subject = f"{base.name}({base.ticker})",
            path = base.path,
            form = '.2f',
            unit = base.currency,
            ref = base
        )
        return

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r5c1nsy()
        fig.add_trace(row=1, col=1, trace=self.ref.ohlcv())
        fig.add_trace(row=2, col=1, trace=self.ref.ohlcv.v('barTY', name='Vol.', showlegend=False, marker={"color": "grey"}))
        fig.add_trace(row=3, col=1, trace=self('mfi', name='MFI', unit='%'))
        fig.add_hrect(row=3, col=1, y0=80, y1=100, line_width=0, fillcolor='red', opacity=0.2)
        fig.add_hrect(row=3, col=1, y0=0, y1=20, line_width=0, fillcolor='green', opacity=0.2)
        fig.add_trace(row=4, col=1, trace=self('cmf', name='CMF', unit=''))
        # fig.add_hrect(row=4, col=1, y0=80, y1=100, line_width=0, fillcolor='red', opacity=0.2)
        # fig.add_hrect(row=4, col=1, y0=0, y1=20, line_width=0, fillcolor='green', opacity=0.2)
        fig.add_trace(row=5, col=1, trace=self('obv', name='OBV', unit=''))

        fig.update_layout(title=f"<b>{self.subject}</b> : {self.name}", **kwargs)
        fig.update_yaxes(row=1, col=1, patch={"title": f"[{self.unit}]"})
        fig.update_yaxes(row=2, col=1, patch={"title": f"Vol."})
        fig.update_yaxes(row=3, col=1, patch={"title": f"MFI [%]"})
        fig.update_yaxes(row=4, col=1, patch={"title": f"CMF [-]"})
        fig.update_yaxes(row=5, col=1, patch={"title": f"OBV [-]"})
        return fig