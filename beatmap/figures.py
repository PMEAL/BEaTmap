#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:26:18 2019

@author: ellsworthbell
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sns
import util

def experimental_data_plot(df, file_name):
    """Creates a scatter plot of experimental data.

    Typical isotherm presentation where
    x-axis is relative pressure, y-axis is specific amount adsorbed.
    
    Parameters
    __________
    df : dataframe
        dataframe of imported experimental data

    file_name : str
        file name used to import .csv data, this function uses it to name the output .png file
        
    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """

    fig, (ax) = plt.subplots(1, 1, figsize=(13,13))
    ax.plot(df.relp, df.n, c='grey', marker='o', linewidth=0)
    ax.set_xlim(-.05, 1.05)
    ax.set_title('Experimental Isotherm')
    ax.set_ylabel('n [mol/g]')
    ax.set_xlabel('P/Po')
    ax.grid(b=True, which='major', color='gray', linestyle='-')
    fig.savefig('experimentaldata_%s.png' % (file_name[:-4]), bbox_inches='tight')
    print('Experimental data plot saved as: experimentaldata_%s.png' % (file_name[:-4]))
    return()


def experimental_data_1stderiv_plot(df, file_name):
    """Creates a scatter plot of experimental data's first derivative.

    dn/drelp, computed from experimental data
    x-axis is relative pressure, y-axis is dndrelp
    this plot is to aid in isotherm type identification
    
    Parameters
    __________
    df : dataframe
        dataframe of imported experimental data

    file_name : str
        file name used to import .csv data, this function uses it to name the output .png file
        
    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """
    fig, (ax) = plt.subplots(1, 1, figsize=(13, 13))
    ax.plot(df.relp, df.dndp, c='grey', marker='o', linewidth=0)
    ax.set_title('Experimental Isotherm 1st Derivative')
    ax.set_ylabel('dn/dp')
    ax.set_xlabel('P/Po')
    ax.grid(b=True, which='major', color='gray', linestyle='-')
    fig.savefig('expdata1deriv_%s.png' % (file_name[:-4]), bbox_inches='tight')
    print('Experimental data first derivative plot saved as: expdata1deriv_%s.png' % (file_name[:-4]))
    return()


def ssa_heatmap(df, sa, file_name, gradient = 'Greens'):
    """Creates a heatmap of specific surface areas.

    Shading corresponds to specific surface area, normalized for the minimum and maximum spec sa values.
    
    Parameters
    __________
    df : dataframe
        dataframe of imported experimental data, used to label heatmap axis

    sa : array
        array of specific surface area values, resulting from BET analysis
        if the array has had masks applied to it the resulting heatmap will be masked

    file_name : str
        file name used to import .csv data, this function uses it to name the output .png file
        
    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """
    
    if np.any(sa) == False:
        print('No valid relative pressure ranges. Specific surface area heat map not created.')
        return
    
    # finding max and min sa to normalize heatmap colours
    samax, sa_max_idx, samin, sa_min_idx = util.max_min(sa)
    hm_labels = round(df.relp * 100, 1)
    fig, ax= plt.subplots(1,1, figsize=(13, 13))
    sns.heatmap(sa, vmin=samin, vmax=samax, square=True, cmap=gradient,
                mask=(sa==0), xticklabels=hm_labels, yticklabels=hm_labels,
                linewidths=1, linecolor='w', cbar_kws={'shrink':.78, 'aspect':len(df.relp)})
    ax.invert_yaxis()
    ax.set_title('BET Specific Surface Area [m^2/g]')
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.xlabel('Start Relative Pressure')
    plt.yticks(rotation=45, horizontalalignment='right')
    plt.ylabel('End Relative Pressure') 
    fig.savefig('ssa_heatmap_%s.png' % (file_name[:-4]), bbox_inches='tight')
    print('Specific surface area heatmap saved as: ssa_heatmap_%s.png' % (file_name[:-4]))
    return


