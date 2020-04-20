import numpy as np


def index_of_value(array, value):
    """ Find the index of a value in an array most similar to value passed.

    Parameters
    __________
    array : array
        array containing values

    value : numeric
        value you wish to find in array

    Returns
    _______
    idx : array
        for 2D idx[0] = i index, idx[1] = j index

    """
    X = np.abs(array - value)
    idx = np.where(X ==0)
    return idx

def max_min(array):
    """Finds maximum and minimum of an array.
    
    Parameters
    __________
    array : array
        masked array of BET constant values
        
    Returns
    _______
    maximum : float

    max_idx : array
        for 2D max_idx[0] = i index, max_idx[1] = j index

    minimum : float

    min_idx : array
        for 2D min_idx[0] = i index, min_idx[1] = j index

    """

    maximum = np.nanmax(array[np.nonzero(array)])
    minimum = np.nanmin(array[np.nonzero(array)])
    max_idx = index_of_value(array, maximum)
    min_idx = index_of_value(array, minimum)
    return(maximum, max_idx, minimum, min_idx)
  
def mean_ignore0(array):
    """Computes the mean of an array's values, considering only non-zero values.
    
    Parameters
    __________
    array : array
        masked array of BET constant values
        
    Returns
    _______
    mean : float

    """
    col = array.sum(0)
    n_col = (array != 0).sum(0)
    mean = np.sum(col) / np.sum(n_col)
    return mean
    
    
def median_ignore0(array):
    """Computes the median of an array's values, considering only non-zero values.

    If there are an even number of non-zero values the median is the mean of the two
    central values.
    
    Parameters
    __________
    array : array
        masked array of BET constant values
        
    Returns
    _______
    median : float
    
    """

    m = np.ma.masked_equal(array, 0)
    median = np.ma.median(m)
    return median


def lin_interp(df, val):
    """Linerarly interpolates between two points.
    Specifically designed to find the relative pressure corresponding to some n
    
    Parameters
    __________
    df : dataframe
        containing relp and n columns
    
    Returns
    _______
    interp_val : float
        The relative pressure corresponding to some n, between two (n, relp) points
    
    
    """
    hindex = len(df[df['n'] <= val])
    if hindex == len(df):
        hindex = hindex -1
    lindex = hindex - 1
    if hindex == 0:
        lindex = 0
        m = 0
    else:
        m = (df.loc[hindex, 'relp'] - df.loc[lindex, 'relp']) /\
        (df.loc[hindex, 'n'] - df.loc[lindex, 'n'])
    
    b = df.loc[hindex, 'relp'] - df.loc[hindex, 'n'] * m
    
    interp_val = m * val + b
    return interp_val
