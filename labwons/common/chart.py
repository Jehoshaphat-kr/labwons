# from labwons.common.config import PATH
# from labwons.equity.equity import Equity
# from labwons.indicator import Indicator
from plotly.subplots import make_subplots
import plotly.graph_objects as go


plot = {
    "bgcolor" : "white"
}

legendV = {
    "bgcolor" : "white",                # [str]
    "bordercolor" : "#444",             # [str]
    "borderwidth" : 0,                  # [float]
    "font" : {
        ''' User Defaults '''
    },
    "grouptitlefont" : {
        ''' User Defaults '''
    },
    "itemdoubleclick" : "toggleothers", # [str | bool] one of ( "toggle" | "toggleothers" | False )
    "itemsizing" : "trace",             # [str] one of ( "trace" | "constant" )
    "itemwidth" : 30,                   # [int] greater than or equal to 30
    "orientation" : "v",                # [str] one of ( "v" | "h" )
    "title" : {
        ''' User Defaults '''
    },
    "tracegroupgap" : 10,               # [int] greater than or equal to 0
    "traceorder" : "normal",            # [str] Any combination of "reversed", "grouped" joined with a "+" OR "normal"
    "valign" : "middle",                # [str] one of ( "top" | "middle" | "bottom" )
    "visible" : True,                   # [bool]
    "xref" : "paper",                   # [str] one of ( "container" | "paper" )
    "x" : 1.02,                         # [float]
    "xanchor" : "left",                 # [str] one of ( "auto" | "left" | "center" | "right" )
    "yref" : "paper",                   # [str] one of ( "container" | "paper" )
    "y" : 1,                            # [float]
    "yahcnor" : "auto"                  # [str] one of ( "auto" | "top" | "middle" | "bottom" )
}

legendH = legendV.copy().update({
    "orientation" : "h",
    "xanchor" : "right",
    "yanchor" : "bottom",
    "x" : 0.96,
    "y" : 1
})

hovermode = "closeset"                  # [str] one of ( "x" | "y" | "closest" | False | "x unified" | "y unified" )

dragmode = "zoom"                       # [str] one of ( "zoom" | "pan" | "select" | "lasso" | "drawclosedpath" |
                                        #                "drawopenpath" | "drawline" | "drawrect" | "drawcircle" |
                                        #                "orbit" | "turntable" | False )
xaxis = {
    "autorange" : True,                 # [str | bool] one of ( True | False | "reversed" | "min reversed" |
                                        #                       "max reversed" | "min" | "max" )
    "color" : "#444",                   # [str]
    "showgrid" : True,                  # [bool]
    "gridcolor" : "lightgrey",          # [str]
    "griddash" : "solid",               # [str] one of ( "solid" | "dot" | "dash" | "longdash" | "dashdot" )
    "gridwidth" : 0.5,                  # [float]
    "showline" : True,                  # [bool]
    "linecolor" : "grey",               # [str]
    "linewidth" : 1,                    # [float]
    "mirror" : False,                   # [str | bool] one of ( True | "ticks" | False | "all" | "allticks" )
    "rangeslider" : {
        "visible" : False
    },
    "rangeselector" : {
        "visible" : True,
        "bgcolor" : "#eee",             # [str]
        "bordercolor" : "#444",         # [str]
        "borderwidth" : 0,              # [float]
        "buttons" : [
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(count=2, label="3Y", step="year", stepmode="backward"),
            dict(step="all")
        ]
    },
    "showticklabels" : True,            # [bool]
    "tickformat" : "%Y/%m/%d",          # [str]
    "zeroline" : True,                  # [bool]
    "zerolinecolor" : "lightgrey",      # [str]
    "zerolinewidth" : 1                 # [float]
}

yaxis = {
    "autorange" : True,                 # [str | bool] one of ( True | False | "reversed" | "min reversed" |
                                        #                       "max reversed" | "min" | "max" )
    "color" : "#444",                   # [str]
    "showgrid" : True,                  # [bool]
    "griddash" : "solid",               # [str] one of ( "solid" | "dot" | "dash" | "longdash" | "dashdot" )
    "gridwidth" : 0.5,                  # [float]
    "showline" : True,                  # [bool]
    "linecolor" : "grey",               # [str]
    "linewidth" : 1,                    # [float]
    "mirror" : False,                   # [str | bool] one of ( True | "ticks" | False | "all" | "allticks" )
    "showticklabels" : True,            # [bool]
    "zeroline" : True,                  # [bool]
    "zerolinecolor" : "lightgrey",      # [str]
    "zerolinewidth" : 1                 # [float]
}



