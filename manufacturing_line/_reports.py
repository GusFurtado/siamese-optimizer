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

    def __str__(self):
        return f'''
        {self.machine.name} report
        {'-' * (len(self.machine.name)+7)}
        Model type       :  Machine
        Items processed  :  {self.machine.items_processed}
        Time starved     :  {self.machine.time_starved}
        Time processing  :  {self.machine.time_processing}
        Time blocked     :  {self.machine.time_blocked}
        '''

    def _repr_html_(self):
        return f'''<table>
            <thead>
                <th colspan="2">{self.machine.name} report</th>
            </thead>
            <tbody>
                <tr>
                    <td>Model type</td>
                    <td>Machine</td>
                </tr>
                <tr>
                    <td>Items processed</td>
                    <td>{self.machine.items_processed}</td>
                </tr>
                <tr>
                    <td>Time starved</td>
                    <td>{self.machine.time_starved}</td>
                </tr>
                <tr>
                    <td>Time processing</td>
                    <td>{self.machine.time_processing}</td>
                </tr>
                <tr>
                    <td>Time blocked</td>
                    <td>{self.machine.time_blocked}</td>
                </tr>
            </tbody>
        </table>'''



@dataclass
class SourceReport(Report):
    source : object

    def __str__(self):
        return f'''
        {self.source.name} report
        {'-' * (len(self.source.name)+7)}
        Model type     :  Source
        Items created  :  {self.source.items_created}
        Time blocked   :  {self.source.time_blocked}
        '''

    def _repr_html_(self):
        return f'''<table>
            <thead>
                <th colspan="2">{self.source.name} report</th>
            </thead>
            <tbody>
                <tr>
                    <td>Model type</td>
                    <td>Machine</td>
                </tr>
                <tr>
                    <td>Items created</td>
                    <td>{self.source.items_created}</td>
                </tr>
                <tr>
                    <td>Time blocked</td>
                    <td>{self.source.time_blocked}</td>
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
        return '<hr>'.join([equip.report._repr_html_() for equip in self._equips])
