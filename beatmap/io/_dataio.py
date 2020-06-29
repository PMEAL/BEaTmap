#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 13:00:16 2019

@author: ellsworthbell
"""
import numpy as np
import pandas as pd
import scipy as sp
import beatmap.core as bet
from collections import namedtuple


def import_data():
    """Imports isothermal adsoprtion data from a csv file.

    The .csv file format expected is a two column table,
    the first column being "n" (specific amount adsorbed, mol/g)
    and the second being the relative pressure.

    Parameters
    ----------

    Returns
    -------
    isotherm_data : namedtuple
        Contains all information required for BET analysis.
        Relevant fields are:

        - ``isotherm_data.iso_data`` (dataframe) : imported isotherm data.
        - ``isotherm_data.a_o`` (float) : adsorbate cross sectional area.
        - ``isotherm_data.info`` (string) : string of adsorbate-adsorbent info.
        - ``isotherm_data.file`` (string) : file name or path.
    """

    file = input("Enter file name/path:")
    info = input("Enter adsorbate-adsorbent information (this will be \
incorporated into file names):")
    a_o_input = input("Enter cross sectional area of adsorbate in \
square Angstrom:")

    try:
        a_o = float(a_o_input)
    except ValueError:
        print('The ao provided is not numeric.')
        a_o_input = input("Try again, enter the cross sectional area of \
adsorbate in square Angstrom: ")
        a_o = float(a_o_input)

    print('\nAdsorbate used has an adsorbed cross sectional area of \
%.2f sq. Angstrom.' % (a_o))

    # importing data and creating 'bet' and 'check2' data points
    try:
        data = pd.read_csv(file)
    except FileNotFoundError:
        print('File not found.')
        file = input("Try again, entering the file name/path:")
        data = pd.read_csv(file)

    labels = list(data)
    data.rename(columns={labels[0]: 'relp', labels[1]: 'n'}, inplace=True)
    data['n'] = data.n  # necessary? why that here?
    data['bet'] = (1 / data.n) * (data.relp / (1-data.relp))

    # checking data quality
    test = np.zeros(len(data))
    minus1 = np.concatenate(([0], data.n[: -1]))
    test = data.n - minus1
    test_sum = sum(x < 0 for x in test)
    if test_sum > 0:
        print("""\nIsotherm data is suspect.
Adsorbed moles do not consistantly increase as relative pressure increases""")
    else:
        print("""\nIsotherm data quality appears good.
Adsorbed molar amounts are increasing as relative pressure increases.""")

    # checking isotherm type
    x = data.relp.values
    y = data.n.values

    dist = np.sqrt((x[:-1] - x[1:])**2 + (y[:-1] - y[1:])**2)
    dist_along = np.concatenate(([0], dist.cumsum()))

    # build a spline representation of the contour
    spline, u = sp.interpolate.splprep([x, y], u=dist_along,
                                       w=np.multiply(1, np.ones(len(x))),
                                       s=.0000000001)
    interp_d = np.linspace(dist_along[0], dist_along[-1], 50)
    interp_x, interp_y = sp.interpolate.splev(interp_d, spline)

    # take derivative of the spline (to find inflection points)
    spline_1deriv = np.diff(interp_y)/np.diff(interp_x)
    spline_2deriv = np.diff(spline_1deriv)/np.diff(interp_x[1:])

    zero_crossings = np.where(np.diff(np.sign(spline_2deriv)))[0]

    if len(zero_crossings) == 0 and np.sign(spline_2deriv[0]) == -1:
        print('Isotherm is type I.')
    elif len(zero_crossings) == 0 and np.sign(spline_2deriv[0]) == 1:
        print('Isotherm is type III.')
    elif len(zero_crossings) == 1 and np.sign(spline_2deriv[0]) == -1:
        print('Isotherm is type II.')
    elif len(zero_crossings) == 1 and np.sign(spline_2deriv[0]) == 1:
        print('Isotherm is type V.')
    elif len(zero_crossings) == 2 and np.sign(spline_2deriv[0]) == -1:
        print('Isotherm is type IV.')
    else:
        print('Isotherm is type VI.')

    iso_data = namedtuple('iso_data', 'iso_df a_o info file')
    isotherm_data = iso_data(data, a_o, info, file)

    return isotherm_data


def import_list_data(relp, n):
    """Imports isothermal adsoprtion data.

    User provides two lists, one of relative pressures and the other of amount
    adsorbed with units of [mol/g].

    Parameters
    ----------
    relp : list
        Experimental isotherm relative pressure values.

    n : list
        Experimental amount adsorbed values, mols per gram.

    Returns
    -------
    isotherm_data : namedtuple
        Contains all information required for BET analysis.
        Relevant fields are:

        - ``isotherm_data.iso_data`` (dataframe) : imported isotherm data.
        - ``isotherm_data.a_o`` (float) : adsorbate cross sectional area.
        - ``isotherm_data.info`` (string) : string of adsorbate-adsorbent info.
        - ``isotherm_data.file`` (string) : file name or path.
    """

    file = input("Enter name for dataset:")
    info = input("Enter name of adsorbate used:")
    a_o_input = input("Enter cross sectional area of adsorbate in \
square Angstrom:")

    try:
        a_o = float(a_o_input)
    except ValueError:
        print('The ao provided is not numeric.')
        a_o_input = input("Try again, enter the cross sectional area of \
adsorbate in square Angstrom:")
        a_o = float(a_o_input)

    print('\nAdsorbate used has an adsorbed cross sectional area of \
%.2f sq. Angstrom.' % (a_o))

    # importing data and creating 'bet' and 'check2' data points
    dict_from_lists = {'relp': relp, 'n': n}
    data = pd.DataFrame(dict_from_lists)
    data['bet'] = (1 / data.n) * (data.relp / (1-data.relp))
    data['check2'] = data.n * (1 - data.relp)

    # checking data quality
    test = np.zeros(len(data))
    minus1 = np.concatenate(([0], data.n[: -1]))
    test = data.n - minus1
    test_sum = sum(x < 0 for x in test)
    if test_sum > 0:
        print("""\nIsotherm data is suspect.
