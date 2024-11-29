"""Module to plot parsed plate reader ouptputs."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from .plate_reader import IControlXML, Measurements


@dataclass
class Plot(ABC):
    """"""

    @abstractmethod
    def load_data(self, Measurement: Measurements, *args, **kwargs) -> None:
        """"""
        ...

    def format_plot(
        self,
        axes: matplotlib.axes._axes.Axes,
        xlim: Optional[list[float]] = None,
        ylim: Optional[list[float]] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        square: Optional[bool] = False,
    ):

        if xlim is not None:
            axes.set_xlim(xlim)

        if ylim is not None:
            axes.set_ylim(ylim)

        if xlabel is not None:
            axes.set_xlabel(xlabel)

        if ylabel is not None:
            axes.set_ylabel(ylabel)

        if square == True:
            axes.set_box_aspect(1)


@dataclass
class IControlXMLPlot(Plot):
    """"""

    _plate_read: dict = field(default_factory=dict, init=False)

    def load_data(self, IControlXML: IControlXML) -> None:

        self._plate_read = IControlXML

    def get_wavelength_axis(self, section) -> np.ndarray:

        lmin, lmax, lstep = (
            self._plate_read.get_parameter(section, parameter)
            for parameter in [
                "Emission Wavelength Start",
                "Emission Wavelength End",
                "Emission Wavelength Step Size",
            ]
        )

        return np.arange(lmin, lmax + lstep, lstep)

    def plot_well_spectrum(
        self,
        axes: matplotlib.axes._axes.Axes,
        section: str,
        well: str,
        cycle: Optional[int] = 1,
        color: Optional[tuple] = (0, 0, 0),
        label: Optional[str] = None,
    ) -> None:

        data = np.array(list(self._plate_read.get_well(section, well, cycle).values()))

        ll = self.get_wavelength_axis(section)

        axes.plot(ll, data, color=color, label=label)
