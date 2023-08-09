from typing import Any
from pandas import DataFrame, Series
from plotly import graph_objects as go
from plotly.offline import plot


class baseDataFrameChart(DataFrame):

    _attr_ = dict()
    def __init__(self, frame:DataFrame, **kwargs):
        """
        Plotly 속성을 포함한 DataFrame
        :param df     : [DataFrame] 기본 데이터프레임
        :param kwargs : [dict] 속성 값 (아래는 필수 속성 키)
                        - @name, @unit, @path, @dtype
        """
        super().__init__(index=frame.index, columns=frame.columns, data=frame.values)
        self._attr_ = dict(name='', ticker='', unit='', path='', dtype='.2f')
        for k, v in kwargs.items():
            if k in self._attr_:
                self._attr_[k] = v
        return

    @staticmethod
    def _overwrite(cls:Any, inst:Any, **kwargs) -> Any:
        for k in vars(cls):
            if k in kwargs:
                setattr(inst, k, kwargs[k])
        return inst

    def line(self, col:str, data:DataFrame=DataFrame(), **kwargs) -> go.Scatter:
        data = (self if data.empty else data)[col]
        trace = go.Scatter(
            name=col,
            x=data.index,
            y=data,
            mode='lines',
            visible=True,
            showlegend=True,
            connectgaps=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=self._attr_['dtype'],
            hovertemplate=self._attr_['name'] + '<br>%{y}' + self._attr_['unit'] + '@%{x}<extra></extra>'
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def candle(self, data:DataFrame=DataFrame(), **kwargs) -> go.Candlestick:
        data = self if data.empty else data
        if not all([c in data for c in ['open', 'high', 'low', 'close']]):
            raise ValueError(f"Candlestick requires 'open', 'high', 'low', 'close' column data")
        trace = go.Candlestick(
            name=self._attr_['name'],
            x=self.index,
            open=self['open'],
            high=self['high'],
            low=self['low'],
            close=self['close'],
            visible=True,
            showlegend=False,
            increasing_line=dict(
                color='red'
            ),
            decreasing_line=dict(
                color='royalblue'
            ),
            xhoverformat='%Y/%m/%d',
            yhoverformat=self._attr_['dtype'],
        )
        return self._overwrite(go.Candlestick, trace, **kwargs)

    def bar(self, col:str, data:DataFrame=DataFrame(), **kwargs) -> go.Bar:
        data = (self if data.empty else data)[col].dropna()
        trace = go.Bar(
            name=col,
            x=data.index,
            y=data,
            visible=True,
            showlegend=False,
            xhoverformat='%Y/%m/%d',
            hovertemplate='%{y} @%{x}<extra></extra>'
        )
        return self._overwrite(go.Bar, trace, **kwargs)

    def figure(self) -> go.Figure:
        pass

    def show(self):
        self.figure().show()
        return

    def save(self, filename:str):
        plot(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{self._attr_["path"]}/{filename}.html'
        )
        return


class baseSeriesChart(Series):

    def __init__(self, series:Series, **kwargs):
        """
        Plotly 속성을 포함한 Series
        :param df     : [Series] 기본 데이터
        :param kwargs : [dict] 속성 값 (아래는 필수 속성 키)
                        - @name, @unit, @path, @dtype
        """
        super().__init__(index=series.index, data=series.values, dtype=series.dtype, name=series.name)
        self._attr_ = dict(name='', unit='', path='', dtype='')
        for k, v in kwargs.items():
            if k in self._attr_:
                self._attr_[k] = v
        self.name = self._attr_['name']
        return

    def __call__(self, mode:str='line', **kwargs):
        if mode == 'line':
            return self.line(**kwargs)
        elif mode == 'bar':
            return self.bar(**kwargs)
        else:
            raise KeyError

    @staticmethod
    def _overwrite(cls:Any, inst:Any, **kwargs) -> Any:
        for k in vars(cls):
            if k in kwargs:
                setattr(inst, k, kwargs[k])
        return inst

    def line(self, data:Series=Series(dtype=float), **kwargs) -> go.Scatter:
        data = (self if data.empty else data).dropna()
        trace = go.Scatter(
            name=self._attr_['name'],
            x=data.index,
            y=data,
            mode='lines',
            visible=True,
            showlegend=True,
            connectgaps=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=self._attr_['dtype'],
            hovertemplate=self._attr_['name'] + '<br>%{y}' + self._attr_['unit'] + '@%{x}<extra></extra>'
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def bar(self, data:Series=Series(dtype=float), **kwargs) -> go.Bar:
        data = (self if data.empty else data).dropna()
        trace = go.Bar(
            name=self._attr_['name'],
            x=data.index,
            y=data,
            visible=True,
            showlegend=False,
            xhoverformat='%Y/%m/%d',
            hovertemplate='%{y} @%{x}<extra></extra>'
        )
        return self._overwrite(go.Bar, trace, **kwargs)

    def figure(self, mode:str='line') -> go.Figure:
        layout = go.Layout(
            title=self._attr_['name'],
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
                showline=True,
                linecolor='grey',
                linewidth=1.0
            ),
            yaxis=dict(
                title=self._attr_['unit'],
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=True,
                zerolinecolor='lightgrey',
                zerolinewidth=0.8,
                showline=True,
                linecolor='grey',
                linewidth=1.0
            )
        )
        fig = go.Figure(data=self.line() if mode=='line' else self.bar(), layout=layout)
        return fig

    def show(self, mode:str='line'):
        self.figure(mode).show()
        return

    def save(self, filename:str='', mode:str='line'):
        filename = filename if filename else self._attr_['name']
        plot(
            figure_or_data=self.figure(mode),
            auto_open=False,
            filename=f'{self._attr_["path"]}/{filename}.html'
        )
        return

if __name__ == "__main__":
    from labwons.equity.ohlcv import _ohlcv

    df = _fetch('005930').ohlcv['close']

    # dfch = basisDataFrameChart(df)
    # print(dfch.line('close'))
    # print(dfch.line('close', line=dict(color='black')))
    # go.Figure(dfch.candle()).show()

    srch = baseSeriesChart(df)
    print(srch.line())