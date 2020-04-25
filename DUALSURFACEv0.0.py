#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:16:10 2019

@author: ellsworthbell
"""
import beatmap as bt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
General algorithim: have isotherm, know one C value eg Ca

guess nm_a

compute n_a
subtract n_a from n givign n_b
make bet plot of n_b values
    if convex to x axis
        decrease nm_a
    if concave to x axis
        increase nm_a




"""

#model isotherm, nma = nmb = .002, Ca = 100, Cb = 2
#relp = [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9] 
#n = [0.001055181, 0.001449707, 0.001678185, 0.001840364, 0.00196963, 0.002442776, 0.002840569, 0.003237179, 0.003655663, 0.004110678, 0.004616264, 0.005188834, 0.005849509, 0.006627063, 0.007562498, 0.008716887, 0.012128413, 0.018863951, 0.038925171]

user_input = input('Provide C and nm values? If no, defaults of Ca = 100, Cb =2, nma=nmb=.002 will be used. (y/n) :')
if user_input == 'y':
    Ca = input('Ca value:')
    Ca = float(Ca)
    Cb = input('Cb value:')
    Cb = float(Cb)
    nma = input('nma value:')
    nma = float(nma)
    nmb = input('nmb value:')
    nmb = float(nmb)
else:
    Ca = 100
    Cb = 2
    nma = .002
    nmb = nma

relp = [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9]

n = []
for item in relp:
    n = np.append(n, (item / (1 - item)) * (((nma * Ca) / (1 + (Ca - 1) * item)) + ((nmb * Cb) / (1 + (Cb - 1) * item))))
    
dict_from_lists = {'relp': relp, 'n':n}
data = pd.DataFrame(dict_from_lists)
data['bet'] = (1 / data.n) * (data.relp / (1-data.relp))
data['check1'] = data.n * (1 - data.relp)

#checking data quality
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

#plot as initial guess approaches nm_a value from below
nma_igs = np.linspace(.1 * nma, nma, 10)
fig, (ax) = plt.subplots(1, 1, figsize=(13,13))
for item in nma_igs:
    na = []
    for pressure in relp:
        na = np.append(na, pressure/(1-pressure) * (item*Ca)/(1+(Ca-1)*pressure))    
    nb = n - na
    nb_bet = []
    for x, y in zip(relp, nb):
        nb_bet = np.append(nb_bet, 1 / (y * ((1/x) - 1)))
    ax.plot(relp, nb_bet, marker='o', linewidth=1, label = str(item))
    ax.legend(loc='lower right', framealpha=1)
plt.show()

#plot as initial guess moves away from nm_a value, starting at nm_a and increasing
nma_igs = np.linspace(nma, nma * 10, 10)
fig2, (ax2) = plt.subplots(1, 1, figsize=(13,13))
for item in nma_igs:
    na = []
    for pressure in relp:
        na = np.append(na, pressure/(1-pressure) * (item*Ca)/(1+(Ca-1)*pressure))    
    nb = n - na
    nb_bet = []
    for x, y in zip(relp, nb):
        nb_bet = np.append(nb_bet, 1 / (y * ((1/x) - 1)))
    ax2.plot(relp, nb_bet, marker='o', linewidth=1, label = str(item))   
    ax2.legend(loc='lower right', framealpha=1)
plt.show()