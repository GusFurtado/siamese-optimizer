from dataclasses import dataclass

import simpy



@dataclass
class Source:
    name : str
    speed : float
    output_buffer : str



class _Source:

    def __init__(self, env:simpy.Environment, source:Source, objects:dict):
        self.env = env
        self.name = source.name
        self.output_buffer = objects[source.output_buffer]
        self.speed = source.speed
        self.process = self.env.process(self.produce())

    def produce(self):
        while True:
            yield self.env.timeout(self.speed)
            yield self.output_buffer.buffer.put(1)
