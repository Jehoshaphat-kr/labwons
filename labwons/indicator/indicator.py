from labwons.common.metadata.metadata import MetaData
from labwons.common.config import DESKTOP
from labwons.indicator.fetch import (
    fetchEcos,
    fetchOecd,
    fetchFred
)
from pandas import Series
from datetime import datetime, timedelta
from plotly import graph_objects as go
from plotly.offline import plot
from os import path


class Indicator(Series):
    def __init__(
        self,
        ticker:str,
        *args,
        **kwargs,
    ):
        if not ticker in MetaData.index and not 'source' in kwargs:
            raise KeyError(f'@ticker: "{ticker}" NOT FOUND in metadata, @source must be specified')
        for key in kwargs:
            if not key in ['period', 'source', 'enddate', 'country', 'unit']:
                raise KeyError(f"Invalid keyword argument: {key} = {kwargs[key]}")
        _args_ = lambda k, replacement: kwargs[k] if k in kwargs else replacement

        period = _args_('period', 20)
        enddate = _args_('enddate', datetime.today().strftime("%Y%m%d"))
        startdate = (datetime.strptime(enddate, "%Y%m%d") - timedelta(period * 365)).strftime("%Y%m%d")
        source = _args_('source', MetaData.loc[ticker, 'exchange'])
        country = _args_('country', '')
        unit = _args_('unit', '')
        if source.lower() == 'oecd' and not country:
            raise KeyError(f"OECD data requires country code: ex) KOR@Korea, USA@USA, G-20@G-20...")
        if source.lower() == 'ecos' and not args:
            raise KeyError(f"ECOS data requires specific parameters")

        if source.lower() == 'ecos':
            series = fetchEcos(MetaData.API_ECOS, ticker, startdate, *args)
        elif source.lower() == 'oecd':
            series = fetchOecd(ticker, startdate, enddate, country)
        elif source.lower() == 'fred':
            series = fetchFred(ticker, startdate, enddate)
        else:
            raise KeyError(f'Invalid @source: "{source}", possible source is ["fred", "ecos", "oecd"]')
        super().__init__(index=series.index, data=series.values, name=ticker)

        self.ticker = ticker
        self.startdate = startdate
        self.enddate = enddate
        self.source = source
        self.dformat = '.2f'
        self.unit = MetaData.loc[ticker, 'unit'] if ticker in MetaData.index else unit
        return

    def trace(self, **kwargs) -> go.Scatter:
        trace = go.Scatter(
            name=self.name,
            x=self.index,
            y=self.values,
            visible=True,
            showlegend=True,
            mode='lines',
            connectgaps=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=self.dformat,
            hovertemplate=self.ticker + '<br>%{y}' + self.unit + '@%{x}<extra></extra>'
        )
        for key, val in kwargs.items():
            if key in vars(go.Scatter).keys():
                setattr(trace, key, val)
        return trace

    def figure(self) -> go.Figure:
        data = [self.trace()]
        layout = go.Layout(
            title=self.name,
            plot_bgcolor='white',
            legend=dict(
                xanchor='left',
                yanchor='top',
                x=0.0,
                y=1.0
            ),
            xaxis=dict(
                title='Date',
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.8,
            ),
            yaxis=dict(
                title=self.unit,
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.8
            )
        )
        fig = go.Figure(data=data, layout=layout)
        return fig

    def show(self):
        self.figure().show()
        return

    def save(self):
        plot(figure_or_data=self.figure(), auto_open=False, filename=path.join(DESKTOP, f"{self.name}.html"))
        return
