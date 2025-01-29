"""Module to parse plate reader outputs."""

import logging
import pandas as pd
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class Data(ABC):
    """"""

    _data: dict = field(default_factory=dict, init=False)

    def read_IControlXML(self, filepath: str, name: Optional[str] = None) -> None:
        """"""

        if name is None:
            name = filepath

        xmldict = {}

        with open(filepath) as file:
            input = BeautifulSoup(file, "xml")

        # parse XML for relevant information
        # store in nested dictionary

        xmldict[name] = {section["Name"]: {
            cycle["Cycle"]: {
                well["Pos"]: {scan["WL"]: scan.contents[0] for scan in well.select("Scan")} for well in cycle.select("Well")
            } for cycle in section.select("Data")
        } for section in input.select("Section")}

        # convert to DataFrame

        for file, file_data in xmldict.items():
            for section, section_data in file_data.items():
                for cycle, cycle_data in section_data.items():

                    df = pd.DataFrame(cycle_data)
                    df = df.apply(pd.to_numeric, errors="coerce")

                    self._data[f"{file}_{section}_{cycle}"] = df
        
    def export_to_excel(self, filepath: str) -> None:

        with pd.ExcelWriter(filepath) as writer:

            for sheet_name, sheet_data in self._data.items():

                sheet_data.to_excel(writer, sheet_name=sheet_name)