from labwons.common.basis import baseDataFrameChart
from labwons.common.chart import Chart
from labwons.equity.fetch import fetch
from plotly import graph_objects as go


class benchmarkmultiple(baseDataFrameChart):
    colors = [
        'royalblue',
        "#9BC2E6",
        "#A9D08E"
    ]
    def __init__(self, base:fetch):
        super().__init__(
            data=getattr(base, '_serv').benchmarkMultiples,
            name='BENCHMARK - MULTIPLES',
            subject=f"{base.name}({base.ticker})",
            path=base.path,
            unit='KRW',
            ref=base
        )
        return

    def figure(self, **kwargs) -> go.Figure:
        fig = Chart.r2c2nsy(
            subplot_titles=[col[0] for n, col in enumerate(self) if not n % 3],
            vertical_spacing=0.1,
            horizontal_spacing=0.08,
        )
        for n, col in enumerate(self):
            unit = '' if col[0].startswith('PER') or col[0].startswith('EV') else '%'
            kwargs = dict(
                col=col, style='barXY', drop=False,
                name=col[1], marker=dict(color=self.colors[n % 3]), unit=unit,
                showlegend=True if n < 3 else False, legendgroup=col[1],
                hovertemplate=col[1] + ": %{y}" + unit + "<extra></extra>"
            )
            row = 1 if col[0].startswith('PER') or col[0].startswith('EV') else 2
            col = 1 if col[0].startswith('PER') or col[0].startswith('ROE') else 2
            fig.add_trace(row=row, col=col, trace=self(**kwargs))

        fig.update_layout(
            title=f"<b>{self.subject}</b> : {self.name}",
            legend=dict(y=1.05),
            **kwargs
        )
        fig.update_yaxes(row=1, col=1, title='[-]')
        fig.update_yaxes(row=1, col=2, title='[-]')
        fig.update_yaxes(row=2, col=1, title='[%]')
        fig.update_yaxes(row=2, col=2, title='[%]')
        return fig
