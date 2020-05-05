#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:46:59 2019

@author: ellsworthbell
"""


from prettytable import PrettyTable
import numpy as np
from beatmap import utils as util


def ascii_tables(df, ssa, c, err):
    """Creates and populates ASCII formatted tables of BET results.

    Parameters
    __________
    c : array
        masked array of BET constant values

    ssa : array
        masked array of specific surface area values

    err : array
        masked array of error values

    df : dataframe
        dataframe of imported isotherm

    Returns
    _______
    none

    """


    if ssa.mask.all() == True:
        print('No valid relative pressure ranges. ASCII tables not created.')
        return

    c = np.nan_to_num(c)

    ssamax, ssa_max_idx, ssamin, ssa_min_idx = util.max_min(ssa)
    cmax, c_max_idx, cmin, c_min_idx = util.max_min(c)

    ssamean = np.ma.mean(ssa)
    ssamedian = np.ma.median(ssa)
    cmean = np.ma.mean(c)
    cmedian = np.ma.median(c)

    ssa_std = np.nan_to_num(ssa)[ssa != 0].std()
    c_std = np.nan_to_num(c)[c != 0].std()

    err_max, err_max_idx, err_min, err_min_idx = util.max_min(err)

    cmax_err = float(c[err_max_idx[0], err_max_idx[1]])
    cmin_err = float(c[err_min_idx[0], err_min_idx[1]])

    # these are just variables to print in tables
    ssa_min = round(ssamin, 3)
    ssa_min_c = round(float(c[ssa_min_idx[0], ssa_min_idx[1]]), 3)
    ssa_min_start_ppo = round(float(df.relp[ssa_min_idx[1]]), 3)
    ssa_min_end_ppo = round(float(df.relp[ssa_min_idx[0]]), 3)
    ssa_max = round(ssamax, 3)
    ssa_max_c = round(float(c[ssa_max_idx[0], ssa_max_idx[1]]), 3)
    ssa_max_start_ppo = round(float(df.relp[ssa_max_idx[1]]), 3)
    ssa_max_end_ppo = round(float(df.relp[ssa_max_idx[0]]), 3)
    ssa_mean = round(ssamean, 3)
    ssa_median = round(ssamedian, 3)

    c_min = round(cmin, 3)
    c_min_sa = round(float(ssa[c_min_idx[0], c_min_idx[1]]), 3)
    c_min_start_ppo = round(float(df.relp[c_min_idx[1]]), 3)
    c_min_end_ppo = round(float(df.relp[c_min_idx[0]]), 3)
    c_min_err = round(float(err[c_min_idx[0], c_min_idx[1]]), 3)
    c_max = round(cmax, 3)
    c_max_sa = round(float(ssa[c_max_idx[0], c_max_idx[1]]), 3)
    c_max_start_ppo = round(float(df.relp[c_max_idx[1]]), 3)
    c_max_end_ppo = round(float(df.relp[c_max_idx[0]]), 3)
    c_max_err = round(float(err[c_max_idx[0], c_max_idx[1]]), 3)
    c_mean = round(cmean, 3)
    c_median = round(cmedian, 3)
    cmin_err = round(cmin_err, 3)
    c_min_err_sa = round(float(ssa[err_min_idx[0], err_min_idx[1]]), 3)
    c_min_err_start_ppo = round(float(df.relp[err_min_idx[1]]), 3)
    c_min_err_end_ppo = round(float(df.relp[err_min_idx[0]]), 3)
    err_min = round(err_min, 3)
    cmax_err = round(cmax_err, 3)
    c_max_err_sa = round(float(ssa[err_max_idx[0], err_max_idx[1]]), 3)
    c_max_err_start_ppo = round(float(df.relp[err_max_idx[1]]), 3)
    c_max_err_end_ppo = round(float(df.relp[err_max_idx[0]]), 3)
    err_max = round(err_max, 3)

    table = PrettyTable()
    table.field_names = ['', 'Spec SA m2/g', 'C', 'Start P/Po', 'End P/Po']
    table.add_row(['Min Spec SA', ssa_min, ssa_min_c, ssa_min_start_ppo,
                   ssa_min_end_ppo])
    table.add_row(['Max Spec SA', ssa_max, ssa_max_c, ssa_max_start_ppo,
                   ssa_max_end_ppo])
    table.add_row(['Mean Spec SA', ssa_mean, 'n/a', 'n/a', 'n/a'])
    table.add_row(['Median Spec SA', ssa_median, 'n/a', 'n/a', 'n/a'])
    print('\n')
    print(table)
    print('Standard deviation of specific surface area = %.3f' % (ssa_std))

    table2 = PrettyTable()
    table2.field_names = ['', 'C, BET constant', 'Spec SA', 'Start P/Po',
                          'End P/Po', 'error']
    table2.add_row(['Min C', c_min, c_min_sa, c_min_start_ppo, c_min_end_ppo,
                    c_min_err])
    table2.add_row(['Max C', c_max, c_max_sa, c_max_start_ppo, c_max_end_ppo,
                    c_max_err])
    table2.add_row(['Mean C', c_mean, 'n/a', 'n/a', 'n/a', 'n/a'])
    table2.add_row(['Median C', c_median, 'n/a', 'n/a', 'n/a', 'n/a'])
    table2.add_row(['Min Error C', cmin_err, c_min_err_sa, c_min_err_start_ppo,
                    c_min_err_end_ppo, err_min])
    table2.add_row(['Max Error C', cmax_err, c_max_err_sa, c_max_err_start_ppo,
                    c_max_err_end_ppo, err_max])
    print('\n')
    print(table2)
    print('Standard deviation of BET constant (C) = %.5f' % (c_std))

    return
