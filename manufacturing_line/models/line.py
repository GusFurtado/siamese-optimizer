from typing import List

from networkx import nx
import simpy

from .buffer import Buffer, _Buffer
from .machine import Machine, _Machine
from .source import Source, _Source



class Line:

    def __init__(
            self,
            sources: List[Source],
            machines: List[Machine],
            buffers: List[Buffer]
        ):

        self.env = simpy.Environment()
        self._add_objects(buffers, _Buffer)
        self._add_objects(sources, _Source)
        self._add_objects(machines, _Machine)


    def _add_objects(self, objects:List, object_type):
        for obj in objects:
            if obj.name in self.__dict__:
                raise ValueError('Duplicated object name.')
            setattr(self, obj.name, object_type(self.env, obj, self.__dict__))


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


    def simulate(self, time:int) -> None:
        self.env.run(until=time)
