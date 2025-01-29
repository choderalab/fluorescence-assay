"""Module to plot parsed plate reader ouptputs."""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Callable, Union, Optional

from matplotlib.axes import Axes

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def plot_fluorescence_spectrum(data: List[pd.Series], conc: List[float], title: Optional[str] = None):

    fig, ax = plt.subplots()

    cmap_color = plt.get_cmap("winter")

    norm = plt.Normalize(vmin=min(conc), vmax=max(conc))

    xx = []

    for i in range(len(data)):

        series = data[i]

        xx_i = [int(x) for x in series.index.to_list()]
        yy_i = series.to_numpy()

        ax.plot(xx_i, yy_i, color=cmap_color(norm(conc[i])))

        xx += xx_i

    xmin = min(xx)
    xmax = max(xx)

    xticks = np.arange(xmin, xmax+20, 20)

    ax.set_box_aspect(1)
    ax.set_yscale("log")

    ax.set_xlim((xmin, xmax))
    ax.set_ylim((int(1e1),int(1e6)))
    ax.set_xticks(xticks)

    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Fluorescence (RFU)")

    sm = plt.cm.ScalarMappable(cmap=cmap_color, norm=norm)
    sm.set_array([])
    cbar1 = plt.colorbar(sm, ax=ax)
    cbar1.set_label(f"Ligand concentration (µM)")

    if title is not None:
        ax.set_title(title)

def plot_dose_response_curve(protein: List[float], drug: List[float], conc: List[float], fraction_bound: Optional[bool] = None):

    if fraction_bound is None:
        fraction_bound = True
    else:
        fraction_bound = False

    dose_response = protein - drug

    fig, ax = plt.subplots()

    if fraction_bound:
        F_max = np.max(dose_response)
        F_min = np.min(dose_response)

        F_bound = (dose_response - F_min)/(F_max - F_min)

        ax.plot(conc, F_bound, "r.")
        ax.set_ylabel("Fraction Bound")
    else:
        ax.plot(conc, dose_response, "r.")
        ax.set_ylabel("Corrected Fluorescence (RFU)")
        
    ax.set_xscale("log")
    ax.set_xlabel("Ligand Concentration (µM)")
    ax.set_box_aspect(1)