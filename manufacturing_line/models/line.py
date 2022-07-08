from typing import List

from networkx import nx
import simpy

from .buffer import Buffer, _Buffer
from .machine import Machine, _Machine
from .source import Source, _Source
from .model import Model



class Line:

    def __init__(self, *models):

        self.env = simpy.Environment()
        self._add_models(models, buffers=True)
        self._add_models(models, buffers=False)


    def _add_models(self, models:List, buffers:bool):

        for model in models:

            if not isinstance(model, Model):
                raise 'Not a model'

            if buffers and (not isinstance(model, Buffer)):
                continue
            
            if (not buffers) and isinstance(model, Buffer):
                continue

            if model.name in self.__dict__:
                raise ValueError('Duplicated object name.')

            setattr(self, model.name, model._model_type()(self.env, model, self.__dict__))



    def plot(self):

        G = nx.DiGraph()

        for obj_name in self.__dict__:
            if obj_name != 'env':
                G.add_node(obj_name)

        for obj_name in self.__dict__:
            obj = self.__dict__[obj_name]
            if isinstance(obj, _Source):
                G.add_edge(obj.name, obj.output_buffer.name)

            elif isinstance(obj, _Machine):
                G.add_edge(obj.input_buffer.name, obj.name)
                G.add_edge(obj.name, obj.output_buffer.name)
        
        nx.draw_shell(G, with_labels=True)


    @property
    def report(self) -> str:
        return ''.join([model.report for model in self.__dict__.values() \
            if isinstance(model, _Machine) or isinstance(model, _Source)])


    def simulate(self, time:int) -> None:
        self.env.run(until=time)
