"""The Siamese Optimizer.

A Python toolkit for manufacturing and assembly lines simulation and optimization.

Main features
-------------
- Create and visualize a production line in a network.
- Simulate throughput, capacity and restrictions of machines and buffers.
- Work with failure times and statistical distributions.
- Generate simulation reports, plots and optimization suggestions.

Getting Started
---------------
Firstly, import the simulation building blocks:

>>> from siamese import (
...     Buffer,
...     Line,
...     Machine,
...     Source
... )

Optionally, import some of the support objects from the `failure` and
`distribution` submodules.

>>> from siamese.failures import TimeFailure
>>> from siamese.distributions import Uniform
>>> ...

Create the `Model` objects.

>>> entry_buffer = Buffer(
...     name = 'entry_buffer',
...     capacity = 4
... )

>>> source = Source(
...     name = 'source',
...     processing_time = dist.Exponential(1),
...     output_buffer = 'entry_buffer'
... )

>>> first_machine = Machine(
...     name = 'first_machine',
...     processing_time = 2,
...     input_buffer = 'entry_buffer',
...     output_buffer = 'first_buffer',
...     failure = failures.TimeFailure(
...         time_between_failures = dist.Uniform(10,20),
...         time_to_repair = dist.Triangular(1,2,3)
...     )
... )

Feed the `Line` object with the models.

>>> model = Line(
...     source,
...     first_machine,
...     second_machine,
...     entry_buffer,
...     first_buffer,
...     second_buffer,
...     last_machine,
...     last_buffer
... )

Plot the `Line` model to visualize your prodution line.

>>> model.plot(seed=4)

Run the simulation to generate reports.

>>> model.simulate(100)
>>> model.report

Home Page
---------
https://github.com/GusFurtado/siamese-optimizer

"""

from .models.buffer import Buffer
from .models.machine import Machine
from .models.line import Line
from .models.source import Source



__author__ = 'Gustavo Furtado'
__email__ = 'gustavofurtado2@gmail.com'
__version__ = '0.0.1'
