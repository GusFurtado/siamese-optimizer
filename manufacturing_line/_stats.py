from numbers import Number

import numpy as np
import plotly.graph_objects as go



class Stats(list):
    
    @property
    def max(self) -> Number:
        return max(self)

    @property
    def min(self) -> Number:
        return min(self)

    @property
    def len(self) -> int:
        return len(self)

    def percentile(self, p:float, **kwargs) -> Number:
        return np.percentile(self, p, **kwargs)

    def histogram(self, **kwargs) -> go.Figure:
        return self._plot(go.Histogram, **kwargs)

    def boxplot(self, **kwargs) -> go.Figure:
        return self._plot(go.Box, **kwargs)

    def _plot(self, plot_type, **kwargs) -> go.Figure:
        return go.Figure(
            data = plot_type(x=self, **kwargs),
            layout = {
                'title': {'text': 'Time Distribution'},
                'xaxis': {'title': 'Time'},
                'yaxis': {'title': 'Frequency'}
            }
        )
