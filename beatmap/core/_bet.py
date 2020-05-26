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


def bet(bet_results):
    """Performs BET analysis on isotherm data for all relative pressure ranges.

    This function performs BET analysis of any relative pressure range where
    the starting relative pressure is less than the ending relative pressure.

    Results of the analysis are written to arrays, the indexes of the arrays
    correspond to the starting and ending relative pressure.

    eg the specific surface area value with the indicies [3,9] is the specific
    surface area for the relative pressure range that begins with the 4th data
    point and ends with the 10th.

    Arrays of results are stored in the bet_results named tuple.

    Parameters
    ----------
    bet_results : namedtuple
        Contains all information required for BET analysis. Results of BET
        analysis are also stored in this named tuple. Relevant fields for BET
        anaylsis are:

        - ``bet_results.raw_data`` (dataframe) : experimental isotherm data.

        - ``bet_results.a_o`` (flaot) : the cross sectional area of the
        adsorbate molecule, in square angstrom.


    Returns
    -------
    bet_results : namedtuple
        Contains the results of BET analysis.
        Relevant fields are:

            - ``bet_results.ssa`` (array) : 2D array of specific surface area
            values, in m^2/g, indicies correspond to first and last datapoint
            used in the analysis.

            - ``bet_results.c`` (array) : 2D array of BET constants values,
            indicies correspond to first and last datapoint used in the
            analysis.

            - ``bet_results.nm`` (array) : 2D array of monolayer adsorbed
            amounts, in mol/g, indicies correspond to first and last datapoint
            used in the analysis.

            - ``bet_results.err`` (array) : 2D array of average error between
            a datapoint and the theoretical BET isotherm. Indicies correspond
            to first and last datapoint used in the analysis.

            - ``bet_results.slope`` (array) : 2D array of slope values for the
            BET plot trendline. Indicies correspond to first and last datapoint
            used in the analysis.

            - ``bet_results.intercept`` (array) : 2D array of intercept values
            for the BET plot trendline. Indicies correspond to first and last
            datapoint used in the analysis.

            - ``bet_results.r`` (array) : 2D array of r values for the BET plot
            trendline. Indicies correspond to first and last datapoint used in
            the analysis.

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
    number_pts = np.zeros((len(df.relp), len(df.relp)))

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
                spec_sa = nm * 6.022*10**23 * a_o * 10**-20
                ssa_array[i, j] = spec_sa
                c_array[i, j] = c
                nm_array[i, j] = nm
                number_pts[i, j] = i - j + 1
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
                bet_results.number_pts = number_pts

    return bet_results


def single_point_bet(df, a_o):
    """Performs single point BET analysis on an isotherm data set for all
    relative pressure ranges. Can be used to check for agreement between BET
    and single point BET.

    Parameters
    ----------
    bet_results : namedtuple
        Contains all information required for BET analysis. Results of BET
        analysis are also stored in this named tuple.
        Relevant fields for single point BET anaylsis are:

        - ``bet_results.raw_data`` (dataframe) : experimental isotherm data.

        - ``bet_results.a_o`` (flaot) : the cross sectional area of the
        adsorbate molecule, in square angstrom.

    Returns
    -------
    singlept_results : namedtuple
        Contains the results of single point BET analysis. Relevant fields are:

            - ``singlept_results.ssa`` (array) : 2D array of specific surface
            area values, in m^2/g, indicies correspond to first and last
            datapoint used in the analysis.

            - ``singlept_results.nm`` (array) : 2D array of monolayer adsorbed
            amounts, in mol/g, indicies correspond to first and last datapoint
            used in the analysis.

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
                ssa_array[i, j] = n * 6.022 * 10**23 * a_o * 10**-20

    singlept_results = namedtuple('singlept_results', ('ssa', 'nm'))
    singlept_results.ssa = ssa_array
    singlept_results.nm = nm_array

    return singlept_results


