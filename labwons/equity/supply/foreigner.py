from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go


class foreigner(baseDataFrameChart):
    def __init__(self, base:fetch):
        super().__init__(
            data=getattr(base, '_fnguide').foreignRate,
            name='FOREIGN-RATE',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='KRW',
            ref=base
        )
        return

    @property
    def buttons(self) -> list:
        buttons = [
            {
                "label": "3개월",
                "method": "update",
                "args": [
                    {"visible": [True, True, False, False, False, False]},
                    {"title": f"<b>{self.subject}</b> : {self.name} (3개월)"}
                ]
            },
            {
                "label": "1년",
                "method": "update",
                "args": [
                    {"visible": [False, False, True, True, False, False]},
                    {"title": f"<b>{self.subject}</b> : {self.name} (1년)"}
                ]
            },
            {
                "label": "3년",
                "method": "update",
                "args": [
                    {"visible": [False, False, False, False, True, True]},
                    {"title": f"<b>{self.subject}</b> : {self.name} (3년)"}
                ]
            }
        ]
        return buttons

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r1c1sy1()
        for col in self:
            visible = True if col[0] == '3M' else False
            line = {
                "color": "royalblue" if col[1] == "종가" else "black",
                "dash": "solid" if col[1] == "종가" else "dot"
            }
            yhover = ",d" if col[1] == "종가" else ".2f"
            unit = "KRW" if col[1] == "종가" else "%"
            sy = False if col[1] == "종가" else True
            fig.add_trace(self(col, visible=visible, line=line, yhoverformat=yhover, name=col[1], unit=unit), secondary_y=sy)

        fig.update_layout(
            title=f"<b>{self.subject}</b> : {self.name} (3개월)",
            updatemenus=[
                dict(
                    direction="down",
                    active=0,
                    xanchor='left', x=0.005,
                    yanchor='bottom', y=0.99,
                    buttons=self.buttons
                )
            ],
            **kwargs
        )
        fig.update_yaxes(secondary_y=True, patch={"title": "외국인 비중 [%]"})
        fig.update_yaxes(secondary_y=False, patch={"title": "종가 [KRW]"})
        return fig
