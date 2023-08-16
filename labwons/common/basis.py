from typing import Any, Union
from pandas import DataFrame, Series
from plotly import graph_objects as go
from plotly.offline import plot
import os


class baseDataFrameChart(DataFrame):
    _prop_ = {
        'dataName': '',
        'ticker': '',
        'unit': '',
        'path': '',
        'form': '.2f',
        'filename': '',
    }
    def __init__(self, frame:DataFrame, **kwargs):
        """
        Plotly 속성을 포함한 DataFrame
        :param df     : [DataFrame] 기본 데이터프레임
        :param kwargs : [dict] 속성 값 (아래는 필수 속성 키)
                        - @name, @unit, @path, @dtype
        """
        self._prop_ = {
            'dataName': '',
            'ticker': '',
            'unit': '',
            'path': '',
            'form': '.2f',
            'filename': '',
        }
        labels = {
            'dataName': 'name',
            'ticker': 'ticker',
            'unit': 'unit',
            'path': 'path',
            'form': 'dtype',
            'filename': 'filename'
        }

        super(baseDataFrameChart, self).__init__(
            index=frame.index,
            columns=frame.columns,
            data=frame.values
        )
        for k in self._prop_:
            if labels[k] in kwargs:
                self._prop_[k] = kwargs[labels[k]]

        self._prop_['filename'] = self._prop_['dataName']
        return

    @staticmethod
    def _overwrite(cls:Any, inst:Any, **kwargs) -> Any:
        for k in vars(cls):
            if k in kwargs:
                setattr(inst, k, kwargs[k])
        return inst

    @property
    def _dataName_(self) -> str:
        return self._prop_['dataName']

    @_dataName_.setter
    def _dataName_(self, dataName:str):
        self._prop_['dataName'] = dataName

    @property
    def _ticker_(self) -> str:
        return self._prop_['ticker']

    @_ticker_.setter
    def _ticker_(self, ticker:str):
        self._prop_['ticker'] = ticker

    @property
    def _unit_(self) -> str:
        return self._prop_['unit']

    @_unit_.setter
    def _unit_(self, unit:str):
        self._prop_['unit'] = unit

    @property
    def _path_(self) -> str:
        return self._prop_['path']

    @_path_.setter
    def _path_(self, path:str):
        self._prop_['path'] = path

    @property
    def _form_(self) -> str:
        return self._prop_['form']

    @_form_.setter
    def _form_(self, form:str):
        self._prop_['form'] = form


    @property
    def _filename_(self) -> str:
        return self._prop_['filename']

    @_filename_.setter
    def _filename_(self, filename:str):
        self._prop_['filename'] = filename

    def line(self, col:Union[str, tuple], data:DataFrame=DataFrame(), **kwargs) -> go.Scatter:
        data = (self if data.empty else data)[col].dropna()
        name = col if isinstance(col, str) else col[1]
        unit = kwargs['unit'] if 'unit' in kwargs else self._unit_
        trace = go.Scatter(
            name=name,
            x=data.index,
            y=data,
            mode='lines',
            visible=True,
            showlegend=True,
            connectgaps=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=self._form_,
            hovertemplate=name + '<br>%{y}' + _unit_ + '@%{x}<extra></extra>'
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def candle(self, data:DataFrame=DataFrame(), **kwargs) -> go.Candlestick:
        data = self if data.empty else data
        if not all([c in data for c in ['open', 'high', 'low', 'close']]):
            raise ValueError(f"Candlestick requires 'open', 'high', 'low', 'close' column data")
        trace = go.Candlestick(
            name=self._dataName_,
            x=self.index,
            open=self['open'],
            high=self['high'],
            low=self['low'],
            close=self['close'],
            visible=True,
            showlegend=True,
            increasing_line=dict(
                color='red'
            ),
            decreasing_line=dict(
                color='royalblue'
            ),
            xhoverformat='%Y/%m/%d',
            yhoverformat=self._form_,
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

    def scatter(self, col:str, data:DataFrame=DataFrame(), **kwargs) -> go.Scatter:
        data = (self if data.empty else data)[col].dropna()
        trace = go.Scatter(
            name=col,
            x=data.index,
            y=data,
            mode='markers',
            visible=True,
            showlegend=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=self._dtype_,
            hovertemplate='%{y} @%{x}<extra></extra>'
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def figure(self) -> go.Figure:
        pass

    def show(self):
        self.figure().show()
        return

    def save(self, filename:str=''):
        os.makedirs(self._path_, exist_ok=True)
        filename = filename if filename else self._filename_
        plot(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{self._path_}/{filename}.html'
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
        self.name = self._name_ = kwargs['name'] if 'name' in kwargs else ''
        self._ticker_ = kwargs['ticker'] if 'ticker' in kwargs else ''
        self._unit_ = kwargs['unit'] if 'unit' in kwargs else ''
        self._path_ = kwargs['path'] if 'path' in kwargs else r'./'
        self._form_ = kwargs['form'] if 'form' in kwargs else '.2f'
        self._filename_ = f"{self._name_}"
        return

    def __call__(self, mode:str='line', **kwargs) -> Union[go.Scatter, go.Bar]:
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
            name=self._name_,
            x=data.index,
            y=data,
            mode='lines',
            visible=True,
            showlegend=True,
            connectgaps=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=self._form_,
            hovertemplate=self._name_ + '<br>%{y}' + self._unit_ + '@%{x}<extra></extra>'
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def bar(self, data:Series=Series(dtype=float), **kwargs) -> go.Bar:
        data = (self if data.empty else data).dropna()
        trace = go.Bar(
            name=self._name_,
            x=data.index,
            y=data,
            visible=True,
            showlegend=False,
            xhoverformat='%Y/%m/%d',
            hovertemplate='%{y} @%{x}<extra></extra>'
        )
        return self._overwrite(go.Bar, trace, **kwargs)

    def scatter(self, data:Series=Series(dtype=float), **kwargs) -> go.Scatter:
        data = (self if data.empty else data).dropna()
        trace = go.Scatter(
            name=self._name_,
            x=data.index,
            y=data,
            mode='markers',
            visible='legendonly',
            showlegend=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=self._form_,
            hovertemplate='%{y} @%{x}<extra></extra>'
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def figure(self, mode:str='line') -> go.Figure:
        layout = go.Layout(
            title=self._name_,
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
                title=self._unit_,
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
        fig = go.Figure(data=self(mode), layout=layout)
        return fig

    def show(self, mode:str='line'):
        self.figure(mode).show()
        return

    def save(self, filename:str='', mode:str='line'):
        os.makedirs(self._path_, exist_ok=True)
        filename = filename if filename else self._filename_
        plot(
            figure_or_data=self.figure(mode),
            auto_open=False,
            filename=f'{self._path_}/{filename}.html'
        )
        return