import numpy as np
import pandas as pd


__all__ = [
    "index_of_value",
    "max_min",
    "lin_interp",
]


def index_of_value(array, value):
    """ Finds the index of a value in an array most similar to value passed.

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