Adsorbed moles do not consistantly increase as relative pressure increases""")
    else:
        print("""\nIsotherm data quality appears good.
Adsorbed molar amounts are increasing as relative pressure increases.""")

    # checking isotherm type
    x = data.relp.values
    y = data.n.values

    dist = np.sqrt((x[:-1] - x[1:])**2 + (y[:-1] - y[1:])**2)
    dist_along = np.concatenate(([0], dist.cumsum()))

    # build a spline representation of the contour
    spline, u = sp.interpolate.splprep([x, y], u=dist_along,
                                       w=np.multiply(1, np.ones(len(x))),
                                       s=.0000000001)
    interp_d = np.linspace(dist_along[0], dist_along[-1], 50)  # len(x)
    interp_x, interp_y = sp.interpolate.splev(interp_d, spline)

    # take derivative of the spline (to find inflection points)
    spline_1deriv = np.diff(interp_y)/np.diff(interp_x)
    spline_2deriv = np.diff(spline_1deriv)/np.diff(interp_x[1:])

    zero_crossings = np.where(np.diff(np.sign(spline_2deriv)))[0]

    if len(zero_crossings) == 0 and np.sign(spline_2deriv[0]) == -1:
        print('Isotherm is type I.')
    elif len(zero_crossings) == 0 and np.sign(spline_2deriv[0]) == 1:
        print('Isotherm is type III.')
    elif len(zero_crossings) == 1 and np.sign(spline_2deriv[0]) == -1:
        print('Isotherm is type II.')
    elif len(zero_crossings) == 1 and np.sign(spline_2deriv[0]) == 1:
        print('Isotherm is type V.')
    elif len(zero_crossings) == 2 and np.sign(spline_2deriv[0]) == -1:
        print('Isotherm is type IV.')
    else:
        print('Isotherm is type VI.')

    iso_data = namedtuple('iso_data', 'iso_df a_o info file')
    isotherm_data = iso_data(data, a_o, info, file)

    return isotherm_data


def export_raw_data(isotherm_data):
    """Exports isothermal adsoprtion data.

    Exported data is saved as a .csv file in the parent directory.

    Parameters
    ----------

    isotherm_data : namedtuple
        Contains all information required for BET analysis.
        Relevant fields are:

        - ``isotherm_data.iso_df`` (dataframe) : of the raw isotherm data
        written to a .csv
        - ``bet_results.info`` (string) : adsorbate-adsorbent information used

    Returns
    -------

    """

    export_file_name = isotherm_data.info + 'raw_data_export.csv'
    df = isotherm_data.iso_df
    df.to_csv(export_file_name, index=None, header=True)
    print('Raw data saved as: %s' % (export_file_name))
    return


def export_processed_data(bet_results, points=5):
    """Exports processed isothermal adsoprtion data.

    Exported data is saved as a .csv file in the parent directory.

    Parameters
    ----------

    bet_results : namedtuple
        Contains all information required for BET analysis.
        Relevant fields are:

    points : int
        The minimum number of experimental data points for a relative pressure
        interval to be considered valid. Default is 5.

    Returns
    -------

    """

    df = bet_results.iso_df
    i = 0
    end_relp = np.zeros((len(df), len(df)))
    while i < len(df):
        end_relp[i:] = df.relp[i]
        i += 1

    begin_relp = np.transpose(end_relp)

    mask1 = bet.check_1(bet_results.intercept)
    mask2 = bet.check_2(df)
    mask3 = bet.check_3(df, bet_results.nm)
    mask4 = bet.check_4(df, bet_results.nm, bet_results.slope,
                        bet_results.intercept)
    mask5 = bet.check_5(df, points)

    processed_data = np.column_stack((begin_relp.flatten(),
                                      end_relp.flatten()))
    processed_data = np.column_stack((processed_data,
                                      bet_results.ssa.flatten()))
    processed_data = np.column_stack((processed_data,
                                      bet_results.nm.flatten()))
    processed_data = np.column_stack((processed_data,
                                      bet_results.c.flatten()))
    processed_data = np.column_stack((processed_data,
                                      bet_results.err.flatten()))
    processed_data = np.column_stack((processed_data,
                                      bet_results.slope.flatten()))
    processed_data = np.column_stack((processed_data,
                                      bet_results.intercept.flatten()))
    processed_data = np.column_stack((processed_data,
                                      bet_results.r.flatten()))
    processed_data = np.column_stack((processed_data, mask1.flatten()))
    processed_data = np.column_stack((processed_data, mask2.flatten()))
    processed_data = np.column_stack((processed_data, mask3.flatten()))
    processed_data = np.column_stack((processed_data, mask4.flatten()))
    processed_data = np.column_stack((processed_data, mask5.flatten()))

    processed_data = pd.DataFrame(data=processed_data,
                                  columns=['begin relative pressure',
                                           'end relative pressure',
                                           'spec sa [m2/g]', 'bet constant',
                                           'nm [mol/g]', 'error', 'slope',
                                           'y-int', 'r value', 'check2',
                                           'check2', 'check3', 'check4',
                                           'check5'])

    export_file_name = bet_results.info + 'processed_data_export.csv'
    processed_data.to_csv(export_file_name, index=None, header=True)
    print('Processed data saved as: %s' % (export_file_name))
    return


def run_beatmap_import_data(file, info, a_o):
    """Import function for the run_beatmap function.

    The .csv file format expected is a two column table,
    the first column being "n" (specific amount adsorbed, mol/g)
    and the second being the relative pressure.

    Parameters
    ----------
    a_o : float
        Adsorbate cross sectional area.
    info : string
        String of adsorbate-adsorbent info, used for file naming.
    file : String
        File name or path. It is recommended to store .csv files in the parent
        directory and use relative import by providing the file name.
        eg 'mydata.csv'

    Returns
    -------
    isotherm_data : namedtuple
        Contains all information required for BET analysis.
        Relevant fields are:

        - ``isotherm_data.iso_data`` (dataframe) : imported isotherm data.
        - ``isotherm_data.a_o`` (float) : adsorbate cross sectional area.
        - ``isotherm_data.info`` (string) : string of adsorbate-adsorbent info.
        - ``isotherm_data.file`` (string) : file name or path.
    """

    print('\nAdsorbate used has an adsorbed cross sectional area of \
%.2f sq. Angstrom.' % (a_o))

    # importing data and creating 'bet' and 'check2' data points
    try:
        data = pd.read_csv(file)
    except FileNotFoundError:
        print('File not found.')
        file = input("Try again, entering the file name/path:")
        data = pd.read_csv(file)

    labels = list(data)
    data.rename(columns={labels[0]: 'relp', labels[1]: 'n'}, inplace=True)
    data['n'] = data.n  # necessary? why that here?
    data['bet'] = (1 / data.n) * (data.relp / (1-data.relp))

    # checking data quality
    test = np.zeros(len(data))
    minus1 = np.concatenate(([0], data.n[: -1]))
    test = data.n - minus1
    test_sum = sum(x < 0 for x in test)
    if test_sum > 0:
        print("""\nIsotherm data is suspect.
