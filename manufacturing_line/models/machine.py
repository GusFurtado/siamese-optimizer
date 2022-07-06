from dataclasses import dataclass

import simpy



@dataclass
class Machine:
    name : str
    speed : float
    input_buffer : str
    output_buffer : str



class _Machine:

    def __init__(self, env:simpy.Environment, machine:Machine, objects:dict):
        self.env = env
        self.name = machine.name
        self.input_buffer = objects[machine.input_buffer]
        self.output_buffer = objects[machine.output_buffer]
        self.speed = machine.speed
        self.process = self.env.process(self.produce())

    def produce(self):
        while True:
            part = yield self.input_buffer.buffer.get()
            yield self.env.timeout(self.speed)
            yield self.output_buffer.buffer.put(part)
