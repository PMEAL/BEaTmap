#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:59:27 2019

@author: ellsworthbell
"""
import numpy as np
import dataio
import bet
import figures
import settables

file, df, adsorbate, a_o = bt.dataio.import_data()
print(df)

sa, c, nm, err, linreg = bet.bet(df, a_o)
single_sa, single_nm = bet.single_point_bet(df, a_o)

diff = np.zeros((len(df), len(df)))
diff = sa - single_sa
theta = bet.theta(df, nm)

mask = bet.combine_masks(df, linreg, nm, check1 = True, check2 = True, check3 = True, check4 = True, check5 = True, points = 5)

masked_ssa = np.multiply(sa, mask)
masked_c = np.multiply(c, mask)
masked_nm = np.multiply(nm, mask)
masked_error = np.multiply(err, mask)
masked_theta = np.multiply(theta, mask)
#masked_diff = np.multiply(diff, mask)

#print(nm)

figures.ssa_heatmap(df, masked_ssa, file)
#figures.experimental_data_plot(df, file)
figures.err_heatmap(df, masked_error, file)
settables.ascii_tables(masked_c, masked_ssa, masked_error, df)
#figures.bet_iso_combo_plot(masked_c, masked_error, masked_ssa, masked_nm, df, file)
figures.experimental_data_plot(df, file)
figures.bet_combo_plot(masked_c, masked_error, df, file)
figures.bet_iso_combo_plot(masked_c, masked_error, masked_ssa, masked_nm, df, file)
dataio.export_processed_data(df, sa, c, nm, linreg, file)
#dataio.export_raw_data(df, file)
