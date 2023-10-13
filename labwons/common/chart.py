from plotly.subplots import make_subplots
import plotly.graph_objects as go


class chart:

    @staticmethod
    def xaxis(**kwargs) -> dict:
        xaxis = {
            "autorange": True,              # [str | bool] one of ( True | False | "reversed" | "min reversed" |
                                            #                       "max reversed" | "min" | "max" )
            "color": "#444",                # [str]
            "showgrid": True,               # [bool]
            "gridcolor": "lightgrey",       # [str]
            "griddash": "solid",            # [str] one of ( "solid" | "dot" | "dash" | "longdash" | "dashdot" )
            "gridwidth": 0.5,               # [float]
            "showline": True,               # [bool]
            "linecolor": "grey",            # [str]
            "linewidth": 1,                 # [float]
            "mirror": False,                # [str | bool] one of ( True | "ticks" | False | "all" | "allticks" )
            "rangeslider": {
                "visible": False            # [bool]
            },
            "rangeselector": {
                "visible": True,            # [bool]
                "bgcolor": "#eee",          # [str]
                "bordercolor": "#444",      # [str]
                "borderwidth": 0,           # [float]
                "buttons": [
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all")
                ]
            },
            "showticklabels": True,         # [bool]
            "tickformat": "%Y/%m/%d",       # [str]
            "zeroline": True,               # [bool]
            "zerolinecolor": "lightgrey",   # [str]
            "zerolinewidth": 1              # [float]
        }
        for k, v in kwargs.items():
            if k in vars(go.layout.XAxis):
                xaxis.update({k:v})
        return xaxis

    @staticmethod
    def yaxis(**kwargs) -> dict:
        yaxis = {
            "autorange": True,              # [str | bool] one of ( True | False | "reversed" | "min reversed" |
                                            #                       "max reversed" | "min" | "max" )
            "color": "#444",                # [str]
            "showgrid": True,               # [bool]
            "gridcolor": "lightgrey",       # [str]
            "griddash": "solid",            # [str] one of ( "solid" | "dot" | "dash" | "longdash" | "dashdot" )
            "gridwidth": 0.5,               # [float]
            "showline": True,               # [bool]
            "linecolor": "grey",            # [str]
            "linewidth": 1,                 # [float]
            "mirror": False,                # [str | bool] one of ( True | "ticks" | False | "all" | "allticks" )
            "showticklabels": True,         # [bool]
            "zeroline": True,               # [bool]
            "zerolinecolor": "lightgrey",   # [str]
            "zerolinewidth": 1              # [float]
        }
        for k, v in kwargs.items():
            if k in vars(go.layout.YAxis):
                yaxis.update({k:v})
        return yaxis

    @staticmethod
    def legend(**kwargs) -> dict:
        legend = {
            "bgcolor": "white",                 # [str]
            "bordercolor": "#444",              # [str]
            "borderwidth": 0,                   # [float]
            "groupclick" : "togglegroup",       # [str] one of ( "toggleitem" | "togglegroup" )
            "itemclick" : "toggle",             # [str] one of ( "toggle" | "toggleothers" | False )
            "itemdoubleclick": "toggleothers",  # [str | bool] one of ( "toggle" | "toggleothers" | False )
            "itemsizing": "trace",              # [str] one of ( "trace" | "constant" )
            "itemwidth": 30,                    # [int] greater than or equal to 30
            "orientation": "h",                 # [str] one of ( "v" | "h" )
            "tracegroupgap": 10,                # [int] greater than or equal to 0
            "traceorder": "normal",             # [str] combination of "normal", "reversed", "grouped" joined with "+"
            "valign": "middle",                 # [str] one of ( "top" | "middle" | "bottom" )
            "xanchor": "right",                 # [str] one of ( "auto" | "left" | "center" | "right" )
            "x": 1.0,                           # [float] 1.02 for "v", 0.96 for "h"
            "yanchor": "top",                   # [str] one of ( "auto" | "top" | "middle" | "bottom" )
            "y": 1.0,                           # [float] 1.0 for both "v" and "h",

        }
        for k, v in kwargs.items():
            if k in vars(go.layout.Legend):
                legend.update({k:v})
        return legend

    @staticmethod
    def layout(**kwargs) -> dict:
        layout = {
            "plot_bgcolor": "white",            # [str] colors
            "hovermode": "x unified",           # [str] one of ( "x" | "y" | "closest" | False | "x unified" |
                                                #                "y unified" )
            "dragmode": "zoom",                 # [str] one of ( "zoom" | "pan" | "select" | "lasso" |
                                                #                "drawclosedpath" | "drawopenpath" | "drawline" |
                                                #                "drawrect" | "drawcircle" | "orbit" | "turntable" |
                                                #                False )
            "margin" : {
                "b" : 80,                       # [int] bottom margin
                "l" : 80,                       # [int] left margin
                "r" : 80,                       # [int] right margin
                "t" : 80                        # [int] top margin
            },
        }
        for k, v in kwargs.items():
            if k in vars(go.Layout):
                layout.update({k: v})
        return layout

    def r1c1nsy(self) -> go.Figure:
        fig = go.Figure()
        fig.update_layout(**self.layout(legend=self.legend()))
        fig.update_xaxes(patch=self.xaxis())
        fig.update_yaxes(patch=self.yaxis())
        return fig

    def r1c1sy1(self) -> go.Figure:
        return go.Figure()

    def r2c1nsy(self, **kwargs) -> go.Figure:
        _kwargs_ = dict(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.85, 0.15],
            vertical_spacing=0.01,
            x_title='Date',
        )
        _kwargs_.update(kwargs)
        fig = make_subplots(**_kwargs_)

        fig.update_layout(**self.layout(legend=self.legend()))
        fig.update_xaxes(row=1, col=1, patch=self.xaxis(showticklabels=False))
        fig.update_xaxes(row=2, col=1, patch=self.xaxis(rangeselector=None))
        fig.update_yaxes(row=1, col=1, patch=self.yaxis())
        fig.update_yaxes(row=2, col=1, patch=self.yaxis())
        return fig

    def r2c3nsy(self, **kwargs) -> go.Figure:
        _kwargs_ = dict(
            rows=2, cols=3,
            vertical_spacing=0.08,
            horizontal_spacing=0.04,
            x_title='Date',
            y_title='[x1 Average]',
        )
        _kwargs_.update(kwargs)
        fig = make_subplots(**_kwargs_)

        fig.update_layout(**self.layout())
        fig.update_yaxes(patch=self.yaxis())
        fig.update_xaxes(patch=self.xaxis(rangeselector=None))
        return fig

    def r4c1nsy(self, **kwargs) -> go.Figure:
        _kwargs_ = dict(
            rows=4, cols=1,
            shared_xaxes=True,
            row_width=[0.12, 0.12, 0.1, 0.66],
            vertical_spacing=0.01
        )
        _kwargs_.update(kwargs)
        fig = make_subplots(**_kwargs_)

        fig.update_layout(**self.layout(legend=self.legend()))
        fig.update_xaxes(row=1, col=1, patch=self.xaxis(showticklabels=False))
        fig.update_xaxes(row=2, col=1, patch=self.xaxis(showticklabels=False, rangeselector=None))
        fig.update_xaxes(row=3, col=1, patch=self.xaxis(showticklabels=False, rangeselector=None))
        fig.update_xaxes(row=4, col=1, patch=self.xaxis(rangeselector=None))
        fig.update_yaxes(row=1, col=1, patch=self.yaxis())
        fig.update_yaxes(row=2, col=1, patch=self.yaxis())
        fig.update_yaxes(row=3, col=1, patch=self.yaxis())
        fig.update_yaxes(row=4, col=1, patch=self.yaxis())
        return fig

    def r5c1nsy(self, **kwargs) -> go.Figure:
        _kwargs_ = dict(
            rows=5, cols=1,
            shared_xaxes=True,
            row_width=[0.15, 0.15, 0.15, 0.1, 0.45],
            vertical_spacing=0.01
        )
        _kwargs_.update(kwargs)
        fig = make_subplots(**_kwargs_)

        fig.update_layout(**self.layout(legend=self.legend()))
        fig.update_xaxes(row=1, col=1, patch=self.xaxis(showticklabels=False))
        fig.update_xaxes(row=2, col=1, patch=self.xaxis(showticklabels=False, rangeselector=None))
        fig.update_xaxes(row=3, col=1, patch=self.xaxis(showticklabels=False, rangeselector=None))
        fig.update_xaxes(row=4, col=1, patch=self.xaxis(showticklabels=False, rangeselector=None))
        fig.update_xaxes(row=5, col=1, patch=self.xaxis(rangeselector=None))
        fig.update_yaxes(row=1, col=1, patch=self.yaxis())
        fig.update_yaxes(row=2, col=1, patch=self.yaxis())
        fig.update_yaxes(row=3, col=1, patch=self.yaxis())
        fig.update_yaxes(row=4, col=1, patch=self.yaxis())
        fig.update_yaxes(row=5, col=1, patch=self.yaxis())
        return fig


# Alias
Chart = chart()

if __name__ == "__main__":
    myChart = Chart.r2c1nsy()
    myChart.add_trace(go.Scatter(x=[0, 2], y=[4, 2]), row=1, col=1)
    myChart.add_trace(go.Scatter(x=[1, 2], y=[1, 2]), row=2, col=1)
    myChart.show()
