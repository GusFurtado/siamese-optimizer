"""The `Stats` class submodule.

The `Stats` class holds the values generated through the simulation and can be
accessed through the object's properties.

"""

from dataclasses import dataclass
from numbers import Number

import numpy as np
import plotly.graph_objects as go



@dataclass
class Stats:
    """The `Stats` class holds the values generated through the simulation.
    
    """

    total : Number
    values : list

    @property
    def len(self) -> int:
        return len(self.values)

    @property
    def max(self) -> Number:
        return max(self.values)

    @property
    def mean(self) -> Number:
        return np.mean(self.values)

    @property
    def min(self) -> Number:
        return min(self.values)

    def percentile(self, p:float, **kwargs) -> Number:
        return np.percentile(self.values, p, **kwargs)

    def histogram(self, **kwargs) -> go.Figure:
        return self._plot(go.Histogram, **kwargs)

    def boxplot(self, **kwargs) -> go.Figure:
        return self._plot(go.Box, **kwargs)

    def _plot(self, plot_type, **kwargs) -> go.Figure:
        return go.Figure(
            data = plot_type(x=self.values, **kwargs),
            layout = {
                'title': {'text': 'Time Distribution'},
                'xaxis': {'title': 'Time'},
                'yaxis': {'title': 'Frequency'}
            }
        )
