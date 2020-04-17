#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:16:10 2019

@author: ellsworthbell
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import dataio
import getadsorbate
import bet
import util
import settables

# file = input("Enter file name/path:" )
# Ca = input("Enter Ca value:")
    # for now just use EtOH isotherms, Ca = mean C for EtOH onto slight sample,
    # init_nma = corresponding nm value for Ca
    # using philic as other dataset because big diff between mean C
    # for philic and slight (49.26 and 14.96 respectively)

# ONLY WORKS WITH SLIGHT_02 INITIAL SETTINGS AND PHILIC_02 DATA!!!!!!!
# CHANGE START SO LOWEST CA IS USED AS IC?

#Unmodified surface = "a", modified surface = no prefix
a_file = input("Enter file name/path of the unmodified surface isotherm:")
a_df = dataio.import_dvs_data(a_file)
a_adsorbate, a_ads_vp, a_ads_xc_area = getadsorbate.get_adsorbate(a_df)

print("\n", a_df)
print('\nAdsorbate used for unmodified material isotherm was %s with a vapor pressure of %.2f mmHg and an \
adsorbed cross sectional area of %.2f sq. Angstrom.'
      % (a_adsorbate, a_ads_vp, a_ads_xc_area))

file = input("\nEnter file name/path of the modified surface isotherm:")
df = dataio.import_dvs_data(file)
adsorbate, ads_vp, ads_xc_area = getadsorbate.get_adsorbate(df)

print("\n", df)
print('\nAdsorbate used for modified material iotherm was %s with a vapor pressure of %.2f mmHg and an \
adsorbed cross sectional area of %.2f sq. Angstrom.'
      % (adsorbate, ads_vp, ads_xc_area))

if a_adsorbate == adsorbate:
    print("\nAdsorbates match.")

a_sa, a_c, a_nm, a_err, a_linreg = bet.bet(a_df, a_ads_xc_area)
sa, c, nm, err, linreg = bet.bet(df, ads_xc_area)

a_mask = bet.combine_masks(a_df, a_linreg, a_nm)
mask = bet.combine_masks(df, linreg, nm)

a_masked_sa = np.multiply(a_sa, a_mask)
a_masked_c = np.multiply(a_c, a_mask)
a_masked_nm = np.multiply(a_nm, a_mask)
a_masked_error = np.multiply(a_err, a_mask)

masked_ssa = np.multiply(sa, mask)
masked_c = np.multiply(c, mask)
masked_nm = np.multiply(nm, mask)
masked_error = np.multiply(err, mask)

a_err_max, a_err_max_idx, a_err_min, a_err_min_idx = util.max_min(a_masked_error)
err_max, err_max_idx, err_min, err_min_idx = util.max_min(masked_error)

"""this doesn't work because the index shared by both the min error ranges isn't
necessiarly a vaild (ie unmasked) point"""
# =============================================================================
# if a_err_min_idx[1] >= err_min_idx[1]:
#     start_idx = int(a_err_min_idx[1])
# else:
#     start_idx = int(err_min_idx[1])
# 
# if a_err_min_idx[0] <= err_min_idx[0]:
#     end_idx = int(a_err_min_idx[0])
# else:
#     end_idx = int(err_min_idx[0])
# 
# print(df.relp[start_idx],"\n",df.relp[end_idx])
# 
# a_dual_c = a_masked_c[end_idx, start_idx]
# a_dual_nm = a_nm[end_idx, start_idx]
# dual_nm = masked_nm[end_idx, start_idx]
# dual_c = masked_c[end_idx, start_idx]
# =============================================================================

start_idx = int(a_err_min_idx[1])
end_idx = int(a_err_min_idx[0])

a_dual_c = a_masked_c[end_idx, start_idx]
a_dual_nm = a_nm[end_idx, start_idx]
dual_nm = masked_nm[end_idx, start_idx]
dual_c = masked_c[end_idx, start_idx]

print(df.relp[start_idx],"\n",df.relp[end_idx])

