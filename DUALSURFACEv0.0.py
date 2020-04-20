#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:16:10 2019

@author: ellsworthbell
"""
import beatmap as bt
import numpy as np
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
relp = [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9] 
n = [0.001055181, 0.001449707, 0.001678185, 0.001840364, 0.00196963, 0.002442776, 0.002840569, 0.003237179, 0.003655663, 0.004110678, 0.004616264, 0.005188834, 0.005849509, 0.006627063, 0.007562498, 0.008716887, 0.012128413, 0.018863951, 0.038925171]

file, data, adsorbate, a_o = bt.io.import_list_data(relp, n)

Ca = 100

#plot as initial guess approaches nm_a value from below
nma_igs = np.linspace(.001, .0020, 10)
fig, (ax) = plt.subplots(1, 1, figsize=(13,13))
for item in nma_igs:
    na = []
    for pressure in relp:
        na = np.append(na, pressure/(1-pressure) * (item*Ca)/(1+(Ca-1)*pressure))    
    nb = n - na
    nb_bet = []
    for x, y in zip(relp, nb):
        nb_bet = np.append(nb_bet, 1 / (y * ((1/x) - 1)))
    ax.plot(relp, nb_bet, marker='o', linewidth=1)   
plt.show()

#plot as initial guess moves away from nm_a value, starting at nm_a and increasing
nma_igs = np.linspace(.002, .0030, 10)
fig2, (ax2) = plt.subplots(1, 1, figsize=(13,13))
for item in nma_igs:
    na = []
    for pressure in relp:
        na = np.append(na, pressure/(1-pressure) * (item*Ca)/(1+(Ca-1)*pressure))    
    nb = n - na
    nb_bet = []
    for x, y in zip(relp, nb):
        nb_bet = np.append(nb_bet, 1 / (y * ((1/x) - 1)))
    ax2.plot(relp, nb_bet, marker='o', linewidth=1)   
plt.show()