def theta_heatmap(df, theta, file_name, gradient = 'PiYG', center = 1):
    """Creates a heatmap of theta values.

    Shading corresponds to theta, normalized for the minimum and maximum theta values, 0 = white
    Can be used to explore correlation between theta in BET analysis and BET specific surface area
    
    Parameters
    __________
    df : dataframe
        dataframe of imported experimental data, used to label heatmap axis

    theta : array
        array of theta values, resulting from theta function
        if the array has had masks applied to it the resulting heatmap will be masked

    file_name : str
        file name used to import .csv data, this function uses it to name the output .png file
        
    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """
    
    if np.any(theta) == False:
        print('No valid relative pressure ranges. Theta heat map not created.')
        return
    
    thetamax, theta_max_idx, thetamin, theta_min_idx = util.max_min(theta)
    hm_labels = round(df.relp * 100, 1)
    fig, (ax) = plt.subplots(1, 1, figsize=(13, 13))
    sns.heatmap(theta, vmin=thetamin, vmax=thetamax, square=True, cmap=gradient,
                center=center, mask=(theta==0), xticklabels=hm_labels, yticklabels=hm_labels,
                linewidths=1, linecolor='w', cbar_kws={'shrink':.78, 'aspect':len(df.relp)})
    ax.invert_yaxis()
    ax.set_title('BET Theta (n/nm) where n is Median of Pressure Range')
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.xlabel('Start Relative Pressure')
    plt.yticks(rotation=45, horizontalalignment='right')
    plt.ylabel('End Relative Pressure')
    fig.savefig('theta_heatmap_%s.png' % (file_name[:-4]), bbox_inches='tight')
    print('Theta heatmap saved as: theta_heatmap_%s.png' % (file_name[:-4]))
    return


def err_heatmap(df, err, file_name, gradient = 'Greys'):
    """Creates a heatmap of error values.

    Shading corresponds to theta, normalized for the minimum and maximum theta values, 0 = white
    Can be used to explore correlation between error in BET analysis and BET specific surface area
    
    Parameters
    __________
    df : dataframe
        dataframe of imported experimental data, used to label heatmap axis

    error : array
        array of theta values, resulting from error calculation
        if the array has had masks applied to it the resulting heatmap will be masked

    file_name : str
        file name used to import .csv data, this function uses it to name the output .png file
        
    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """
    
    if np.any(err) == False:
        print('No valid relative pressure ranges. Error heat map not created.')
        return
    
    errormax, error_max_idx, errormin, error_min_idx = util.max_min(err)

    hm_labels = round(df.relp * 100, 1)
    fig, (ax) = plt.subplots(1, 1, figsize=(13, 13))
    sns.heatmap(err, vmin=0, vmax=errormax, square=True, cmap=gradient, mask=(err==0),
                xticklabels=hm_labels, yticklabels=hm_labels, linewidths=1, linecolor='w',
                cbar_kws={'shrink':.78, 'aspect':len(df.relp)})
    ax.invert_yaxis()
    ax.set_title('BET Error Between Experimental and Theoretical Isotherms')
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.xlabel('Start Relative Pressure')
    plt.yticks(rotation=45, horizontalalignment='right')
    plt.ylabel('End Relative Pressure')
    fig.savefig('error_heatmap_%s.png' % (file_name[:-4]), bbox_inches='tight')
    print('Error heatmap saved as: error_heatmap_%s.png' % (file_name[:-4]))
    return
    
    
def diff_heatmap(df, diff, file_name, gradient = 'PuOr', center = 0):
    """Creates a heatmap of error values.

    Shading corresponds to theta, normalized for the minimum and maximum theta values, 0 = white
    Can be used to explore correlation between error in BET analysis and BET specific surface area
    
    Parameters
    __________
    df : dataframe
        dataframe of imported experimental data, used to label heatmap axis

    diff : array
        array of difference values, resulting from multipoint - single point
        if the array has had masks applied to it the resulting heatmap will be masked

    file_name : str
        file name used to import .csv data, this function uses it to name the output .png file
        
    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*
    """
    if np.any(diff) == False:
        print('No valid relative pressure ranges. Difference heat map not created.')
        return
    
    diffmax, diff_max_idx, diffmin, diff_min_idx = util.max_min(diff)

    hm_labels = round(df.relp * 100, 1)
    fig, (ax) = plt.subplots(1, 1, figsize=(13, 13))
    sns.heatmap(diff, vmin=diffmin, vmax=diffmax, square=True, cmap=gradient,
                mask=(diff==0), xticklabels=hm_labels, yticklabels=hm_labels, center=center,
                linewidths=1, linecolor='w', cbar_kws={'shrink':.78, 'aspect':len(df.relp)})
    ax.invert_yaxis()
    ax.set_title('BET Difference Between Multipoint and Single Point: Diff = Multi - Single')
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.xlabel('Start Relative Pressure')
    plt.yticks(rotation=45, horizontalalignment='right')
    plt.ylabel('End Relative Pressure')
    fig.savefig('diff_heatmap_%s.png' % (file_name[:-4]), bbox_inches='tight')
    print('Difference heatmap saved as: diff_heatmap_%s.png' % (file_name[:-4]))
    return
    

