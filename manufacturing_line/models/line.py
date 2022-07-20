from typing import List, Optional

from networkx import nx
import simpy

from manufacturing_line._reports import LineReport
from .base import Model
from .machine import Machine
from .source import Source



class Line:

    def __init__(self, *models):

        self.env = simpy.Environment()
        for model in models:
            self.add_models(model)


    def add_models(self, model:Model):

        if not isinstance(model, Model):
            raise TypeError(f"Can't add objects of type <{type(model)}>. It needs to be a <Model> object.")

        if model.name in self.__dict__:
            raise ValueError('Duplicated object name.')

        setattr(self, model.name, model)


    def plot(self, seed:Optional[int]=None):

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
        return LineReport(self)


    def simulate(self, time:int) -> None:

        for model in self.__dict__.values():
            if hasattr(model, '_before_run'):
                model._before_run(self.env, self.__dict__)

        self.env.run(until=time)

        for model in self.__dict__.values():
            if hasattr(model, '_after_run'):
                model._after_run()
