import beatmap as bt
import numpy as np
'''
file, data, adsorbate, a_o = bt.io.import_data()
sa, c, nm, err, linreg = bt.core.bet(data, a_o)
mask = bt.core.combine_masks(data, linreg, nm)
masked_sa = np.multiply(sa, mask)
bt.vis.ssa_heatmap(data, masked_sa, file)
'''

#model isotherm, nma = nmb = .002, Ca = 100, Cb = 2
relp = [0.00000001, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 0.9] 
n = [2.04*10**-9, 0.001055181, 0.001449707, 0.001678185, 0.001840364, 0.00196963, 0.002442776, 0.002840569, 0.003237179, 0.003655663, 0.004110678, 0.004616264, 0.005188834, 0.005849509, 0.006627063, 0.007562498, 0.008716887, 0.012128413, 0.018863951, 0.038925171]

file, data, adsorbate, a_o = bt.io.import_list_data(relp, n)

Ca = 100
nma_ig = .01

na = relp/(1-relp) * (nma_ig*Ca)/(1+(Ca-1)*relp)