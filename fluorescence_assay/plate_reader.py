"""Module to parse plate reader outputs."""

import logging
import numpy as np
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

                    self._data[f"{file}_{section}_{cycle}"] = DFData(df)

    def get_df(self, df: str) -> pd.DataFrame:

        return self._data[df]
        
    # def export_to_excel(self, filepath: str) -> None:

    #     with pd.ExcelWriter(filepath) as writer:

    #         for sheet_name, sheet_data in self._data.items():

    #             sheet_data.to_excel(writer, sheet_name=sheet_name)

@dataclass
class DFData:
    """"""

    df: pd.DataFrame

    def get_WL(self, WL: int):
        """"""

        return Wavelength(self.df.loc[str(WL)])
    
    def get_plate(self, WL: int, format: Optional[int] = None):
        """"""

        if format is None:
            format = "96"

        if format == "96":
            plate = np.zeros((8,12))

        data = self.get_WL(WL)

        for series_index in data.index.tolist():

            alpha2num = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}

            row = alpha2num[series_index[0]]
            col = int(series_index[1]) - 1

            plate[row, col] = data.loc[series_index]

        return plate
    
@dataclass
class Wavelength:
    """"""

    series: pd.Series

    @property
    def plate(self):

        plate = np.zeros((8,12))
        
        for series_index in self.series.index.tolist():

            alpha2num = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}

            row = alpha2num[series_index[0]]
            col = int(series_index[1]) - 1

            plate[row, col] = self.series.loc[series_index]

        return plate