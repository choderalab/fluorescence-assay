"""Module to plot parsed plate reader ouptputs."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

import matplotlib
import matplotlib.axes
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
        title: Optional[str] = None,
        xlim: Optional[list[float]] = None,
        ylim: Optional[list[float]] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        square: Optional[bool] = False,
    ):
        
        if title is not None:
            axes.set_title(title)

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

    def plot_corrected_spectrum(
        self,
        axes: matplotlib.axes._axes.Axes,
        section: str,
        well_foreground: str,
        well_background: str,
        cycle: Optional[int] = 1,
        color: Optional[tuple] = (0, 0, 0),
        label: Optional[str] = None,
    ) -> None:

        foreground = np.array(
            list(self._plate_read.get_well(section, well_foreground, cycle).values())
        )
        background = np.array(
            list(self._plate_read.get_well(section, well_background, cycle).values())
        )

        difference = foreground - background

        ll = self.get_wavelength_axis(section)

        axes.plot(ll, difference, color=color, label=label)

    def plot_dose_response(
        self,
        axes: matplotlib.axes._axes.Axes,
        section: str,
        row_foreground: str,
        row_background: str,
        wavelength: int,
        concentrations: list[float],
        cycle: Optional[int] = 1,
        color: Optional[tuple] = (0, 0, 0),
        label: Optional[str] = None,
    ) -> None:

        differences = []

        for i in range(len(concentrations)):

            foreground = self._plate_read.get_well(
                section, f"{row_foreground}{i+1}", cycle
            )[wavelength]
            background = self._plate_read.get_well(
                section, f"{row_background}{i+1}", cycle
            )[wavelength]

            difference = foreground - background

            differences.append(difference)

        axes.plot(concentrations, differences, ".", color=color, label=label)
