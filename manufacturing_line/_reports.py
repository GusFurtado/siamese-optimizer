from abc import ABC, abstractmethod
from dataclasses import dataclass



class Report(ABC):

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def _repr_html_(self):
        pass

    def __repr__(self):
        return self.__str__()



@dataclass
class MachineReport(Report):
    machine : object

    def __post_init__(self):
        self.total = self.machine.time_starved \
            + self.machine.time_processing \
            + self.machine.time_blocked \
            + self.machine.time_broken

    def __str__(self):
        return f'''
        {self.machine.name} report
        {'-' * (len(self.machine.name)+7)}
        Model type       :  Machine
        Items processed  :  {self.machine.items_processed}
        Time starved     :  {self.machine.time_starved:,.2f} ({self.machine.time_starved/self.total:.2%})
        Time processing  :  {self.machine.time_processing:,.2f} ({self.machine.time_processing/self.total:.2%})
        Time blocked     :  {self.machine.time_blocked:,.2f} ({self.machine.time_blocked/self.total:.2%})
        Time broken      :  {self.machine.time_broken:,.2f} ({self.machine.time_broken/self.total:.2%})
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
                    <td>{self.machine.time_starved:,.2f}</td>
                    <td>{self.machine.time_starved/self.total:.2%}</td>
                </tr>
                <tr>
                    <td>Time processing</td>
                    <td>{self.machine.time_processing:,.2f}</td>
                    <td>{self.machine.time_processing/self.total:.2%}</td>
                </tr>
                <tr>
                    <td>Time blocked</td>
                    <td>{self.machine.time_blocked:,.2f}</td>
                    <td>{self.machine.time_blocked/self.total:.2%}</td>
                </tr>
                <tr>
                    <td>Time broken</td>
                    <td>{self.machine.time_broken:,.2f}</td>
                    <td>{self.machine.time_broken/self.total:.2%}</td>
                </tr>
            </tbody>
        </table>'''



@dataclass
class SourceReport(Report):
    source : object

    def __post_init__(self):
        self.total = self.source.time_creating \
            + self.source.time_blocked \
            + self.source.time_broken

    def __str__(self):
        return f'''
        {self.source.name} report
        {'-' * (len(self.source.name)+7)}
        Model type     :  Source
        Items created  :  {self.source.items_created}
        Time creating  :  {self.source.time_creating:,.2f} ({self.source.time_creating/self.total:.2%})
        Time blocked   :  {self.source.time_blocked:,.2f} ({self.source.time_blocked/self.total:.2%})
        Time broken    :  {self.source.time_broken:,.2f} ({self.source.time_broken/self.total:.2%})
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
                    <td>Items created</td>
                    <td>{self.source.items_created}</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Time blocked</td>
                    <td>{self.source.time_creating:,.2f}</td>
                    <td>{self.source.time_creating/self.total:.2%}</td>
                </tr>
                <tr>
                    <td>Time blocked</td>
                    <td>{self.source.time_blocked:,.2f}</td>
                    <td>{self.source.time_blocked/self.total:.2%}</td>
                </tr>
                <tr>
                    <td>Time broken</td>
                    <td>{self.source.time_broken:,.2f}</td>
                    <td>{self.source.time_broken/self.total:.2%}</td>
                </tr>
            </tbody>
        </table>'''



@dataclass
class LineReport(Report):
    line : object

    def __post_init__(self):
        self._equips = [equip for equip in self.line.__dict__.values() \
            if hasattr(equip, 'report')]

    def __str__(self):
        return ''.join([equip.report.__str__() for equip in self._equips])

    def _repr_html_(self):
        return '<br>'.join([equip.report._repr_html_() for equip in self._equips])