def check_1(df):
    """Checks that n(p-po) aka check1 is increasing.

    This is a necessary condition for linearity of the BET dataset.

    Parameters
    ----------
    df : dataframe
        dataframe of imported experimental isothermal adsorption data.

    Returns
    -------
    check1 : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges
        where n(p-po) isn't consistently increasing with relative pressure, ie
        ranges that fail this check.

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
    """Checks that y intercept of the BET plot's linear regression is positive.

    Parameters
    ----------
    intercept : array
        2D array of y-intercept values.

    Returns
    -------
    check2 : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges
        where the y-intercept is negative or zero, ie ranges that fail this
        check.

    """

    check2 = (intercept[:, :] > 0)

    if np.any(check2) is False:
        print('All relative pressure ranges fail check 2.')

    return check2


def check_3(df, nm):
    """Checks that nm, amount adsorbed in the monolayer, is in the range of
    data points used in BET analysis.

    Parameters
    ----------
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    nm : array
        2D array of BET specific amount of adsorbate in the monolayer, the
        coordinates of the array corresponding to relative pressures, units
        [moles / gram].

    Returns
    -------
    check3 : array
        array of 1s and 0s where 0 corresponds to relative pressure ranges nm
        is not included in the range of experimental n values, ie ranges that
        fail this check.

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

    A second relative pressure is found by setting n to nm in the BET equation
    and solving for relative pressure.

    The two relative pressures are compared and must agree within 10% to pass
    this check.

    Parameters
    ----------
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    nm : array
        2D array of BET specific amount of adsorbate in the monolayer,
        the coordinates of the array corresponding to relative pressures,
        units [moles / gram]

    slope : array
        2D array of slope values resulting from linear regression applied to
        relevant experimental data

    intercept : array
        2D array of y-intercept values resulting from linear regression applied
        to relevant experimental data

    Returns
    -------
    check4 : array
        array of 1s and 0s where 0 corresponds to relative pressure values that
        do not agree within 10%, ie ranges that fail this check

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
    ----------
    df : dataframe
        dataframe of imported experimental isothermal adsorption data

    points : int
        minimum number of data points required for BET analysis to be
        considered valid default value is 5

    Returns
    -------
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
    ----------
    bet_results : namedtuple
        Contains all the necessary arrays to be passed to check 1-5.

    check1 : boolean
        True means the will be evalued, False means the check will not be
        evaluated.

    check2 : boolean
        True means the will be evalued, False means the check will not be
        evaluated.

    check3 : boolean
        True means the will be evalued, False means the check will not be
        evaluated.

    check4 : boolean
        True means the will be evalued, False means the check will not be
        evaluated.

    check5 : boolean
        True means the will be evalued, False means the check will not be
        evaluated.

    points : int
        The minimum number of experimental data points for a relative pressure
        interval to be considered valid.

    Returns
    -------
    rouq_mask : namedtuple
        Contains arrays for the result of each check and a masked array that is
        the result of all selected checks.
        Fields of the named tuple are:

        -``rouq_mask.mask`` (MaskedArray) : object where invalid BET results
        are masked.

        -``rouq_mask.check1 (array) : array of 1s and 0s where 0 corresponds
        failing check1
        -``rouq_mask.check2 (array) : array of 1s and 0s where 0 corresponds
        failing check2
        -``rouq_mask.check3 (array) : array of 1s and 0s where 0 corresponds
        failing check3
        -``rouq_mask.check4 (array) : array of 1s and 0s where 0 corresponds
        failing check4
        -``rouq_mask.check5 (array) : array of 1s and 0s where 0 corresponds
        failing check5

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
        check4 = check_4(df, bet_results.nm, bet_results.slope,
                         bet_results.intercept)
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

    rouq_mask = namedtuple('rouq_mask', ('mask', 'check1', 'check2', 'check3',
                                         'check4', 'check5'))
    rouq_mask.mask = invertedmask
    rouq_mask.check1 = check1
    rouq_mask.check2 = check2
    rouq_mask.check3 = check3
    rouq_mask.check4 = check4
    rouq_mask.check5 = check5

    return rouq_mask


def ssa_answer(bet_results, rouq_mask, criterion='error'):
    """ Prints a single specific surface area answer from the valid relative
    pressure range with either the lowest error or most number of points.

    Parameters
    ----------
    bet_results : named tuple
        ``bet_results.ssa`` contains the array of specific surface values.

    rouq_mask : named tuple
        ``rouq_mask.mask`` contains the mask used to remove invaid specific
        surface area values from consideration.

    criterion : string
        Used to specify the criterion for a final specific surface area answer,
        either 'error' or 'points'. Defaults to 'error'.

    Returns
    -------

    """

    mask = rouq_mask.mask
    ssa = np.ma.array(bet_results.ssa, mask=mask)

    if criterion == 'error':
        err = np.ma.array(bet_results.err, mask=mask)
        errormax, error_max_idx, errormin, error_min_idx = util.max_min(err)
        ssa_ans = ssa[int(error_min_idx[0]), int(error_min_idx[1])]
        print('The specific surface area value, based on %s is %.2f m2/g.' %
              (criterion, ssa_ans))
        return

    if criterion == 'points':
        pts = np.ma.array(bet_results.number_pts, mask=mask)
        max_pts = np.max(pts)
        ssa_ans_array = np.ma.masked_where(pts < max_pts, ssa)
        try:
            ssa_ans = float(ssa_ans_array.compressed())
        except:
            print('Error, so single specific surface area answer. Multiple\
relative pressure ranges with the maximum number of points.')
            return 0
        print('The specific surface area value, based on %s is %.2f m2/g.' %
              (criterion, ssa_ans))
        return ssa_ans
