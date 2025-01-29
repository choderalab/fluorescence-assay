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

    def read_file(self, filepath: str, name: Optional[str] = None) -> None:
        """"""

        if name is None:
            name = filepath

        with open(filepath) as file:
            input = BeautifulSoup(file, "xml")

        self._data[name] = {section["Name"]: {
            cycle["Cycle"]: {
                well["Pos"]: {scan["WL"]: scan.contents[0] for scan in well.select("Scan")} for well in cycle.select("Well")
            } for cycle in section.select("Data")
        } for section in input.select("Section")}

    def to_df(self, numeric: Optional[bool] = None) -> Dict[str, pd.DataFrame]:
        """"""

        if numeric is None:
            numeric = True
        else:
            numeric = False

        output = {}

        for file, file_data in self._data.items():
            for section, section_data in file_data.items():
                for cycle, cycle_data in section_data.items():
                    
                    df = pd.DataFrame(cycle_data)

                    if numeric:
                        df = df.apply(pd.to_numeric, errors="coerce")

                    output[f"{file}_{section}_{cycle}"] = df

        return output
    
    def export_to_excel(self, filepath: str) -> None:

        with pd.ExcelWriter(filepath) as writer:

            df = self.to_df()

            for sheet_name, sheet_data in df.items():

                sheet_data.to_excel(writer, sheet_name=sheet_name)