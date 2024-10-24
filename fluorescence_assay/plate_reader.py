"""Comment."""

# TEST


import logging
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class Measurements(ABC):
    """"""

    def read_file(self, filepath: str, sections: list[str] | None = None) -> None:
        """"""
        self._parse_file(filepath, sections)
        return

    @abstractmethod
    def _get_data(self) -> dict:
        """"""
        ...

    # steps taken in read_file(...)

    @abstractmethod
    def _parse_file(self, filepath: str, sections: list[str] | None = None) -> None:
        """"""
        ...


@dataclass
class IControlXML(Measurements):
    _data: dict = field(default_factory=dict, init=False)

    def _parse_file(self, filepath: str, sections: list[str] | None = None) -> None:
        """"""

        try:

            tree = ET.parse(filepath)
            root = tree.getroot()

            # section > data > well > scan

            for section in root.findall(".//Section"):

                if sections is not None and section.get("Name") not in sections:
                    continue
                else:

                    # create section

                    self._data[section.get("Name")] = {"parameters": {}, "data": {}}

                    for parameter in section.findall(".//Parameter"):
                        parameter_name = parameter.get("Name")
                        parameter_value = parameter.get("Value")
                        parameter_unit = parameter.get("Unit")

                        try:
                            parameter_value = int(parameter_value)
                        except:
                            pass

                        self._data[section.get("Name")]["parameters"][
                            parameter_name
                        ] = (parameter_value, parameter_unit)

                    # create data

                    for data in section.findall(".//Data"):
                        cycle = int(data.get("Cycle"))
                        temperature = int(data.get("Temperature"))

                        self._data[section.get("Name")]["data"][
                            (cycle, temperature)
                        ] = {}

                        for well in data.findall(".//Well"):
                            pos = well.get("Pos")

                            self._data[section.get("Name")]["data"][
                                (cycle, temperature)
                            ][pos] = {}

                            for scan in well.findall(".//Scan"):
                                wl = int(scan.get("WL"))
                                value = float(scan.text)

                                self._data[section.get("Name")]["data"][
                                    (cycle, temperature)
                                ][pos][wl] = value

        except ET.ParseError as e:
            logging.error(f"Failed to parse the file at {filepath}", exc_info=e)

    def _get_data(self) -> dict:
        return self._data

    def get_parameter(self, section: str, parameter: str) -> tuple:
        return self._data[section]["parameters"][parameter]

    def get_value(self, section: str, data: tuple, pos: str, wl: int):
        return self._data[section]["data"][data][pos][wl]
