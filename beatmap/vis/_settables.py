#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:46:59 2019

@author: ellsworthbell
"""

import numpy as np
import pandas as pd
from prettytable import PrettyTable
from beatmap import utils as util


def ascii_tables(bet_results, rouq_mask):
    """Creates and populates ASCII formatted tables of BET results.

    Parameters
    __________
    bet_results : namedtuple
        namedtuple containing elements that result from BET  analysis

    rouq_mask : namedtuple
        namedtuple, the rouq_mask.mask element is used to mask the
        BET results so that only valid results are displayed

    Returns
    _______
    none

    """
    
    mask = rouq_mask.mask
    if mask.all() == True:
        print('No valid relative pressure ranges. ASCII tables not created.')
        return
    
    df = bet_results.raw_data
    ssa = np.ma.array(bet_results.ssa, mask=mask)
    c = np.ma.array(bet_results.c, mask=mask)
    err = np.ma.array(bet_results.err, mask=mask)
    
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
    table2.field_names = ['', 'C, BET Constant', 'Spec SA', 'Start P/Po',
                          'End P/Po', 'Error']
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


def dataframe_tables(bet_results, rouq_mask):
    """Creates and populates pandas dataframes summarizing BET results.

    Parameters
    __________
    bet_results : namedtuple
        namedtuple containing elements that result from BET  analysis

    rouq_mask : namedtuple
        namedtuple, the rouq_mask.mask element is used to mask the
        BET results so that only valid results are displayed

    Returns
    _______
    ssa_table : dataframe
         dataframe summarizing BET result, highlighting the high, low, and
         average values of specific surface area
         
    c_table : dataframe
         dataframe summarizing BET result, highlighting the high, low, and
         average values of the BET constant
         
    ssa_std : float
         standard deviation of valid specific surface area values
         
    c_std : float
         standard deviation of valid BET constant values  
 
    """
    
    mask = rouq_mask.mask
    
    if mask.all() == True:
        print('No valid relative pressure ranges. Tables not created.')
        
        ssa_dict = {' ': ['Min Spec SA', 'Max Spec SA', 'Mean Spec SA', 'Median Spec SA'],
         'Spec SA m2/g': ['n/a', 'n/a', 'n/a', 'n/a'],
         'C': ['n/a', 'n/a', 'n/a', 'n/a'],
         'Start P/Po': ['n/a', 'n/a', 'n/a', 'n/a'],
         'End P/Po': ['n/a', 'n/a', 'n/a', 'n/a']
         }
    
        ssa_table = pd.DataFrame(data=ssa_dict)
    
        c_dict = {' ': ['Min C', 'Max C', 'Mean C', 'Median C', 'Min Error C', 'Max Error C'],
              'C': ['n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a'],
              'Spec SA': ['n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a'],
              'Start P/Po': ['n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a'],
              'End P/Po': ['n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a'],
              'Error': ['n/a', 'n/a', 'n/a', 'n/a', 'n/a', 'n/a']
              }
    
        c_table = pd.DataFrame(data=c_dict)
        ssa_sdev = 'No valid relative pressure ranges. Standard deviation not calculated.'
        c_sdev = 'No valid relative pressure ranges. Standard deviation not calculated.'
        return ssa_table, c_table, ssa_sdev, c_sdev
    
    df = bet_results.raw_data
    ssa = np.ma.array(bet_results.ssa, mask=mask)
    c = np.ma.array(bet_results.c, mask=mask)
    err = np.ma.array(bet_results.err, mask=mask)
    
    c = np.nan_to_num(c) #is this necessary? --- check

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
    
    ssa_dict = {' ': ['Min Spec SA', 'Max Spec SA', 'Mean Spec SA', 'Median Spec SA'],
         'Spec SA m2/g': [ssa_min, ssa_max, ssa_mean, ssa_median],
         'C': [ssa_min_c, ssa_max_c, 'n/a', 'n/a'],
         'Start P/Po': [ssa_min_start_ppo, ssa_max_start_ppo, 'n/a', 'n/a'],
         'End P/Po': [ssa_min_end_ppo, ssa_max_end_ppo, 'n/a', 'n/a']
         }
    
    ssa_table = pd.DataFrame(data=ssa_dict)
    
    c_dict = {' ': ['Min C', 'Max C', 'Mean C', 'Median C', 'Min Error C', 'Max Error C'],
              'C': [c_min, c_max, c_mean, c_median, cmin_err, cmax_err],
              'Spec SA': [c_min_sa, c_max_sa, 'n/a', 'n/a', c_min_err_sa, c_max_err_sa],
              'Start P/Po': [c_min_start_ppo, c_max_start_ppo, 'n/a', 'n/a', c_min_err_start_ppo, c_max_err_start_ppo],
              'End P/Po': [c_min_end_ppo, c_max_end_ppo, 'n/a', 'n/a', c_min_err_end_ppo, c_max_err_end_ppo],
              'Error': [c_min_err, c_max_err, 'n/a', 'n/a', err_min, err_max]
              }
    
    c_table = pd.DataFrame(data=c_dict)
    
    return ssa_table, c_table, ssa_std, c_std