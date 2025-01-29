"""Module to parse plate reader outputs."""

import logging
import pandas as pd
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional

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
    def to_df(self, *args, **kwargs) -> Dict[str, pd.DataFrame]:
        """"""
        ...

@dataclass
class IControlXML(Measurements):
    """"""
    _data: dict = field(default_factory=dict, init=False)

    def read_file(self, filepath: str) -> None:
        """"""

        with open(filepath) as file:
            input = BeautifulSoup(file, "xml")

        self._data = {section["Name"]: {
            cycle["Cycle"]: {
                well["Pos"]: {scan["WL"]: scan.contents[0] for scan in well.select("Scan")} for well in cycle.select("Well")
            } for cycle in section.select("Data")
        } for section in input.select("Section")}

    def to_df(self) -> Dict[str, pd.DataFrame]:

        output = {}

        for section in self._data.keys():
            for cycle in self._data[section].keys():
                output[f"{section}_{cycle}"] = pd.DataFrame(self._data[section][cycle])

        return output