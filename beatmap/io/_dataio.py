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
    """Imports isothermal adsoprtion data.

    The .csv file format expected is a two column table,
    the first column being "n" (specific adsorbed amount)
    and the second "relp" the relative pressure.

    requires n values with units of mol/g

    Parameters
    _________
    Returns
    _______
    file: string
        file name, used later to name saved files

    data : dataframe
        contains adsorption data and values computed from
        adsortion data, used later in the BET analysis

    adsorbate: string
        adsorbate name, for reference

    a_o: float
        cross sectional surface area of adsorbate in square angstrom
    """

    file = input("Enter file name/path:")
    info = input("Enter adsorbate-adsorbent information (this will be incorporated into file names):")
    a_o_input = input("Enter cross sectional area of adsorbate in \
square Angstrom:")

    try:
        a_o = float(a_o_input)
    except:
        print('The ao provided is not numeric.')
        a_o_input = input("Try again, enter the cross sectional area of \
adsorbate in square Angstrom: ")
        a_o = float(a_o_input)

    print('\nAdsorbate used has an adsorbed cross sectional area of \
%.2f sq. Angstrom.' % (a_o))

    # importing data and creating 'bet' and 'check1' data points
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
    data['check1'] = data.n * (1 - data.relp)

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
        
    bet_results = namedtuple('bet_results', ('file', 'info', 'a_o', 'raw_data', 'ssa', 'nm', 'c', 'err', 'slope', 'intercept', 'r'))
    bet_results.file = file
    bet_results.info = info
    bet_results.a_o = a_o
    bet_results.raw_data = data
    return bet_results


def import_list_data(relp, n):
    """Imports isothermal adsoprtion data.

    User provides two lists, one of relative pressures and the other of amount
    adsorbed with units of [mol/g].

    Parameters
    __________
    relp : list
        list of relative pressure values

    n : list
        list of amount adsorbed at each relative pressure stage, mols per gram

    Returns
    _______
    file: string
        file name, used later to name saved files

    data : dataframe
        contains adsorption data and values computed from
        adsortion data, used later in the BET analysis

    adsorbate: string
        adsorbate name, for reference

    a_o: float
        cross sectional surface area of adsorbate in square angstrom
    """

    file = input("Enter name for dataset:")
    info = input("Enter name of adsorbate used:")
    a_o_input = input("Enter cross sectional area of adsorbate in \
square Angstrom:")

    try:
        a_o = float(a_o_input)
    except:
        print('The ao provided is not numeric.')
        a_o_input = input("Try again, enter the cross sectional area of \
adsorbate in square Angstrom:")
        a_o = float(a_o_input)

    print('\nAdsorbate used has an adsorbed cross sectional area of \
%.2f sq. Angstrom.' % (a_o))

    # importing data and creating 'bet' and 'check1' data points
    dict_from_lists = {'relp': relp, 'n': n}
    data = pd.DataFrame(dict_from_lists)
    data['bet'] = (1 / data.n) * (data.relp / (1-data.relp))
    data['check1'] = data.n * (1 - data.relp)

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
        
    bet_results = namedtuple('bet_results', ('file', 'info', 'a_o', 'raw_data', 'ssa', 'nm', 'c', 'err', 'slope', 'intercept', 'r'))
    bet_results.file = file
    bet_results.info = info
    bet_results.a_o = a_o
    bet_results.raw_data = data

    return bet_results


def export_raw_data(bet_results):
    """Exports isothermal adsoprtion data as a .csv file.

    Parameters
    __________

    df : dataframe
        contains adsorption data and values computed from
        adsortion data, used later in the BET analysis

    file_name: string
        file name, used to name .csv file

    Returns
    _______
    """
    export_file_name = 'raw_data_export_' + bet_results.info
    df = bet_results.raw_data
    df.to_csv(export_file_name, index=None, header=True)
    print('Raw data saved as: %s' % (export_file_name))
    return


def export_processed_data(bet_results, points=5):
    """Exports processed isothermal adsoprtion data as a .csv file.

    Parameters
    __________

    df : dataframe
        contains adsorption data and values computed from
        adsortion data, used later in the BET analysis

    bet_results : namedtuple
        bet_results is the named tuple returned from the bet function, containing all data
        required to check the validity of BET theory over all relative pressure intervals

    file_name: string
        file name, used to name .csv file

    points : int
        the minimum number of experimental data points for a relative pressure interval to be considered valid

    Returns
    _______
    """
    
    df = bet_results.raw_data
    i = 0
    end_relp = np.zeros((len(df), len(df)))
    while i < len(df):
        end_relp[i:] = df.relp[i]
        i += 1

    begin_relp = np.transpose(end_relp)

    mask1 = bet.check_1(df)
    mask2 = bet.check_2(bet_results.intercept)
    mask3 = bet.check_3(df, bet_results.nm)
    mask4 = bet.check_4(df, bet_results.nm, bet_results.slope, bet_results.intercept)
    mask5 = bet.check_5(df, points)
   
    processed_data = np.column_stack((begin_relp.flatten(),
                                      end_relp.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.ssa.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.nm.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.c.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.err.flatten()))
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
                                           'nm [mol/g]', 'error', 'slope', 'y-int',
                                           'r value', 'check1', 'check2',
                                           'check3', 'check4', 'check5'])

    export_file_name = 'processed_data_export_' + bet_results.info
    processed_data.to_csv(export_file_name, index=None, header=True)
    print('Processed data saved as: %s' % (export_file_name))
    return
