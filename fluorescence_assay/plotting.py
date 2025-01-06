"""Module to plot parsed plate reader ouptputs."""

from dataclasses import dataclass
from typing import Dict, Optional

import matplotlib.pyplot as plt


@dataclass
class Plot:
    """"""

    fig: plt.Figure = None
    ax: plt.Axes = None

    def __post_init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_box_aspect(1)
        plt.close(self.fig)

    def plot_well(self, data: dict[int, float], line: Optional[str] = None) -> None:

        if line is None:
            line = "k."

        for key, value in data.items():
            self.ax.plot(key, value, line)

    def save(
        self,
        filename: str,
        dpi: Optional[int] = None,
        format: Optional[str] = None,
        bbox_inches: Optional[str] = None,
    ) -> None:

        if dpi is None:
            dpi = 300
        if format is None:
            format = "pdf"
        if bbox_inches is None:
            bbox_inches = "tight"

        self.fig.savefig(filename, dpi=dpi, format=format, bbox_inches=bbox_inches)
