"""
Unit and regression test for the fluorescence_assay package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import fluorescence_assay


def test_fluorescence_assay_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "fluorescence_assay" in sys.modules