print("a_dual_c=", a_dual_c, "\ndual_nm=", dual_nm, "\ndual_c=", dual_c)

print("\nAscii tables for the unmodified surface")
settables.ascii_tables(a_masked_c, a_masked_sa, a_masked_error, a_df)
print("\nAscii tables for the modified surface")
settables.ascii_tables(masked_c, masked_ssa, masked_error, df)

print('dual nm', dual_nm)
a_nm_guess = a_dual_nm/2000 #inital guess for nm of surface a (unmodified surface)

# =============================================================================
# a_ds_isotherm = pd.DataFrame(data=a_df.relp[start_idx:end_idx+1]) #range of relp shared by both isotherms minimum error BET plot
# a_ds_isotherm['bet'] = (1/(a_nm_guess*a_dual_c)) + (((a_dual_c - 1)*a_ds_isotherm.relp) / (a_nm_guess * a_dual_c))
# ds_isotherm = pd.DataFrame(data=a_df.relp[start_idx:end_idx+1])
# ds_isotherm['bet'] = df.bet - a_ds_isotherm.bet 
# =============================================================================

a_n = (((1 / (a_nm_guess * a_dual_c)) + (((a_dual_c - 1) * df.relp[start_idx:end_idx+1]) / (a_nm_guess * a_dual_c))) ** -1) * ((df.relp[start_idx:end_idx+1]) / (1 - df.relp[start_idx:end_idx+1]))
n = df.n[start_idx:end_idx+1] - a_n
ds_isotherm = pd.DataFrame(data=a_df.relp[start_idx:end_idx+1])
ds_isotherm['bet'] = df.relp[start_idx:end_idx+1] / (n * (1 - df.relp[start_idx:end_idx+1]))



m = (ds_isotherm['bet'].iloc[0] - ds_isotherm['bet'].iloc[-1]) / (ds_isotherm['relp'].iloc[0] - ds_isotherm['relp'].iloc[-1])
b = ds_isotherm['bet'].iloc[1] - m * ds_isotherm['relp'].iloc[1]

line = m * ds_isotherm.relp + b

diff = ds_isotherm.bet - (m * ds_isotherm.relp + b)
print(diff)
sum_diff = sum(diff)

while abs(sum_diff) > .001 and abs(a_nm_guess) > dual_nm*.000001:
    if sum_diff > 0:
        a_nm_guess = a_nm_guess * 1.5 * a_nm_guess
    else:
        a_nm_guess = a_nm_guess - .5 *a_nm_guess
    
    print(a_nm_guess)
    a_n = (((1 / (a_nm_guess * a_dual_c)) + (((a_dual_c - 1) * df.relp[start_idx:end_idx+1]) / (a_nm_guess * a_dual_c))) ** -1) * ((df.relp[start_idx:end_idx+1]) / (1 - df.relp[start_idx:end_idx+1]))
    n = df.n[start_idx:end_idx+1] - a_n
    ds_isotherm['bet'] = df.relp[start_idx:end_idx+1] / (n * (1 - df.relp[start_idx:end_idx+1]))
    m = (ds_isotherm['bet'].iloc[0] - ds_isotherm['bet'].iloc[1]) / (ds_isotherm['relp'].iloc[0] - ds_isotherm['relp'].iloc[1])
    b = ds_isotherm['bet'].iloc[1] - m * ds_isotherm['relp'].iloc[1]
    line = m * ds_isotherm.relp + b
    diff = ds_isotherm.bet - (m * ds_isotherm.relp + b)
    

print('sum_diff', sum_diff)
print('ds_isotherm_bet', ds_isotherm['bet'])

nm_b = dual_nm - a_nm_guess
print('a_nm', a_nm_guess, 'b_nm', nm_b, 'surf_cov', nm_b/dual_nm)

f, ax2 = plt.subplots()
ax2.plot(ds_isotherm.relp, ds_isotherm.bet, marker='o', linewidth=0)
ax2.plot(ds_isotherm.relp, line, linestyle='-', linewidth=1)

