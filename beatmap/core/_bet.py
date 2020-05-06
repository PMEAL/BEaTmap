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


"""
from collections import namedtuple
profile = namedtuple('profile', ('volume', 'porosity'))
profile.volume = volume
profile.porosity = porosity
return profile
"""

def bet(df, a_o):
    """Performs BET analysis on an isotherm data set for all relative pressure
        ranges.
    This is the meat and potatoes of the whole package.

    Parameters
    ----------
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    a_o : float
        adsorbate cross section area, units must be [square angstrom]

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
        3D array, x by y by 3 with the x and y corrdinates corresponding to
        relative pressure this array is available for reference and BET theory
        checks
    """

    ssa_array = np.zeros((len(df), len(df)))
    c_array = np.zeros((len(df), len(df)))
    nm_array = np.zeros((len(df), len(df)))
    err_array = np.zeros((len(df), len(df)))
    lin_reg = np.zeros((len(df), len(df), 3))
    bet_c = np.zeros(len(df.relp))

    for i in range(len(df)):
        for j in range(len(df)):
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
                ssa_array[i, j] = spec_sa
                c_array[i, j] = c
                nm_array[i, j] = nm
                errors = np.nan_to_num(abs(bet_c - df.bet))
                if i - j == 1:
                    err_array[i, j] = 0
                else:
                    err_array[i, j] = sum(errors[j:i + 1]) / (i + 1 - j)
                # error is normalized for the interval of relative pressures
                # used to compute C, so, min and max error corresponds to the
                # best and worst fit over the interval used in BET analysis,
                # not the entire isotherm
    np.nan_to_num(lin_reg)
    return ssa_array, nm_array, c_array, err_array, lin_reg


def single_point_bet(df, a_o):
    """Performs single point BET analysis on an isotherm data set for all
    relative pressure ranges. Can be used to check for agreement between BET
    and single point BET.

    Parameters
    ----------
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    a_o : float
        adsorbate cross section area, units must be [square angstrom]

    Returns
    -------
    sa_array : array
        2D array of BET specific surface areas, the coordinates of the array
        corresponding to relative pressures, units [square meter / gram]

    nm_array : array
        2D array of BET specific amount of adsorbate in the monolayer, the
        coordinates of the array corresponding to relative pressures, units
        [moles / gram]
    """

    ssa_array = np.zeros((len(df), len(df)))
    nm_array = np.zeros((len(df), len(df)))

    for i in range(len(df)):
        for j in range(len(df)):
            if i > j:
                n_range = df.n[j:i]
                relp_range = df.relp[j:i]
                n = np.ma.median(n_range)
                relp = np.ma.median(relp_range)

                nm_array[i, j] = n * (1-relp)
                ssa_array[i, j] = n * avagadro * a_o * 10**-20

    return ssa_array, nm_array


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
    check1 : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges
        where n(p-po) isn't consistently increasing with relative pressure

    """
    check1 = np.ones((len(df), len(df)))
    minus1 = np.concatenate(([0], df.check1[: -1]))
    test = (df.check1 - minus1 >= 0)
    test = np.tile(test, (len(df), 1))
    check1 = check1 * test
    check1 = check1.T

    if np.any(check1) is False:
        print('All relative pressure ranges fail check 1.')

    return check1


def check_2(lin_reg):
    """Checks that y intercept of the BET plot's fit line is positive.

    Parameters
    __________
    lin_reg : array
        3D array of linear regression data where [i, j, 1] contains
        y-intercept values

    Returns
    _______
    check2 : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges
        where the y-intercept is negative or zero
    """

    check2 = (lin_reg[:, :, 1] > 0)

    if np.any(check2) is False:
        print('All relative pressure ranges fail check 2.')

    return check2


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
    check3 : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges nm
        is not included in the range of experimental n values
    """

    check3 = np.zeros((len(df), len(df)))

    for i in range(np.shape(check3)[0]):
        for j in range(np.shape(check3)[1]):
            if df.iloc[j, 1] <= nm[i, j] <= df.iloc[i, 1]:
                check3[i, j] = 1

    if np.any(check3) is False:
        print('All relative pressure ranges fail check 3.')

    return check3


def check_4(df, nm, lin_reg):
    """Checks that relative pressure is consistent.
    The relative pressure corresponding to nm is found from linear
    interpolation of the experiemental data.

    A second relative pressure is
    found by setting n to nm in the BET equation and solving for relative
    pressure.

    The two relative pressures are compared and must agree within 10% to pass
    this check.

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
    check4 : array
        array of 1s and 0s where 0 corresponds to relative pressure values that
        do not agree within 10%
    """
    check4 = np.zeros((len(df), len(df)))

    for i in range(np.shape(check4)[0]):
        for j in range(np.shape(check4)[1]):
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
                        check4[i, j] = 1

    if np.any(check4) is False:
        print('All relative pressure ranges fail check 4.')

    return check4


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
    check5 : array
        array of 1s and 0s where 0 corresponds to ranges of experimental data
        that contain less than the minimum number of points
    """
    check5 = np.ones((len(df), len(df)))

    for i in range(len(df)):
        for j in range(len(df)):
            if i - j < points - 1:
                check5[i, j] = 0

    if np.any(check5) is False:
        print('All relative pressure ranges fail check 5.')

    return check5


def rouq_mask(df, nm, linreg, check1=True, check2=True, check3=True,
              check4=True, check5=True, points=5):
    """Calls all check functions and combines their masks
    into one "rouqerol mask".

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
    invertedmask : numpy mask array
        array of 1s and 0s where 1 corresponds to relative pressure ranges that
        fail one or more checks
    """

    mask = np.ones((len(df), len(df)))
    for i in range(len(df)):
        for j in range(len(df)):
            if j >= i:
                mask[i, j] = 0

    if check1 is True:
        check1 = check_1(df)
    else:
        check1 = np.ones((len(df), len(df)))

    if check2 is True:
        check2 = check_2(linreg)
    else:
        check2 = np.ones((len(df), len(df)))

    if check3 is True:
        check3 = check_3(df, nm)
    else:
        check3 = np.ones((len(df), len(df)))

    if check4 is True:
        check4 = check_4(df, nm, linreg)
    else:
        check4 = np.ones((len(df), len(df)))

    if check5 is True:
        check5 = check_5(df, points)
    else:
        check5 = np.ones((len(df), len(df)))

    mask = np.multiply(check1, mask)
    mask = np.multiply(check2, mask)
    mask = np.multiply(check3, mask)
    mask = np.multiply(check4, mask)
    mask = np.multiply(check5, mask)

    if np.any(mask) == False:
        print('All relative pressure ranges fail the selected checks.')

    mask.astype(bool)  # converting mask to boolean
    invertedmask = np.logical_not(mask)  # inverting mask so that 0 = valid,
    # 1 = invalid, to work well with numpy masks
    return invertedmask
