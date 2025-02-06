"""Module to analyze data, including curve fitting."""

import logging
from typing import Dict, List, Union

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

logger = logging.getLogger(__name__)


def calculate_dose_response(
    dosed: Union[list[float], list[np.array]],
    ref: Union[list[float], list[np.array]],
    conc: Union[list[float], list[np.array]],
) -> pd.Series:
    """"""

    dosed = np.array(dosed)
    ref = np.array(ref)
    conc = np.array(conc)

    diff = np.array(dosed) - np.array(ref)

    return pd.Series(diff, index=conc)


def calculate_fraction_bound(dose_response: pd.Series) -> pd.Series:
    """"""

    conc = np.array(pd.Series.index.to_list())
    arr = dose_response.to_numpy()

    F_max = np.max(arr)
    F_min = np.min(arr)

    F_bound = (arr - F_min) / (F_max - F_min)

    return pd.Series(F_bound, index=conc)