def bet_combo_plot(c, err, df, file_name): #requires masked c and error array
    """Creates two BET plots, for the minimum and maxium error data sets.

    Only datapoints in the minimum and maximum error data sets are plotted
    Line is fit using scipy.stats.linregress
    Equation for best fit line and corresponding R value are annotated on plots
    Image is 2 by 1, two BET plots arranged horizontally in one image
    
    Parameters
    __________
    c : array
        array of C values, resulting from BET analysis
        this array should have masks applied to it
        if the array has had masks applied to it only the valid relative pressure ranges will be considered

    error : array
        array of error values, resulting from BET analysis
        this array should have masks applied to it
        if the array has had masks applied to it only the valid relative pressure ranges will be considered

    df : dataframe
        dataframe of imported experimental data, used to label heatmap axis

    file_name : str
        file name used to import .csv data, this function uses it to name the output .png file
        
    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """
    
    if np.any(err) == False:
        print('No valid relative pressure ranges. BET combo plot not created.')
        return
    
    err_max, err_max_idx, err_min, err_min_idx = util.max_min(err)

    min_start = int(err_min_idx[1])
    min_stop = int(err_min_idx[0])
    max_start = int(err_max_idx[1])
    max_stop = int(err_max_idx[0])

    slope, intercept, r_value, p_value, std_err =\
        sp.stats.linregress(df.relp[min_start: min_stop],
                            df.bet[min_start:min_stop])
    min_liney = np.zeros(2)
    min_liney[0] = slope * (df.relp[min_start] - .01) + intercept
    min_liney[1] = slope * (df.relp[min_stop] + .01) + intercept
    min_linex = np.zeros(2)
    min_linex[0] = df.relp[min_start] - .01
    min_linex[1] = df.relp[min_stop] + .01

    figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    ax1.set_title('BET Plot - Data Points for Minimum Error C')
    ax1.set_xlim(min_linex[0]-.01, min_linex[1]+.01)
    ax1.set_ylabel('1/[n(1-Po/P)]')
    ax1.set_ylim(min_liney[0]*.9, min_liney[1]*1.1)
    ax1.set_xlabel('P/Po')
    ax1.grid(b=True, which='major', color='gray', linestyle='-')
    ax1.plot(df.relp[min_start:min_stop + 1], df.bet[min_start:min_stop + 1],
             label='Experimental Data', c='grey', marker='o', linewidth=0)
    ax1.plot(min_linex, min_liney, color='black', label='Linear Regression')
    ax1.legend(loc='upper left', framealpha=1)
    ax1.annotate('Linear Regression: \nm = %.3f \nb = %.3f \nR = %.3f'
                 % (slope, intercept, r_value),
                 bbox=dict(boxstyle="round", fc='white', ec="gray", alpha=1),
                 textcoords='axes fraction', xytext=(.775, .018),
                 xy=(df.relp[min_stop], df.bet[min_start]), size=11)

    slope, intercept, r_value, p_value, std_err = \
        sp.stats.linregress(df.relp[max_start: max_stop],
                            df.bet[max_start: max_stop])
    max_liney = np.zeros(2)
    max_liney[0] = slope * (df.relp[max_start] - .01) + intercept
    max_liney[1] = slope * (df.relp[max_stop] + .01) + intercept
    max_linex = np.zeros(2)
    max_linex[0] = df.relp[max_start] - .01
    max_linex[1] = df.relp[max_stop] + .01

    ax2.set_title('BET Plot - Data Points for Maximum Error C')
    ax2.set_xlim(max_linex[0]-.01, max_linex[1]+.01)
    ax2.set_xlabel('P/Po')
    ax2.set_ylabel('1/[n(1-Po/P)]')
    ax2.set_ylim(max_liney[0]*.9, max_liney[1]*1.1)
    ax2.grid(b=True, which='major', color='gray', linestyle='-')
    ax2.plot(df.relp[max_start:max_stop], df.bet[max_start:max_stop],
             label='Experimental Data', c='grey', marker='o', linewidth=0)
    ax2.plot(max_linex, max_liney, color='black', label='Linear Regression')
    ax2.annotate('Linear Regression: \nm = %.3f \nb = %.3f \nR = %.3f'
                 % (slope, intercept, r_value),
                 bbox=dict(boxstyle="round", fc='white', ec="gray", alpha=1),
                 textcoords='axes fraction', xytext=(.775, .018), 
                 xy=(df.relp[max_stop], df.bet[max_start + 1]), size=11)
    figure.savefig('betplot_%s.png' % (file_name[:-4]), bbox_inches='tight')
    print('BET plot saved as: betplot_%s.png' % (file_name[:-4]))
    return


