from typing import List

from networkx import nx
import simpy

from manufacturing_line._reports import LineReport
from .buffer import Buffer
from .machine import _Machine
from .source import _Source
from .base import Equipment, Model



class Line(Model):

    def __init__(self, *models):

        self.env = simpy.Environment()
        self._add_models(models, buffers=True)
        self._add_models(models, buffers=False)


    def _add_models(self, models:List, buffers:bool):

        for model in models:

            if not isinstance(model, Model):
                raise TypeError(f"Can't add objects of type <{type(model)}>. It needs to be a <Model> object.")

            if buffers and isinstance(model, Equipment):
                continue
            
            if (not buffers) and isinstance(model, Buffer):
                continue

            if model.name in self.__dict__:
                raise ValueError('Duplicated object name.')

            setattr(self, model.name, model._model_type(self.env, model, self.__dict__))



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
        return LineReport(self)


    def simulate(self, time:int) -> None:
        self.env.run(until=time)

        # Run every model "End" process
        for equip in self.__dict__.values():
            if hasattr(equip, '_end_run'):
                equip._end_run()
