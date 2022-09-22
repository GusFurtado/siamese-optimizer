"""The reports submodule.

This submodule contains each model report, including:
- MachineReport
- SourceReport
- LineReport

These reports are loaded after the simulation run.

"""

from abc import ABC, abstractmethod



class Report(ABC):
    """Abstract base class of a simulation report."""

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def _repr_html_(self):
        pass

    def __repr__(self):
        return self.__str__()



class MachineReport(Report):

    def __init__(self, machine:object):
        self.machine = machine
        self.time_starved = machine.time_starved.total
        self.time_processing = machine.time_processing.total
        self.time_blocked = machine.time_blocked.total
        self.time_broken = machine.time_broken.total
        self.total = self.time_starved+self.time_processing+self.time_blocked+self.time_broken

    def __str__(self):
        return f'''
        {self.machine.name} report
        {'-' * (len(self.machine.name)+7)}
        Model type       :  Machine
        Items processed  :  {self.machine.items_processed}
        Time starved     :  {self.time_starved:,.2f} ({self.time_starved/self.total:.2%})
        Time processing  :  {self.time_processing:,.2f} ({self.time_processing/self.total:.2%})
        Time blocked     :  {self.time_blocked:,.2f} ({self.time_blocked/self.total:.2%})
        Time broken      :  {self.time_broken:,.2f} ({self.time_broken/self.total:.2%})
        '''

    def _repr_html_(self):
        return f'''<table>
            <thead>
                <th colspan="3">{self.machine.name} report</th>
            </thead>
            <tbody>
                <tr>
                    <td>Model type</td>
                    <td>Machine</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Items processed</td>
                    <td>{self.machine.items_processed}</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Time starved</td>
                    <td>{self.time_starved:,.2f}</td>
                    <td>{self.time_starved/self.total:.2%}</td>
                </tr>
                <tr>
                    <td>Time processing</td>
                    <td>{self.time_processing:,.2f}</td>
                    <td>{self.time_processing/self.total:.2%}</td>
                </tr>
                <tr>
                    <td>Time blocked</td>
                    <td>{self.time_blocked:,.2f}</td>
                    <td>{self.time_blocked/self.total:.2%}</td>
                </tr>
                <tr>
                    <td>Time broken</td>
                    <td>{self.time_broken:,.2f}</td>
                    <td>{self.time_broken/self.total:.2%}</td>
                </tr>
            </tbody>
        </table>'''



class SourceReport(Report):

    def __init__(self, source:object):
        self.source = source
        self.time_processing = source.time_processing.total
        self.time_blocked = source.time_blocked.total
        self.time_broken = source.time_broken.total
        self.total = self.time_processing+self.time_blocked+self.time_broken

    def __str__(self):
        return f'''
        {self.source.name} report
        {'-' * (len(self.source.name)+7)}
        Model type       :  Source
        Items processed  :  {self.source.items_processed}
        Time processing  :  {self.time_processing:,.2f} ({self.time_processing/self.total:.2%})
        Time blocked     :  {self.time_blocked:,.2f} ({self.time_blocked/self.total:.2%})
        Time broken      :  {self.time_broken:,.2f} ({self.time_broken/self.total:.2%})
        '''

    def _repr_html_(self):
        return f'''<table>
            <thead>
                <th colspan="3">{self.source.name} report</th>
            </thead>
            <tbody>
                <tr>
                    <td>Model type</td>
                    <td>Source</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Items processed</td>
                    <td>{self.source.items_processed}</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Time processing</td>
                    <td>{self.time_processing:,.2f}</td>
                    <td>{self.time_processing/self.total:.2%}</td>
                </tr>
                <tr>
                    <td>Time blocked</td>
                    <td>{self.time_blocked:,.2f}</td>
                    <td>{self.time_blocked/self.total:.2%}</td>
                </tr>
                <tr>
                    <td>Time broken</td>
                    <td>{self.time_broken:,.2f}</td>
                    <td>{self.time_broken/self.total:.2%}</td>
                </tr>
            </tbody>
        </table>'''



class LineReport(Report):

    def __init__(self, line:object):
        self.line = line
        self._equips = [equip for equip in line.__dict__.values() \
            if hasattr(equip, 'report')]

    def __str__(self) -> str:
        return ''.join([equip.report.__str__() for equip in self._equips])

    def _repr_html_(self) -> str:
        return '<br>'.join([equip.report._repr_html_() for equip in self._equips])
