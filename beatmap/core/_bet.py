#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:05:19 2019

@author: ellsworthbell
"""

import numpy as np
import scipy as sp
import beatmap.utils as util
from collections import namedtuple

avagadro = 6.022*10**23


def bet(bet_results):
    """Performs BET analysis on an isotherm data set for all relative pressure
        ranges.
    This is the meat and potatoes of the whole package.

    Parameters
    ----------
    bet_results : namedtuple
        namedtuple containing all information required for BET analysis,
        

    Returns
    -------
    bet_results : namedtuple
        namedtuple, the following elements contain BET results: ssa, nm, c, err, slope, intercept, r
        the elements are 2D arrays where each cell represents the results for a partiular relative pressure interval
        ssa is the specific suraface area in m^2/g 
        nm is the monolayer amount in mol/g 
        c is the bet constant 
        err is the average percent error bewteen an experimental data point and the theoretical value
        slope results from applying linear regression to the experimental data
        intercept is the y-intercept that results from applying linear regression to the experimental data
        r is the r value that results from applying linear regression to the experimental data
    """
    
    df = bet_results.raw_data
    a_o = bet_results.a_o
    
    ssa_array = np.zeros((len(df), len(df)))
    c_array = np.zeros((len(df), len(df)))
    nm_array = np.zeros((len(df), len(df)))
    err_array = np.zeros((len(df), len(df)))
    slope = np.zeros((len(df), len(df)))
    intercept = np.zeros((len(df), len(df)))
    r = np.zeros((len(df), len(df)))
    bet_c = np.zeros(len(df.relp))

    for i in range(len(df)):
        for j in range(len(df)):
            if i > j:
                a = df.iloc[j:i+1]
                X = a.relp
                y = a.bet
                m, b, r_value, p_value, std_err =\
                    sp.stats.linregress(X, y)
                slope[i, j] = m
                intercept[i, j] = b
                r[i, j] = r_value 
                c = 0
                nm = 0
                bet_c = 0
                if b != 0:
                    c = m/b + 1  # avoiding divide by zero issues
                    nm = 1 / (b * c)
                    bet_c = (1 / (nm * c)) + (c - 1) * df.relp / (nm * c)
                spec_sa = nm * avagadro * a_o * 10**-20
                ssa_array[i, j] = spec_sa
                c_array[i, j] = c
                nm_array[i, j] = nm
                errors = np.nan_to_num(abs(bet_c - df.bet) / bet_c)
                if i - j == 1:
                    err_array[i, j] = 0
                else:
                    err_array[i, j] = 100 * sum(errors[j:i + 1]) / (i + 1 - j)
                # error is normalized for the interval of relative pressures
                # used to compute C, so, min and max error corresponds to the
                # best and worst fit over the interval used in BET analysis,
                # not the entire isotherm

                bet_results.ssa = ssa_array
                bet_results.nm = nm_array
                bet_results.c = c_array
                bet_results.err = err_array
                bet_results.slope = np.nan_to_num(slope)
                bet_results.intercept = np.nan_to_num(intercept)
                bet_results.r = r
                 
    return bet_results


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
    singlept_results : namedtuple
        namedtuple with the following elements: ssa, nm
        ssa is the specific suraface area in m^2/g 
        nm is the monolayer amount in mol/g 
        
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

    singlept_results = namedtuple('singlept_results', ('ssa', 'nm'))
    singlept_results.ssa = ssa_array
    singlept_results.nm = nm_array
    
    return singlept_results


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


def check_2(intercept):
    """Checks that y intercept of the BET plot's fit line is positive.

    Parameters
    __________
    intercept : array
        2D array of y-intercept values

    Returns
    _______
    check2 : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges
        where the y-intercept is negative or zero
    """

    check2 = (intercept[:, :] > 0)

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


def check_4(df, nm, slope, intercept):
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

    nm : array
        2D array of BET specific amount of adsorbate in the monolayer,
        the coordinates of the array corresponding to relative pressures,
        units [moles / gram]
 
    slope : array
        2D array of slope values resulting from linear regression applied to relevant experimental data

    intercept : array
        2D array of y-intercept values resulting from linear regression applied to relevant experimental data
    
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
                coeff = [-1 * slope[i, j] * nm[i, j], slope[i, j]
                         * nm[i, j] - 1 - intercept[i, j] * nm[i, j],
                         intercept[i, j] * nm[i, j]]
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


def rouq_mask(bet_results, check1=True, check2=True, check3=True,
              check4=True, check5=True, points=5):
    """Calls all check functions and combines their masks
    into one "rouqerol mask".

    Parameters
    __________

    bet_results : namedtuple
        bet_results is the named tuple returned from the bet function, containing all data
        required to check the validity of BET theory over all relative pressure intervals

    check1 : boolean
        True means the will be evalued, False means the check will not be evaluated

    check2 : boolean
        True means the will be evalued, False means the check will not be evaluated

    check3 : boolean
        True means the will be evalued, False means the check will not be evaluated

    check4 : boolean
        True means the will be evalued, False means the check will not be evaluated

    check5 : boolean
        True means the will be evalued, False means the check will not be evaluated

    points : int
        the minimum number of experimental data points for a relative pressure interval to be considered valid
    
    Returns
    _______
    rouq_mask : namedtuple
        namedtuple with fields containing arrays for the result of each check
        in addition to the rouq_mask.mask field which contains the mask of invalid relative pressure ranges
    """
    
    df = bet_results.raw_data
    
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
        check2 = check_2(bet_results.intercept)
    else:
        check2 = np.ones((len(df), len(df)))

    if check3 is True:
        check3 = check_3(df, bet_results.nm)
    else:
        check3 = np.ones((len(df), len(df)))

    if check4 is True:
        check4 = check_4(df, bet_results.nm, bet_results.slope, bet_results.intercept)
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

    mask.astype(bool)  # converting mask to boolean
    invertedmask = np.logical_not(mask)  # inverting mask so that 0 = valid,
    # 1 = invalid, to work well with numpy masks
    
    rouq_mask = namedtuple('rouq_mask', ('mask', 'check1', 'check2', 'check3', 'check4', 'check5'))
    rouq_mask.mask = invertedmask
    rouq_mask.check1 = check1
    rouq_mask.check2 = check2
    rouq_mask.check3 = check3
    rouq_mask.check4 = check4
    rouq_mask.check5 = check5
    
    return rouq_mask