Adsorbed moles do not consistantly increase as relative pressure increases""")
    else:
        print("""\nIsotherm data quality appears good.
Adsorbed molar amounts are increasing as relative pressure increases.""")

    # checking isotherm type
    x = data.relp.values
    y = data.n.values

    dist = np.sqrt((x[:-1] - x[1:])**2 + (y[:-1] - y[1:])**2)
    dist_along = np.concatenate(([0], dist.cumsum()))

    # build a spline representation of the contour
    spline, u = sp.interpolate.splprep([x, y], u=dist_along,
                                       w=np.multiply(1, np.ones(len(x))),
                                       s=.0000000001)
    interp_d = np.linspace(dist_along[0], dist_along[-1], 50)
    interp_x, interp_y = sp.interpolate.splev(interp_d, spline)

    # take derivative of the spline (to find inflection points)
    spline_1deriv = np.diff(interp_y)/np.diff(interp_x)
    spline_2deriv = np.diff(spline_1deriv)/np.diff(interp_x[1:])

    zero_crossings = np.where(np.diff(np.sign(spline_2deriv)))[0]

    if len(zero_crossings) == 0 and np.sign(spline_2deriv[0]) == -1:
        print('Isotherm is type I.')
    elif len(zero_crossings) == 0 and np.sign(spline_2deriv[0]) == 1:
        print('Isotherm is type III.')
    elif len(zero_crossings) == 1 and np.sign(spline_2deriv[0]) == -1:
        print('Isotherm is type II.')
    elif len(zero_crossings) == 1 and np.sign(spline_2deriv[0]) == 1:
        print('Isotherm is type V.')
    elif len(zero_crossings) == 2 and np.sign(spline_2deriv[0]) == -1:
        print('Isotherm is type IV.')
    else:
        print('Isotherm is type VI.')

    iso_data = namedtuple('iso_data', 'iso_df a_o info file')
    isotherm_data = iso_data(data, a_o, info, file)

    return isotherm_data
