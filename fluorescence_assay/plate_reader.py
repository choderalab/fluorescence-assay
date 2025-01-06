"""Module to parse plate reader outputs."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class Measurements(ABC):
    """"""

    @abstractmethod
    def read_file(self, filepath: str, *args, **kwargs) -> None:
        """"""
        ...

    @abstractmethod
    def get_well(self, *args, **kwargs) -> dict[int, float]:
        """"""
        ...

    @abstractmethod
    def get_parameter(self, *args, **kwargs):
        """"""
        ...


@dataclass
class IControlXML(Measurements):
    """"""

    _data: dict = field(default_factory=dict, init=False)

    def read_file(self, filepath: str, filter: Optional[list[str]] = None) -> None:
        """"""

        with open(filepath) as file:
            self._data = BeautifulSoup(file, "xml")

    def get_data(self):
        """"""

        return self._data

    def get_well(self, section, well, cycle: Optional[int] = 1):
        """"""

        def fix_type(val):
            try:
                return float(val)
            except:
                return float("nan")

        data = {
            int(scan["WL"]): fix_type(scan.contents[0])
            for scan in self._data.select(
                f'Section[Name="{section}"] > Data[Cycle="{str(cycle)}"] > Well[Pos="{well}"] > Scan'
            )
        }

        return data

    def get_parameter(self, section, parameter):

        def fix_type(val):
            try:
                return float(val)
            except:
                return val

        return fix_type(
            self._data.select(
                f'Section[Name="{section}"] > Parameters > Parameter[Name="{parameter}"]'
            )[0]["Value"]
        )
