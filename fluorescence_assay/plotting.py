"""Module to plot parsed plate reader ouptputs."""

from . import plate_reader

from typing import List, Optional

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages


def plot_spectra(
    spectra: list[pd.Series],
    concentrations: list[float],
    axes: Optional[Axes] = None,
    cmap: Optional[str] = None,
    norm: Optional[bool] = None
) -> None:
    """
    This function plots spectra of given concentrations with a colormap.
    """

    if axes is None:
        fig, axes = plt.subplots()
    if cmap is None:
        cmap = "winter_r"
    if norm is None:
        norm = plt.Normalize(vmin=min(concentrations), vmax=max(concentrations))

    cmap = plt.get_cmap(cmap)

    numSpectra = len(concentrations)

    for i in range(numSpectra):

        spectrum = spectra[i]

        xx_i = [int(x) for x in spectrum.index.to_list()]
        yy_i = spectrum.to_numpy()

        c = cmap(norm(concentrations[i]))

        axes.plot(xx_i, yy_i, color=c)


def create_grid_of_plots(
    rows: int,
    cols: int,
    hspace: Optional[float],
    wspace: Optional[float],
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    xscale: Optional[str] = None,
    yscale: Optional[str] = None,
    titles: Optional[list[str]] = None,
    fig: Optional[Figure] = None,
) -> list[Axes]:
    """"""

    if fig is None:
        fig = plt.figure()
    if hspace is None:
        hspace = 0
    if wspace is None:
        wspace = 0
    if xscale is None:
        xscale = "linear"
    if yscale is None:
        yscale = "linear"
    if xlabel is None:
        xlabel = ""
    if ylabel is None:
        ylabel = ""
    if titles is None:
        titles = ["" for i in range(cols)]

    gs = fig.add_gridspec(rows, cols, hspace=hspace, wspace=wspace)
    _ = gs.subplots(sharex="col", sharey="row")

    axes = fig.get_axes()

    for ax in axes:
        ax.label_outer()

    for i in range(rows*cols):
        axes[i].set_xscale(xscale)
        axes[i].set_yscale(yscale)

    xplots = np.arange(rows * cols - cols, rows * cols)
    for i in xplots:
        axes[i].set_xlabel(xlabel)

    yplots = cols * np.arange(0, rows)
    for i in yplots:
        axes[i].set_ylabel(ylabel)

    titleplots = np.arange(0, cols)
    for i in titleplots:
        axes[i].set_title(titles[i])

    return axes

#
# Above functions are helpful plotting utilities with relatively general implementations
# such that they can be used in multiple cases
#
# Below functions produce standard figures for a single assay format as described here
# 96 well microplate with the following layout
# - Rows:
#   - "A": Replicate 1, (+) protein
#   - "B": Replicate 1, (-) protein
#   - "C": Replicate 2, (+) protein
#   - "D": Replicate 2, (-) protein
#   - "E": Replicate 3, (+) protein
#   - "F": Replicate 3, (-) protein
#   - "G": Empty
#   - "H": Empty
# - Columns: For nonempty wells, each column has a different concentration of ligand dispensed
# Thus "A" - "B" gives the corrected fluorescence for replicate 1,
# and each well corresponds to a different ligand concentration
#
# TODO: Generalize implementation of 
#

def plot_fluorescence_spectra(df: plate_reader.DFData, concentrations: List[float], protein: str, ligand: str, pdf: Optional[PdfPages] = None):
    """"""

    fig = plt.figure(figsize=(21,14))

    norm = colors.AsinhNorm(linear_width=0.005, vmin=min(concentrations), vmax=max(concentrations))

    axes = create_grid_of_plots(2,
                                3,
                                hspace=0,
                                wspace=0.04,
                                fig=fig,
                                yscale="log",
                                xlabel="Emission Wavelength (nm)", 
                                ylabel="Fluorescence (RFU)",
                                titles=["Replicate 1",
                                        "Replicate 2",
                                        "Replicate 3"
                                        ]
                                        )
    
    plot2row = {"0": "A",
                "1": "C", 
                "2": "E", 
                "3": "B", 
                "4": "D", 
                "5": "F"
                }
    
    for i in range(6):

        ax = axes[i]

        row = plot2row[str(i)]

        spectra = df.get_row(row)

        if i in [0, 1, 2]:
            cmap = "winter_r"
        else:
            cmap = "Greys"

        plot_spectra(spectra, concentrations, ax, cmap=cmap, norm=norm)

        ax.set_xlim([380,600])
        ax.set_ylim([1e1,1e5])

    x0, y0, dx, dy = axes[2].get_position().bounds
    cax1 = fig.add_axes([x0+dx+0.01, y0, 0.0125, dy])
    cax2 = fig.add_axes([x0+dx+0.01, y0-dy, 0.0125, dy])

    fig.colorbar(cm.ScalarMappable(norm=norm, cmap="winter_r"), cax=cax1, ticks=[0,0.25,0.5,0.75], format="%.2f", label="Ligand Concentration (µM) in (+) Protein")
    fig.colorbar(cm.ScalarMappable(norm=norm, cmap="Greys"), cax=cax2, ticks=[0,0.25,0.5,0.75], format="%.2f", label="Ligand Concentration (µM) in (-) Protein")
    plt.suptitle(f"{protein}:{ligand}");

    if pdf is not None:
        pdf.savefig()
        plt.close()