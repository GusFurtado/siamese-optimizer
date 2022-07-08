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
        
        # Properties
        self.name = machine.name
        self.input_buffer = objects[machine.input_buffer]
        self.output_buffer = objects[machine.output_buffer]
        self.speed = machine.speed

        # Stats
        self.time_starved = 0
        self.time_processing = 0
        self.time_blocked = 0
        self.items_processed = 0
        
        # Environment
        self.env = env
        self.process = self.env.process(self.produce())


    def produce(self):
        while True:

            # Starving
            starving_start = self.env.now
            part = yield self.input_buffer.buffer.get()
            processing_start = self.env.now
            self.time_starved += (processing_start-starving_start)

            # Processing
            yield self.env.timeout(self.speed)
            blocked_start = self.env.now
            self.items_processed += 1
            self.time_processing += (blocked_start-processing_start)

            # Blocked
            yield self.output_buffer.buffer.put(part)
            self.time_blocked += (self.env.now-blocked_start)
