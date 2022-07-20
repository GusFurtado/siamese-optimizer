from typing import List

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


    def plot(self):

        G = nx.DiGraph()

        for obj_name in self.__dict__:
            if obj_name != 'env':
                G.add_node(obj_name)

        for obj_name in self.__dict__:
            obj = self.__dict__[obj_name]
            if isinstance(obj, Source):
                G.add_edge(obj.name, obj.output_buffer.name)

            elif isinstance(obj, Machine):
                G.add_edge(obj.input_buffer.name, obj.name)
                G.add_edge(obj.name, obj.output_buffer.name)
        
        nx.draw_shell(G, with_labels=True)


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
