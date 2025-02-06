"""Module to plot parsed plate reader ouptputs."""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Callable, Union, Optional

from matplotlib.axes import Axes
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes


def plot_fluorescence_spectra(spectra: List[pd.Series], concentrations: List[float], axes: Optional[Axes] = None, cmap: Optional[str] = None) -> None:
    """"""

    if axes is None:
        fig, axes = plt.subplots()

    if cmap is None:
        cmap = "winter"

    cmap = plt.get_cmap(cmap)

    norm = plt.Normalize(vmin=min(concentrations), vmax=max(concentrations))

    numSpectra = len(concentrations)

    for i in range(numSpectra):

        spectrum = spectra[i]

        xx_i = [int(x) for x in spectrum.index.to_list()]
        yy_i = spectrum.to_numpy()

        c = cmap(1-norm(concentrations[i]))

        axes.plot(xx_i, yy_i, color=c)

        # TODO: Colorbar

def plot_absorbance_spectrum(concentrations: List[float], spectrum: List[float], axes: Optional[Axes] = None) -> None:
    """"""

    if axes is None:
        fig, axes = plt.subplots()

    axes.plot(concentrations, spectrum)

def plot_dose_response(concentrations: List[float], dose_response: List[float], axes: Optional[Axes] = None) -> None:
    """"""

    if axes is None:
        fig, axes = plt.subplots()

    axes.plot(concentrations, dose_response)

def create_grid_of_plots(rows: int, cols: int, hspace: Optional[float], wspace: Optional[float], xlabel: Optional[str] = None, ylabel: Optional[str] = None, titles: Optional[List[str]] = None, fig: Optional[Figure] = None) -> List[Axes]:
    """"""

    if fig is None:
        fig = plt.figure()
    if hspace is None:
        hspace = 0
    if wspace is None:
        wspace = 0

    gs = fig.add_gridspec(rows, cols, hspace=hspace, wspace=wspace)
    _ = gs.subplots(sharex="col", sharey="row")

    axes = fig.get_axes()

    for ax in axes:
        ax.label_outer()

    if xlabel is not None:
        xplots = np.arange(rows*cols - cols, rows*cols)
        for i in xplots:
            axes[i].set_xlabel(xlabel)

    if ylabel is not None:
        yplots = cols*np.arange(0, rows)
        for i in yplots:
            axes[i].set_ylabel(ylabel)

    if titles is not None:
        titleplots = np.arange(0, cols)
        for i in titleplots:
            axes[i].set_title(titles[i])

    return axes