# "BET isocombo plot" is a way to visually compare the "best" and "worst"
# values of C (in terms of error)
def bet_iso_combo_plot(c, err, sa, nm, df, file_name): #requires masked c, err, sa, and nm arrays!
    """Creates an image to visually compare the "best" and "worst" values of C.

    Image is 4 by 4, with two "decomposed isotherm" plots on the top row
    and two BET plots on the bottom row.
    The x axis scale is kept constant on all plots so that data points map nicely.
    Only datapoints in the minimum and maximum error data sets are plotted
    Line is fit using scipy.stats.linregress
    Equation for best fit line and corresponding R value are annotated on plots
    See documentation for more information on this plot.
    
    Parameters
    __________
    c : array
        array of C values, resulting from BET analysis
        this array should have masks applied to it
        if the array is masked only the valid relative pressure ranges will be considered

    error : array
        array of error values, resulting from BET analysis
        this array should have masks applied to it
        if the array is masked only the valid relative pressure ranges will be considered
        
    nm : array
        array of monolayer adsorbed amount, resulting from BET analysis
        this array should have masks applied to it
        if the array is masked only the valid relative pressure ranges will be considered

    df : dataframe
        dataframe of imported experimental data, used to label heatmap axis

    file_name : str
        file name used to import .csv data, this function uses it to name the output .png file
        
    Returns
    _______
    none

    Saves image file in same directory as figures.py code
    *CHANGE OUTPUT LOC BEFORE PACKAGING?!*

    """
    
    if np.any(err) == False:
        print('No valid relative pressure ranges. BET isotherm combo plot not created.')
        return
    
    err_max, err_max_idx, err_min, err_min_idx = util.max_min(err)
    c_max_err = c[err_max_idx[0], err_max_idx[1]]
    c_min_err = c[err_min_idx[0], err_min_idx[1]]

    nnm_min = nm[err_min_idx[0], err_min_idx[1]]
    nnm_max = nm[err_max_idx[0], err_max_idx[1]]
    ppo = np.arange(-.1, .9001, .001)
    nnm1 = 1 / (1 - ppo)
    nnm2_min = 1 / (1 + (c_min_err - 1) * ppo)
    nnm2_max = 1 / (1 + (c_max_err - 1) * ppo)
    synth_min = nnm1 - nnm2_min
    synth_max = nnm1 - nnm2_max
    expnnm_min = df.n / nnm_min
    err_min_i = int(err_min_idx[0] + 1)
    err_min_j = int(err_min_idx[1])
    expnnm_min_used = expnnm_min[err_min_j:err_min_i]
    ppo_expnnm_min_used = df.relp[err_min_j:err_min_i]
    expnnm_max = df.n / nnm_max
    err_max_i = int(err_max_idx[0] + 1)
    err_max_j = int(err_max_idx[1])
    expnnm_max_used = expnnm_max[err_max_j:err_max_i]
    ppo_expnnm_max_used = df.relp[err_max_j:err_max_i]

    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2,
                                               figsize=(20, 20))

    ax1.set_title('Isotherm as a composition of two equations, a and b - Minimum Error C')
    ax1.set_ylim(-1, synth_min[-2]+1)
    ax1.set_xlim(-.05, 1.05)
    ax1.set_ylabel('n/nm')
    ax1.set_xlabel('P/Po')
    ax1.grid(b=True, which='major', color='gray', linestyle='-')
    ax1.plot(ppo, nnm1, linestyle='--', linewidth=1, c='b',
             label='a = 1/(1-P/Po)')
    ax1.plot(ppo, nnm2_min, linestyle='--', linewidth=1, c='r',
             label='b = 1/(1+(c-1)(P/Po))')
    ax1.plot(ppo, synth_min, linestyle='-', linewidth=1, c='y',
             label='Theoretical isotherm', marker='')
    ax1.plot(ppo_expnnm_min_used, expnnm_min_used, c='grey',
             label='Experimental isotherm - used data',
             marker='o', linewidth=0)
    ax1.plot(df.relp, expnnm_min, c='grey', fillstyle='none',
             label='Experimental isotherm', marker='o', linewidth=0)
    ax1.plot([-.05, 1.05], [1, 1], c='grey', linestyle='-', linewidth=1, marker = '')
    ax1.legend(loc='upper left', framealpha=1)

    ax2.set_title('Isotherm as a composition of two equations, a and b - Maximum Error C')
    ax2.set_ylabel('n/nm')
    ax2.set_xlabel('P/Po')
    ax2.set_ylim(-1, synth_max[-2] +1)
    ax2.set_xlim(-.05, 1.05)
    ax2.grid(b=True, which='major', color='gray', linestyle='-')
    ax2.plot(ppo, nnm1, linestyle='--', linewidth=1, c='b',
             label='a = 1/(1-P/Po)')
    ax2.plot(ppo, nnm2_max, linestyle='--', linewidth=1, c='r',
             label='b = 1/(1+(c-1)(P/Po))')
    ax2.plot(ppo, synth_max, linestyle='-', linewidth=1, c='y',
             label='Theoretical isotherm', marker='')
    ax2.plot(ppo_expnnm_max_used, expnnm_max_used, c='grey',
             label='Experimental isotherm - used data',
             marker='o', linewidth=0)
    ax2.plot(df.relp, expnnm_max, c='grey', fillstyle='none',
             label='Experimental isotherm', marker='o', linewidth=0)
    ax2.plot([-.05, 1.05], [1, 1], c='grey', linestyle='-', linewidth=1, marker = '')
    
    min_start = int(err_min_idx[1])
    min_stop = int(err_min_idx[0])
    max_start = int(err_max_idx[1])
    max_stop = int(err_max_idx[0])
    
    
    slope, intercept, r_value, p_value, std_err = \
        sp.stats.linregress(df.relp[min_start: min_stop],
                            df.bet[min_start: min_stop])
    min_liney = np.zeros(2)
    min_liney[0] = slope * (df.relp[min_start] - .01) + intercept
    min_liney[1] = slope * (df.relp[min_stop] + .01) + intercept
    min_linex = np.zeros(2)
    min_linex[0] = df.relp[min_start] -.01
    min_linex[1] = df.relp[min_stop] +.01
    ax3.set_title('BET Plot - Data Points for Minimum Error C')
    ax3.set_xlim(-.05, 1.05)
    ax3.set_ylim(min_liney[0]*.9, min_liney[1]*1.1)
    ax3.set_ylabel('1/[n(1-Po/P)]')
    ax3.set_xlabel('P/Po')
    ax3.grid(b=True, which='major', color='gray', linestyle='-')
    ax3.plot(df.relp[min_start:min_stop + 1], df.bet[min_start:min_stop + 1],
             label='Experimental Data', c='grey', marker='o', linewidth=0)
    ax3.plot(min_linex, min_liney, color='black', label='Linear Regression')
    ax3.legend(loc='upper left', framealpha=1)
    ax3.annotate('Linear Regression: \nm = %.3f \nb = %.3f \nR = %.3f'
                 % (slope, intercept, r_value),
                 bbox=dict(boxstyle="round", fc='white', ec="gray", alpha=1),
                 textcoords='axes fraction', xytext=(.775, .018),
                 xy=(df.relp[min_stop], df.bet[min_start]), size=11)

    slope, intercept, r_value, p_value, std_err =\
        sp.stats.linregress(df.relp[max_start:max_stop],
                            df.bet[max_start:max_stop])
    max_liney = np.zeros(2)
    max_liney[0] = slope * (df.relp[max_start] - .01) + intercept
    max_liney[1] = slope * (df.relp[max_stop] + .01) + intercept
    max_linex = np.zeros(2)
    max_linex[0] = df.relp[max_start] -.01
    max_linex[1] = df.relp[max_stop] +.01

    ax4.set_title('BET Plot - Data Points for Maximum Error C')
    ax4.set_ylabel('1/[n(1-Po/P)]')
    ax4.set_xlabel('P/Po')
    ax4.set_xlim(-.05, 1.05)
    ax4.set_ylim(max_liney[0]*.9, max_liney[1]*1.1)
    ax4.grid(b=True, which='major', color='gray', linestyle='-')
    ax4.plot(df.relp[max_start:max_stop + 1], df.bet[max_start:max_stop + 1],
             label='Experimental Data', c='grey', marker='o', linewidth=0)
    ax4.plot(max_linex, max_liney, color='black', label='Linear Regression')
    ax4.annotate('Linear Regression: \nm = %.3f \nb = %.3f \nR = %.3f'
                 % (slope, intercept, r_value),
                 bbox=dict(boxstyle="round", fc='white', ec="gray", alpha=1),
                 textcoords='axes fraction', xytext=(.775, .018),
                 xy=(df.relp[min_stop], df.bet[min_start]), size=11)
    f.savefig('isothermcomp_%s.png' % (file_name[:-4]), bbox_inches='tight')
    print('Isotherm decomposition plot saved as: isothermcomp_%s.png' % (file_name[:-4]))
    return
