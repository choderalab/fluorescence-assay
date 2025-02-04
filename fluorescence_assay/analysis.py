"""Module to analyze data, including curve fitting."""

import logging
from typing import Dict, List

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

logger = logging.getLogger(__name__)
