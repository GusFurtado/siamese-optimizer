"""The submodule that defines the `Line` object.

`Line` is a wrapper for `Model` objects that represents a production line.

The `Model` objects are:
- `Source`
- `Machine`
- `Buffer`

"""

from typing import Optional

from networkx import nx
import simpy

from siamese._reports import LineReport
from .base import Model
from .machine import Machine
from .source import Source



class Line:
    """Object that represents a production line.

    Through this object's methods, you can plot and simulate the line.

    It wraps `Model` objects, which are:
    - `Source`
    - `Machine`
    - `Buffer`

    Parameters
    ----------
    *models : Model
        Objects that make up the line.

    Methods
    -------
    add_model(model:Model)
        Add another `Model` object to the line.
    plot(seed=None)
        Draw a network of the `Model` objects connection.
    simulate(time)
        Run the simulation.

    Properties
    ----------
    report : LineReport
        Results of the simulation.

    """

    
    def __init__(self, *models):

        self.env = simpy.Environment()
        for model in models:
            self.add_model(model)


    def add_model(self, model:Model) -> None:
        """Add another `Model` object to the line.
        
        Parameters
        ----------
        model : Model
            New object to be added to the line.
        
        """

        if not isinstance(model, Model):
            raise TypeError(f"Can't add objects of type <{type(model)}>. It needs to be a <Model> object.")

        if model.name in self.__dict__:
            raise ValueError('Duplicated object name.')

        setattr(self, model.name, model)


    def plot(self, seed:Optional[int]=None):
        """Draw a network of the `Model` objects connection.

        Parameters
        ----------
        seed : int, optional
            Random state for deterministic node layouts.

        """

        D = {k:i for i, k in enumerate(self.__dict__)}
        G = nx.DiGraph()

        # Add models
        for obj_name in self.__dict__:
            if obj_name != 'env':
                G.add_node(D[obj_name])

        # Connect models
        for obj_name in self.__dict__:
            obj = self.__dict__[obj_name]
            if isinstance(obj, Source):
                G.add_edge(D[obj.name], D[obj.output_buffer])

            elif isinstance(obj, Machine):
                G.add_edge(D[obj.input_buffer], D[obj.name])
                G.add_edge(D[obj.name], D[obj.output_buffer])
        
        # Set models positions
        pos = nx.spring_layout(G, seed=seed)

        # Show legend
        legend_title = ['Legend', '------']
        for d in D:
            if isinstance(self.__dict__[d], Model):
                legend_title.append(f'({D[d]}) {d}')
        print('\n'.join(legend_title))

        # Draw
        return nx.draw(
            G = G,
            pos = pos,
            with_labels = True,
            font_size = 24,
            node_size = 2000,
            node_color = 'white',
            edgecolors = 'black',
            linewidths = 5,
            width = 5
        )


    @property
    def report(self) -> str:
        """Results of the simulation."""
        return LineReport(self)


    def simulate(self, time:int) -> None:
        """Run the simulation.

        Parameters
        ----------
        time : int
            Run the simulation until given time.
        
        """

        for model in self.__dict__.values():
            if hasattr(model, '_before_run'):
                model._before_run(self.env, self.__dict__)

        self.env.run(until=time)

        for model in self.__dict__.values():
            if hasattr(model, '_after_run'):
                model._after_run()
