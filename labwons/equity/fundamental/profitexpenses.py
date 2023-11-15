from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.common.service.tools import int2won
from labwons.equity.fetch import fetch
from plotly import graph_objects as go


class profitexpenses(baseDataFrameChart):
    colors = {
        "매출액": "#9BC2E6",
        "매출원가": "#FF7C80",
        "판매비와관리비": "#F4B084",
        "영업이익": "#A9D08E",
    }

    def __init__(self, base: fetch):
        ao = getattr(base, '_fnguide').annualOverview
        ar = getattr(base, '_fnguide').annualExpenses
        i = ar.index[0]

        super().__init__(
            data=getattr(base, '_fnguide').annualProfit,
            name='PROFIT EXPENSES',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='KRW',
            ref=base
        )
        # [list(self.colors.keys())]
        self["원가비율"] = round(100 * self["매출원가"] / self["매출액"], 2)
        self["판관비율"] = round(100 * self["판매비와관리비"] / self["매출액"], 2)
        self["영업이익율"] = round(100 * self["영업이익"] / self["매출액"], 2)
        self["금융수익"] = self["금융수익"] - self["금융원가"]
        return

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r1c1nsy()
        for n, col in enumerate(["매출액", "영업이익", "매출원가", "판매비와관리비"]):
            meta = self[
                {"매출원가": "원가비율", "판매비와관리비": "판관비율", "영업이익": "영업이익율"}[col]
            ] if n else None
            name = "판관비" if col == "판매비와관리비" else col
            fig.add_trace(
                trace=self(
                    col, 'barXY', drop=True,
                    base=0 if not n else None,
                    width=0.4,
                    offset=-0.4 if not n else 0.0,
                    meta=meta,
                    marker=dict(color=self.colors[col]),
                    customdata=[int2won(x) for x in self[col]],
                    texttemplate=name + ("<br>%{customdata}원<br>%{meta}%" if n else "<br>%{customdata}원"),
                    hovertemplate=name + (": %{customdata}원(매출대비 %{meta}%)" if n else ": %{customdata}원") + "<extra></extra>"
                )
            )
        fig.add_trace(
            trace=self(
                "금융수익", "lineXY", drop=True,
                visible='legendonly',
                meta=[int2won(x) for x in self["금융수익"]],
                line=dict(
                    dash="dot",
                ),
                customdata=round(100 * self["금융수익"] / self["매출액"], 2),
                texttemplate="%{meta}원",
                hovertemplate="금융수익: %{meta}원(매출대비: %{customdata}%)<extra></extra>"
            )
        )
        fig.update_layout(
            title=f"<b>{self.subject}</b> : {self.name}",
            barmode='stack',
            **kwargs
        )
        return fig
