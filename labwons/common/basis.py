from labwons.common.config import PATH
from labwons.common.chart import Chart
from typing import Any, Union
from pandas import DataFrame, Series
from plotly import graph_objects as go
from plotly.offline import plot
import os


class baseDataFrameChart(DataFrame):
    name = ''
    subject = ''
    path = ''
    form = ''
    unit = ''
    ref = None
    def __init__(
        self,
        data:DataFrame,
        name:str='',
        subject:str='',
        path:str=PATH.BASE,
        form:str='.2f',
        unit:str='',
        ref:Any=None,
        **kwargs
    ):
        """
        Plotly Trace 를 포함한 Pandas DataFrame
        :param data:    [DataFrame]* 기본 데이터프레임
        :param name:    [str] 데이터프레임 이름
        :param subject: [str] "{종목명(종목코드)}"
        :param path:    [str] 데이터프레임 및 시각 그래프 저장 경로
        :param form:    [str] 데이터프레임 포맷
        :param unit:    [str] 데이터프레임 단위
        :param ref:     [Any] 상위 레퍼런스 클래스
        """
        super(baseDataFrameChart, self).__init__(
            index=data.index,
            columns=data.columns,
            data=data.values
        )
        self.name = name
        self.subject = subject
        self.path = path
        self.form = form
        self.unit = unit
        self.ref = ref
        return

    def __call__(self, col:Union[str, tuple], style:str='lineTY', drop:bool=True, **kwargs):
        f = getattr(self, ''.join([method for method in dir(self) if method == style]))
        return f(col, drop, **kwargs)

    @staticmethod
    def _overwrite(cls:Any, inst:Any, **kwargs) -> Any:
        for k in vars(cls):
            if k in kwargs:
                setattr(inst, k, kwargs[k])
        return inst

    def lineTY(self, col:Union[str, tuple], drop:bool=True, **kwargs) -> go.Scatter:
        data = self[col].dropna() if drop else self[col]
        name = kwargs['name'] if 'name' in kwargs else col if isinstance(col, str) else '/'.join(col)
        unit = kwargs['unit'] if 'unit' in kwargs else self.unit
        form = kwargs['form'] if 'form' in kwargs else self.form
        trace = go.Scatter(
            name=name,
            x=data.index,
            y=data,
            mode='lines',
            visible=True,
            showlegend=True,
            connectgaps=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=form,
            hovertemplate=name + ': %{y}' + unit + '<extra></extra>'
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def lineXY(self, col:Union[str, tuple], drop:bool=True, **kwargs) -> go.Scatter:
        data = self[col].dropna() if drop else self[col]
        name = col if isinstance(col, str) else '/'.join(col)
        unit = kwargs['unit'] if 'unit' in kwargs else self.unit
        form = kwargs['form'] if 'form' in kwargs else self.form
        trace = go.Scatter(
            name=name,
            x=data.index,
            y=data,
            mode='lines+markers+text',
            visible=True,
            showlegend=True,
            textposition="bottom center",
            texttemplate="%{y:" + form + "}" + unit,
            yhoverformat=form,
            hovertemplate="%{y}" + unit + "<extra></extra>"
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def barTY(self, col:Union[str, tuple], drop:bool=True, **kwargs) -> go.Bar:
        data = self[col].dropna() if drop else self[col]
        name = kwargs['name'] if 'name' in kwargs else col if isinstance(col, str) else '/'.join(col)
        unit = kwargs['unit'] if 'unit' in kwargs else self.unit
        trace = go.Bar(
            name=name,
            x=data.index,
            y=data,
            visible=True,
            showlegend=True,
            xhoverformat='%Y/%m/%d',
            hovertemplate=name + ": %{y}" + unit + "<extra></extra>",
        )
        return self._overwrite(go.Bar, trace, **kwargs)

    def barXY(self, col:Union[str, tuple], drop:bool=True, **kwargs) -> go.Bar:
        data = self[col].dropna() if drop else self[col]
        name = kwargs['name'] if 'name' in kwargs else col if isinstance(col, str) else '/'.join(col)
        unit = kwargs['unit'] if 'unit' in kwargs else self.unit
        trace = go.Bar(
            name=name,
            x=data.index,
            y=data,
            visible=True,
            showlegend=True,
            textposition="inside",
            hovertemplate="%{y}" + unit + "<extra></extra>"
        )
        return self._overwrite(go.Bar, trace, **kwargs)

    def scatterTY(self, col:Union[str, tuple], drop:bool=True, **kwargs) -> go.Scatter:
        data = self[col].dropna() if drop else self[col]
        name = kwargs['name'] if 'name' in kwargs else col if isinstance(col, str) else '/'.join(col)
        unit = kwargs['unit'] if 'unit' in kwargs else self.unit
        trace = go.Scatter(
            name=name,
            x=data.index,
            y=data,
            mode='markers',
            visible=True,
            showlegend=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=self.form,
            hovertemplate="%{y}" + unit + "<extra></extra>"
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def candleStick(self, drop:bool=True, **kwargs) -> go.Candlestick:
        if not all([c in self for c in ['open', 'high', 'low', 'close']]):
            raise ValueError(f"Candlestick requires ['open', 'high', 'low', 'close'] column data")
        data = self.dropna() if drop else self
        trace = go.Candlestick(
            name=self.subject,
            x=data.index,
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            visible=True,
            showlegend=True,
            increasing_line=dict(
                color='red'
            ),
            decreasing_line=dict(
                color='royalblue'
            ),
            hoverinfo='x+y',
            xhoverformat='%Y/%m/%d',
            yhoverformat=self.form,
        )
        return self._overwrite(go.Candlestick, trace, **kwargs)

    def figure(self) -> go.Figure:
        pass

    def show(self):
        self.figure().show()
        return

    def save(self):
        os.makedirs(self.path, exist_ok=True)
        plot(
            figure_or_data=self.figure(),
            auto_open=False,
            filename=f'{self.path}/{self.name}.html'
        )
        return


class baseSeriesChart(Series):
    subject = ''
    path = ''
    form = ''
    unit = ''
    def __init__(
        self,
        data:Series,
        name:str='',
        subject:str='',
        path:str=PATH.BASE,
        form:str='.2f',
        unit:str='',
        **kwargs
    ):
        """
        Plotly Trace 를 포함한 Pandas DataFrame
        :param data:    [Series]* 기본 시계열데이터
        :param name:    [str] 시계열데이터 이름
        :param subject: [str] "{종목명(종목코드)}"
        :param path:    [str] 시계열데이터 및 시각 그래프 저장 경로
        :param form:    [str] 시계열데이터 포맷
        :param unit:    [str] 시계열데이터 단위
        """
        super(baseSeriesChart, self).__init__(
            index=data.index,
            data=data.values,
            dtype=data.dtype,
            name=name if name else data.name
        )
        self.subject = subject
        self.path = path
        self.form = form
        self.unit = unit
        return

    def __call__(self, mode:str='lineTY', drop:bool=True, **kwargs):
        f = getattr(self, ''.join([method for method in dir(self) if method == mode]))
        return f(drop, **kwargs)

    @staticmethod
    def _overwrite(cls:Any, inst:Any, **kwargs) -> Any:
        for k in vars(cls):
            if k in kwargs:
                setattr(inst, k, kwargs[k])
        return inst

    def lineTY(self, drop:bool=True, **kwargs) -> go.Scatter:
        data = self.dropna() if drop else self
        name = kwargs['name'] if 'name' in kwargs else str(self.name)
        trace = go.Scatter(
            name=name,
            x=data.index,
            y=data,
            mode='lines',
            visible=True,
            showlegend=True,
            connectgaps=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=self.form,
            hovertemplate=name + ': %{y}' + self.unit + '<extra></extra>'
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def lineXY(self, drop:bool=True, **kwargs) -> go.Scatter:
        data = self.dropna() if drop else self
        trace = go.Scatter(
            name=self.name,
            x=data.index,
            y=data,
            mode='lines+markers+text',
            visible=True,
            showlegend=True,
            textposition="bottom center",
            texttemplate="%{y}" + self.unit,
            yhoverformat=self.form,
            hovertemplate="%{x}: %{y}" + self.unit + "<extra></extra>"
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def barTY(self, drop:bool=True, **kwargs) -> go.Bar:
        data = self.dropna() if drop else self
        name = kwargs['name'] if 'name' in kwargs else str(self.name)
        trace = go.Bar(
            name=name,
            x=data.index,
            y=data,
            visible=True,
            showlegend=True,
            xhoverformat='%Y/%m/%d',
            yhoverformat=self.form,
            hovertemplate=name + ": %{y}" + self.unit + "<extra></extra>"
        )
        return self._overwrite(go.Bar, trace, **kwargs)

    def barXY(self, drop:bool=True, **kwargs) -> go.Bar:
        data = self.dropna() if drop else self
        trace = go.Bar(
            name=self.name,
            x=data.index,
            y=data,
            visible=True,
            showlegend=False,
            textposition="inside",
            texttemplate="%{y}" + self.unit,
            yhoverformat=self.form,
            hovertemplate="%{x}: %{y}" + self.unit + "<extra></extra>"
        )
        return self._overwrite(go.Bar, trace, **kwargs)

    def scatterXY(self, drop:bool=True, **kwargs) -> go.Scatter:
        data = self.dropna() if drop else self
        trace = go.Scatter(
            name=self.name,
            x=data.index,
            y=data,
            mode='markers',
            visible='legendonly',
            showlegend=True,
            yhoverformat=self.form,
            hovertemplate="%{x}: %{y}" + self.unit + "<extra></extra>"
        )
        return self._overwrite(go.Scatter, trace, **kwargs)

    def figure(self, mode:str='lineTY', drop:bool=True, **kwargs) -> go.Figure:
        fig = Chart.r1c1nsy()
        fig.add_trace(self(mode, drop, **kwargs))
        fig.update_layout(
            title=self.name
        )
        fig.update_xaxes(dict(
            title='Date'
        ))
        fig.update_yaxes(dict(
            title=f'{self.name}[{self.unit}]'
        ))
        return fig

    def show(self, mode:str='lineTY', drop:bool=True, **kwargs):
        self.figure(mode, drop, **kwargs).show()
        return

    def save(self, mode:str='lineTY', drop:bool=True, **kwargs):
        os.makedirs(self.path, exist_ok=True)
        plot(
            figure_or_data=self.figure(mode, drop, **kwargs),
            auto_open=False,
            filename=f'{self.path}/{self.name}.html'
        )
        return

if __name__ == "__main__":
    test = baseSeriesChart(Series())
    print(test())