#print("\n", a_masked_sa)
#print("\n", sa)

"""
nma = init_nma

isotherm = pd.DataFrame(data=df.relp[5:21])
isotherm['bet'] = isotherm.relp / (df.n * (1-isotherm.relp))

isotherm_a = pd.DataFrame(data=df.relp[5:21])
isotherm_a['n'] = (isotherm_a.relp / (1 - isotherm_a.relp)) *\
                    ((nma * Ca) / (1 + (Ca - 1) * isotherm_a.relp))

isotherm_b = pd.DataFrame(data=df[5:21])
isotherm_b.n = isotherm_b.n - isotherm_a.n
isotherm_b['bet'] = isotherm_b.relp / (isotherm_b.n * (1 - isotherm_b.relp))

# plt.scatter(isotherm_b.relp, isotherm_b.bet)
line = np.array([[.05, isotherm_b.bet[5]], [.35, isotherm_b.bet[20]]])
f, ax = plt.subplots()
ax.plot(isotherm_b.relp, isotherm_b.bet, marker='o', linewidth=0)
ax.plot(line[:, 0], line[:, 1], linestyle='-', linewidth=1)


slope = (isotherm_b.bet[20]-isotherm_b.bet[5]) /\
        (isotherm_b.relp[20] - isotherm_b.relp[5])
y_int = isotherm_b.bet[20] - slope*isotherm_b.relp[20]
error = isotherm_b.bet - (slope*isotherm_b.relp + y_int)
error = sum(error)

nma_span = np.linspace(0, init_nma*3, num=2000)
error_span = np.zeros(2000)

i = 0
while i < len(nma_span):
    isotherm_a.n = (isotherm_a.relp / (1 - isotherm_a.relp)) *\
                    ((nma_span[i]*Ca) / (1 + (Ca - 1) * isotherm_a.relp))
    isotherm_b.n = df.n[5:21] - isotherm_a.n
    isotherm_b.bet = isotherm_b.relp /\
        (isotherm_b.n * (1 - isotherm_b.relp))
    slope = (isotherm_b.bet[20]-isotherm_b.bet[5]) /\
            (isotherm_b.relp[20] - isotherm_b.relp[5])
    y_int = isotherm_b.bet[20] - slope*isotherm_b.relp[20]
    error = isotherm_b.bet - (slope*isotherm_b.relp + y_int)
    error_span[i] = sum(error)
    i = i+1


def find_min(error, nma):
    min_error = np.nanmin(abs(error))
    i_min = np.where(abs(error) == min_error)
    nma_min_error = nma[i_min]
    return(min_error, i_min, nma_min_error)


min_error, idx_min, best_nma = find_min(error_span, nma_span)
print(min_error, idx_min, best_nma)

isotherm_a.n = (isotherm_a.relp / (1 - isotherm_a.relp)) *\
            ((best_nma * Ca) / (1 + (Ca - 1) * isotherm_a.relp))
isotherm_b.n = df.n[5:21] - isotherm_a.n
isotherm_b.bet = isotherm_b.relp / (isotherm_b.n * (1 - isotherm_b.relp))
X = isotherm_b.relp
y = isotherm_b.bet
slope, intercept, r_value, p_value, std_err = sp.stats.linregress(X, y)
Cb = slope/intercept + 1
nmb = 1 / (intercept * Cb)

print(Ca, best_nma, Cb, nmb, best_nma+nmb)
line = np.array([[.05, isotherm_b.bet[5]], [.35, isotherm_b.bet[20]]])
f, ax2 = plt.subplots()
ax2.plot(isotherm_b.relp, isotherm_b.bet, marker='o', linewidth=0)
ax2.plot(line[:, 0], line[:, 1], linestyle='-', linewidth=1)
extent_mod = nmb / (best_nma + nmb)
# ^is this right or should you square it so that you're comparing areas
# as opposed to active sites???
print(extent_mod)
"""
