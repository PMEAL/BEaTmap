import importlib
import logging
from pathlib import Path

import numpy as np
from rich.logging import RichHandler

__all__ = [
    "index_of_value",
    "max_min",
    "lin_interp",
    "get_fixtures_path",
    "get_datasets_path",
    "find_package_root",
    "get_logger",
]


def index_of_value(array, value):
    """Finds the index of a value in an array most similar to value passed.

    Parameters
    ----------
    array : array
        Array of values.

    value : numeric
        Value you wish to find in array.

    Returns
    -------
    idx : array
        For 2D idx[0] = i index, idx[1] = j index.

    """
    X = np.abs(array - value)
    idx = np.where(X == 0)
    return idx


def max_min(array):
    """Finds maximum and minimum of an array.

    If multiple max and min values exist, all are returned.

    Parameters
    ----------
    array : array
        Array of values.

    Returns
    -------
    maximum : float
        Maximum value of array.
    max_idx : array
        For 2D max_idx[0] = i index, max_idx[1] = j index.
    minimum : float
        Minimum value of array.
    min_idx : array
        For 2D min_idx[0] = i index, min_idx[1] = j index

    """

    maximum = np.nanmax(array[np.nonzero(array)])
    minimum = np.nanmin(array[np.nonzero(array)])
    max_idx = index_of_value(array, maximum)
    min_idx = index_of_value(array, minimum)

    return maximum, max_idx, minimum, min_idx


def lin_interp(df, val):
    """Linerarly interpolates between two points.

    Specifically designed to find the relp corresponding to some value of n.

    Parameters
    ----------
    df : dataframe
        Contains raw data, realtaive pressure (relp) and amount adsorbed (n).

    Returns
    -------
    interp_val : float
        The relp corresponding to some n, between two (n, relp) points.

    """
    hindex = len(df[df["n"] <= val])
    if hindex == len(df):
        hindex = hindex - 1
    lindex = hindex - 1
    if hindex == 0:
        lindex = 0
        m = 0
    else:
        m = (df.loc[hindex, "relp"] - df.loc[lindex, "relp"]) / (
            df.loc[hindex, "n"] - df.loc[lindex, "n"]
        )

    b = df.loc[hindex, "relp"] - df.loc[hindex, "n"] * m

    interp_val = m * val + b
    return interp_val


def get_fixtures_path():
    """Returns the path to the fixtures directory."""
    return find_package_root("beatmap").joinpath("tests", "unit", "fixtures")


def get_datasets_path():
    """Returns the path to the datasets directory."""
    return find_package_root("beatmap").joinpath("beatmap", "io")


def find_package_root(package_name: str):
    """Finds the root directory of a Python package."""
    # Find the spec of the package
    package_spec = importlib.util.find_spec(package_name)

    # If the package could not be found, return None or raise an error
    if package_spec is None or package_spec.origin is None:
        return None  # or you could raise an error

    # The origin is the path to the __init__.py file of the package
    # We get the parent of that file to get the directory of the package
    package_dir = Path(package_spec.origin).parent

    return package_dir.parent


def get_logger(name: str) -> logging.Logger:
    """Returns a logger with the given name."""
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        # If logger has handlers, do not add another to avoid duplicate logs
        return logger
    
    logger.setLevel(logging.WARNING)  # Set the logging level to INFO for this logger.
    handler = RichHandler(rich_tracebacks=True)
    handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
    logger.addHandler(handler)
    return logger
