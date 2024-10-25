"""Module to parse plate reader outputs."""


import logging
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class Measurements(ABC):
    """"""

    @abstractmethod
    def read_file(self, filepath: str, *args, **kwargs) -> None:
        """"""
        ...

    @abstractmethod
    def get_data(self, *args, **kwargs):
        """"""
        ...

@dataclass
class IControlXML(Measurements):
    _data: dict = field(default_factory=dict, init=False)

    def read_file(self, filepath: str, filter: Optional[List[str]] = None) -> None:
        """"""

        try:

            tree = ET.parse(filepath)
            root = tree.getroot()

            def process_well(well):
                scans = {int(scan.get("WL")): float(scan.text) for scan in well.iter("Scan")}
                return scans

            def process_data(data):
                wells = {well.get("Pos"): process_well(well) for well in data.iter("Well")}
                return wells

            def process_section(section):
                parameters = {parameter.get("Name"): parameter.get("Value") for parameter in section.iter("Parameter")}
                data = {(data.get("Cycle"),data.get("Temperature")): process_data(data) for data in section.iter("Data")}
                return {"parameters": parameters,
                        "data": data}

            self._data = {section.get("Name"): process_section(section) for section in root.iter("Section") if filter is None or section.get("Name") in filter}

        except ET.ParseError as e:
            logging.error(f"Failed to parse the file at {filepath}", exc_info=e)

    def get_data(self):
        """"""
        return self._data