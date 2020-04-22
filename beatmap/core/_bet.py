#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:05:19 2019

@author: ellsworthbell
"""

import numpy as np
import scipy as sp
import beatmap.utils as util

avagadro = 6.022*10**23


def bet(df, a_o):
    """Performs BET analysis on an isotherm data set for all relative pressure
        ranges.
    This is the meat and potatoes of the whole package.

    Parameters
    ----------
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    a_o : float
        adsorbate cross section area, can be found from get adsorbate function
        or input by user, units must be [square angstrom]

    Returns
    -------
    sa_array : array
        2D array of BET specific surface areas, the coordinates of the array
        corresponding to relative pressures, units [square meter / gram]

    c_array : array
        2D array of BET constants, the coordinates of the array
        corresponding to relative pressures

    nm_array : array
        2D array of BET specific amount of adsorbate in the monolayer, the
        coordinates of the array corresponding to relative pressures, units
        [moles / gram]

    err_array : array
        2D array of error between experimental data and BET theoretical
        isotherms, the coordinates of the array corresponding to relative
        pressures

    lin_reg : array
        3D array, x by x by 3 where x is the number of experimental data points
        the x and x corrdinates corresponding to relative pressure
        this array is available for reference and BET theory checks


    """
    sa_array = np.zeros((len(df), len(df)))
    c_array = np.zeros((len(df), len(df)))
    nm_array = np.zeros((len(df), len(df)))
    err_array = np.zeros((len(df), len(df)))
    lin_reg = np.zeros((len(df), len(df), 3))
    bet_c = np.zeros(len(df.relp))

    for i in range(len(df)-1):
        for j in range(len(df)-1):
            if i > j:
                a = df.iloc[j:i+1]
                X = a.relp
                y = a.bet
                slope, intercept, r_value, p_value, std_err =\
                    sp.stats.linregress(X, y)
                lin_reg[i, j, 0] = slope
                lin_reg[i, j, 1] = intercept
                lin_reg[i, j, 2] = r_value
                c = 0
                nm = 0
                bet_c = 0
                if intercept != 0:
                    c = slope/intercept + 1  # avoiding divide by zero issues
                    nm = 1 / (intercept * c)
                    bet_c = (1 / (nm * c)) + (c - 1) * df.relp / (nm * c)
                spec_sa = nm * avagadro * a_o * 10**-20
                sa_array[i, j] = spec_sa
                c_array[i, j] = c
                nm_array[i, j] = nm
                errors = np.nan_to_num(abs(bet_c - df.bet))
                err_array[i, j] = sum(errors[j:i + 1]) / (i + 1 - j)
                # error is normalized for the interval of relative pressures
                # used to compute C, so, min and max error corresponds to the
                # best and worst fit over the interval used in BET analysis,
                # not the entire isotherm
    np.nan_to_num(lin_reg)
    return sa_array, c_array, nm_array, err_array, lin_reg
# lin reg is a 3d array of values from linear regression used in bet analysis


def single_point_bet(df, a_o):

    sa_array = np.zeros((len(df), len(df)))
    nm_array = np.zeros((len(df), len(df)))

    for i in range(len(df)):
        for j in range(len(df)):
            if i > j:
                n_range = df.n[j:i]
                relp_range = df.relp[j:i]
                n = np.ma.median(n_range)
                relp = np.ma.median(relp_range)

                nm_array[i, j] = n * (1-relp)
                sa_array[i, j] = n * avagadro * a_o * 10**-20

    return sa_array, nm_array


# function currently not being used
def theta(df, nm):
    """Computes "theta" for the BET analysis in each pressure range.
    theta = n/nm
    depending on the choice of n, theta can represent different things
    in this case, if n = the median n for the relative pressure range
    then theta gives an idea of how "centered" nm is in the relative pressure
    range

    Parameters
    __________
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    nm : array
        2D array of BET specific amount of adsorbate in the monolayer,
        the coordinates of the array, corresponding to relative pressures,
        units [moles / gram]

    Returns
    _______
    theta : array
        array of computed theta values, the coordinates of the array
        corresponding to relative pressures

    """
    n = np.zeros((len(df), len(df)))
    theta = np.zeros((len(df), len(df)))
    for i in range(len(df)):
        for j in range(len(df)):
            if i > j:
                n[i, j] = util.median_ignore0(df.n[j:i + 1])

    theta = np.divide(n, nm, out=np.zeros_like(n), where=nm != 0)
    return theta


# checks that n(p-po) is increasing over BET interval
# sloppy in that it creates a mask for the whole array
# but works because of how sa array has zeros when j>=i
def check_1(df):
    """Checks that n(p-po) aka check1 is increasing over the relative pressure
    range used in BET analysis. This is a necessary condition for linearity of
    the BET dataset.

    Parameters
    __________
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    Returns
    _______
    mask : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges
        where n(p-po) isn't consistently increasing with relative pressure

    """
    mask1 = np.ones((len(df), len(df)))
    minus1 = np.concatenate(([0], df.check1[: -1]))
    test = (df.check1 - minus1 >= 0)
    test = np.tile(test, (len(df), 1))
    mask1 = mask1 * test
    mask1 = mask1.T

    if np.any(mask1) is False:
        print('All relative pressure ranges fail check 1.')

    return mask1


# checks that y int from bet plot is positive
def check_2(lin_reg):
    """Checks that y intercept of the BET plot's fit line is positive.

    Parameters
    __________
    lin_reg : array
        3D array of linear regression data where [i, j, 1] contains
        y-intercept values

    Returns
    _______
    mask : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges
        where the y-intercept is negative or zero
    """

    mask2 = (lin_reg[:, :, 1] > 0)

    if np.any(mask2) is False:
        print('All relative pressure ranges fail check 2.')

    return mask2


# checks that nm is in range of experimental n values used in BET
def check_3(df, nm):
    """Checks that nm, amount adsorbed in the monolayer, is in the range of
    data points used in BET analysis

    Parameters
    __________
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    nm : array
        2D array of BET specific amount of adsorbate in the monolayer, the
        coordinates of the array corresponding to relative pressures, units
        [moles / gram].

    Returns
    _______
    mask : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges nm
        is not included in the range of experimental n values
    """
    mask3 = np.zeros((len(df), len(df)))

    for i in range(np.shape(mask3)[0]):
        for j in range(np.shape(mask3)[1]):
            if df.iloc[j, 1] <= nm[i, j] <= df.iloc[i, 1]:
                mask3[i, j] = 1

    if np.any(mask3) is False:
        print('All relative pressure ranges fail check 3.')

    return mask3


# checks that relp at nm and relp found from setting n = nm in BET eq agree
# sloppy in the same way as mask1
def check_4(df, lin_reg, nm):
    """Checks that relative pressure is consistent.
    The relative pressure corresponding to nm is found from linear
    interpolation of the experiemental data. A second relative pressure is
    found by setting n to nm in the BET equation and solving for relative
    pressure. The two relative pressures are compared and must agree within 10%
    to pass this check.

    Parameters
    __________
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    lin_reg : array
        3D array of linear regression data where [i, j, 1] contains
        y-intercept values

    nm : array
        2D array of BET specific amount of adsorbate in the monolayer,
        the coordinates of the array corresponding to relative pressures,
        units [moles / gram]

    Returns
    _______
    mask : array
        array of 1s and 0s where 0 corresponds to relative pressure values that
        do not agree within 10%
    """
    mask4 = np.zeros((len(df), len(df)))

    for i in range(np.shape(mask4)[0]):
        for j in range(np.shape(mask4)[1]):
            if nm[i, j] != 0 and i > 0 and j > 0:
                relpm = util.lin_interp(df, nm[i, j])
                coeff = [-1 * lin_reg[i, j, 0] * nm[i, j], lin_reg[i, j, 0]
                         * nm[i, j] - 1 - lin_reg[i, j, 1] * nm[i, j],
                         lin_reg[i, j, 1] * nm[i, j]]
                roots = np.roots(coeff)  # note: some roots are imaginary
                roots = [item.real for item in roots if len(roots) == 2]
                if len(roots) == 2:
                    relp_m = roots[1]
                    if relpm == 0:
                        diff = 1
                    else:
                        diff = abs((relp_m - relpm) / relpm)
                    if diff < .1:
                        mask4[i, j] = 1

    if np.any(mask4) is False:
        print('All relative pressure ranges fail check 4.')

    return mask4


# check that range of values used in BET contain certain number of datapoints
def check_5(df, points=5):
    """Checks that relative pressure ranges contain a minium number of data
        points.

    Parameters
    __________
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    points : int
        minimum number of data points required for BET analysis to be
        considered valid default value is 5

    Returns
    _______
    mask : array
        array of 1s and 0s where 0 corresponds to ranges of experimental data
        that contain less than the minimum number of points
    """
    mask5 = np.ones((len(df), len(df)))

    for i in range(len(df)):
        for j in range(len(df)):
            if i - j < points - 1:
                mask5[i, j] = 0

    if np.any(mask5) is False:
        print('All relative pressure ranges fail check 5.')

    return mask5


def combine_masks(df, linreg, nm, check1=True, check2=True, check3=True,
                  check4=True, check5=True, points=5):
    """Calls all check functions and combines their masks into one "combomask".

    Parameters
    __________
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    lin_reg : array
        3D array of linear regression data where [i, j, 1] contains
        y-intercept values

    nm : array
        2D array of BET specific amount of adsorbate in the monolayer,
        the coordinates of the array corresponding to relative pressures,
        units [moles / gram]

    Returns
    _______
    mask : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges that
        fail one or more checks
    """

    if check1 is True:
        mask1 = check_1(df)
    else:
        mask1 = np.ones((len(df), len(df)))

    if check2 is True:
        mask2 = check_2(linreg)
    else:
        mask2 = np.ones((len(df), len(df)))

    if check3 is True:
        mask3 = check_3(df, nm)
    else:
        mask3 = np.ones((len(df), len(df)))

    if check4 is True:
        mask4 = check_4(df, linreg, nm)
    else:
        mask4 = np.ones((len(df), len(df)))

    if check5 is True:
        mask5 = check_5(df, points)
    else:
        mask5 = np.ones((len(df), len(df)))

    mask = np.multiply(mask1, mask2)
    mask = np.multiply(mask3, mask)
    mask = np.multiply(mask4, mask)
    mask = np.multiply(mask5, mask)

    if np.any(mask) is False:
        print('All relative pressure ranges fail the selected checks.')

    mask.astype(bool)  # converting mask to boolean
    invertedmask = np.logical_not(mask)  # inverting mask so that 0 = valid, 
    # 1 = invlad, to work well with numpy masks
    return invertedmask
