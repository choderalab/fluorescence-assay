"""Module to analyze data, including curve fitting."""

import logging
import numpy as np
import pandas as pd

from typing import Dict, List

from scipy.optimize import curve_fit

logger = logging.getLogger(__name__)