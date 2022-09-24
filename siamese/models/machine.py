"""The submodule that defines the `Machine` object.

`Machine` is a model object that holds entities during simulation.

Feed a `Line` object with this object.

"""

from dataclasses import dataclass
from numbers import Number
from typing import Optional, Union

import simpy

from siamese import distributions as dist
from siamese import failures as fail
from siamese.status import Status
from siamese._reports import MachineReport
from siamese._stats import Stats
from .base import Model



@dataclass
class Machine(Model):
    """Object that holds an entities for some time.

    Parameters
    ----------
    name : str
        A distinct name for this object.
    processing_time : Distribution | Number
        How long it takes to create a new entity.
    input_buffer : str
        Name of the `Buffer` object that will provide the entity.
    output_buffer : str
        Name of the `Buffer` object that will receive the processed entity.
    failure : Failure, optional
        The failure behavior of this object.
    
    """

    name : str
    processing_time : Union[dist.Distribution, Number]
    input_buffer : str
    output_buffer : str
    failure : Optional[fail.Failure] = None


    def _before_run(self, env:simpy.Environment, objects:dict):
        
        # Properties
        self._input_buffer = objects[self.input_buffer]
        self._output_buffer = objects[self.output_buffer]
        self.processing_time = dist._create_dist(self.processing_time)

        # Stats
        self.time_starved    = 0
        self.time_processing = 0
        self.time_blocked    = 0
        self.time_broken     = 0

        # Micromanagement stats
        self.starving_start_time   = 0
        self.processing_start_time = 0
        self.blocking_start_time   = 0
        self.failure_start_time    = 0

        self._starving_tracking   = []
        self._processing_tracking = []
        self._blocking_tracking   = []
        self._failure_tracking    = []

        self.status = Status.STARVING
        self.part = None
        
        # Environment
        self.env = env
        self.process = self.env.process(self._run_process())

        # Failure
        if isinstance(self.failure, fail.Failure):
            self.tbf = dist._create_dist(self.failure.time_between_failures)
            self.ttr = dist._create_dist(self.failure.time_to_repair)
            env.process(self._run_failure())


    def _run_process(self):
        while True:
            try:

                # Starving
                if self.status == Status.STARVING:
                    self._before_starving()
                    self.part = yield self._input_buffer._buffer.get()
                    self._after_starving()

                # Processing
                elif self.status == Status.PROCESSING:
                    self._before_processing()
                    yield self.env.timeout(self.processing_time.generate())
                    self._after_processing()

                # Block
                elif self.status == Status.BLOCKED:
                    self._before_blocking()
                    yield self._output_buffer._buffer.put(self.part)
                    self._after_blocking()

            # Failure
            except simpy.Interrupt:
                self._before_failing()
                yield self.env.timeout(self.ttr.generate())
                self._after_failing()
                self.fixed.succeed()


    def _run_failure(self):
        while True:
            yield self.env.timeout(self.tbf.generate())
            self.process.interrupt()
            self.fixed = self.env.event()
            yield self.fixed


    def _before_starving(self):
        self.starving_start_time = self.env.now


    def _after_starving(self):
        starving_duration = self.env.now-self.starving_start_time
        if starving_duration > 0:
            self._starving_tracking.append(starving_duration)
            self.time_starved += starving_duration
        self.status = Status.PROCESSING


    def _before_processing(self):
        self.processing_start_time = self.env.now


    def _after_processing(self):
        process_duration = self.env.now-self.processing_start_time
        self._processing_tracking.append(process_duration)
        self.time_processing += process_duration
        self.status = Status.BLOCKED


    def _before_blocking(self):
        self.blocking_start_time = self.env.now


    def _after_blocking(self):
        blocking_duration = self.env.now-self.blocking_start_time
        if blocking_duration > 0:
            self._blocking_tracking.append(blocking_duration)
            self.time_blocked += blocking_duration
        self.part = None
        self.status = Status.STARVING


    def _before_failing(self):
        self.failure_start_time = self.env.now
        self._add_current_status()


    def _after_failing(self):
        failure_duration = self.env.now-self.failure_start_time
        self._failure_tracking.append(failure_duration)
        self.time_broken += failure_duration


    def _after_run(self):
        self.items_processed = len(self._processing_tracking)
        self._add_current_status()

        # Generate `Stats` objects
        self.time_starved = Stats(
            total = self.time_starved,
            values = self._starving_tracking
        )
        self.time_processing = Stats(
            total = self.time_processing,
            values = self._processing_tracking
        )
        self.time_blocked = Stats(
            total = self.time_blocked,
            values = self._blocking_tracking
        )
        self.time_broken = Stats(
            total = self.time_broken,
            values = self._failure_tracking
        )

        # Clear micromanagement stats
        del self.starving_start_time
        del self.processing_start_time
        del self.blocking_start_time
        del self.failure_start_time


    def _add_current_status(self):
        if self.status == Status.STARVING:
            self.time_starved += (self.env.now-self.starving_start_time)
        elif self.status == Status.PROCESSING:
            self.time_processing += (self.env.now-self.processing_start_time)
        elif self.status == Status.BLOCKED:
            self.time_broken += (self.env.now-self.blocking_start_time)


    @property
    def report(self) -> str:
        return MachineReport(self)