class MultiChart(object):
    # def __init__(self, *args):
    #     self.args = args
    #     self.units = list()
    #     for arg in args:
    #         if not arg.unit in self.units:
    #             self.units.append(arg.unit)
    #     if len(self.units) > 2:
    #         raise ValueError('The number of units of given object is more than 2. Unable to express dimensions')
    #     self._n_equity = len([arg for arg in args if isinstance(arg, Equity)])
    #     self._trs = list()
    #     self._ys = list()
    #     return



    @staticmethod
    def f1x1y2(**kwargs) -> go.Figure:
        fig = make_subplots(
            rows=1, cols=1,
            x_title='날짜', shared_xaxes=True,
            specs=[
                [{'secondary_y': True}]
            ]
        )
        fig.update_layout(
            plot_bgcolor='white',
            margin=dict(
                r=0
            ),
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=0.96,
                y=1
            ),
            hovermode="x unified",
            xaxis=dict(
                tickformat="%Y/%m/%d",
                showticklabels=True,
                showgrid=True,
                gridcolor='lightgrey',
                rangeslider=dict(
                    visible=False
                ),
                rangeselector=dict(
                    buttons=[
                        dict(count=1, label="1M", step="month", stepmode="backward"),
                        dict(count=3, label="3M", step="month", stepmode="backward"),
                        dict(count=6, label="6M", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(count=2, label="3Y", step="year", stepmode="backward"),
                        dict(step="all")
                    ]
                )
            ),
            yaxis=dict(
                # title=f'[{self.units[0]}]',
                showgrid=True,
                gridcolor='lightgrey',
            ),
            yaxis2=dict(
                # title=f'[{self.units[1]}]'
            )
        )
        for k, v in kwargs.items():
            if k in vars(go.Layout):
                fig.update_layout({k:v})
        return fig


    def _traces(self) -> list:
        if self._trs:
            return self._trs
        for elem in self.args:
            if isinstance(elem, Equity):
                if self._n_equity == 1:
                    ohlc = elem.ohlcv()
                    ohlc.showlegend = True
                    self._trs.append(ohlc)
                    self._ys.append(False if elem.unit == self.units[0] else True)
                typical = elem.typical(
                    line=dict(
                        color='black' if self._n_equity == 1 else None,
                        dash='dot' if self._n_equity == 1 else 'solid',
                        width=0.8 if self._n_equity == 1 else 1.0
                    )
                )
                self._trs.append(typical)
            elif isinstance(elem, Indicator):
                self._trs.append(elem())
            self._ys.append(False if elem.unit == self.units[0] else True)
        return self._trs

    def figure(self) -> go.Figure:
        if len(self.units) > 1:
            fig = self._figSeparate()
        else:
            fig = self._figUniform()
        return fig

    def _figUniform(self) -> go.Figure:
        fig = go.Figure(
            data=self._traces(),
            layout=go.Layout(
                title=", ".join([arg.name for arg in self.args]),
                plot_bgcolor="white",
                legend=dict(
                    orientation="h",
                    xanchor="right",
                    yanchor="bottom",
                    x=0.98,
                    y=1.02
                ),
                hovermode="x unified",
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
                    title="Date",
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
                    title=f"[{self.units[0]}]",
                    showgrid=True,
                    gridwidth=0.5,
                    gridcolor="lightgrey",
                    showline=True,
                    linewidth=1,
                    linecolor="grey",
                    mirror=False,
                    autorange=True
                ),
            )
        )
        return fig

    def _figSeparate(self) -> go.Figure:
        fig = make_subplots(
            rows=1, cols=1,
            x_title='날짜', shared_xaxes=True,
            specs=[
                [{'secondary_y': True}]
            ]
        )
        fig.add_traces(
            data=self._traces(),
            rows=[1] * len(self._traces()),
            cols=[1] * len(self._traces()),
            secondary_ys=self._ys
        )
        fig.update_layout(
            title=", ".join([arg.name for arg in self.args]),
            plot_bgcolor='white',
            margin=dict(r=0),
            legend=dict(
                orientation="h",
                xanchor="right",
                yanchor="bottom",
                x=0.96,
                y=1
            ),
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
            hovermode="x unified",
            xaxis=dict(
                tickformat="%Y/%m/%d",
                showticklabels=True,
                showgrid=True,
                gridcolor='lightgrey',
            ),
            yaxis=dict(
                title=f'[{self.units[0]}]',
                showgrid=True,
                gridcolor='lightgrey',
            ),
            yaxis2=dict(
                title=f'[{self.units[1]}]'
            )
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
            filename=f'{PATH.BASE}/f{"_".join([arg.name for arg in self.args])}.html'
        )
        kwargs.update(setter)
        plot(**kwargs)
        return