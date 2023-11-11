from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go


class products(baseDataFrameChart):
    def __init__(self, base:fetch):
        super().__init__(
            data=getattr(base, '_fnguide').annualProducts,
            name='PRODUCTS',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='%',
            ref=base
        )
        return

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r1c2nsy(specs=[[{"type": 'bar'}, {"type": "pie"}]], subplot_titles=["연간", "최근"])
        for col in self:
            fig.add_trace(
                trace=self(
                    col=col, style="barXY", drop=False,
                    marker=dict(opacity=0.85), showlegend=False
                ), row=1, col=1
            )
        fig.add_trace(
            trace=go.Pie(
                labels=self.iloc[-1].index,
                values=self.iloc[-1],
                showlegend=False,
                visible=True,
                automargin=True,
                opacity=0.85,
                textfont=dict(color='white'),
                textinfo='label+percent',
                insidetextorientation='radial',
                hoverinfo='label+percent',
            ), row=1, col=2
        )
        fig.update_layout(
            title=f"<b>{self.subject}</b>: {self.name}",
            barmode="stack",
            **kwargs
        )
        fig.update_xaxes(title="기말", row=1, col=1)
        fig.update_yaxes(title="비율[%]", row=1, col=1)
        return fig