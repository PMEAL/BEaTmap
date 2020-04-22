import beatmap as bt
import numpy as np

file, data, adsorbate, a_o = bt.io.import_data()
sa, c, nm, err, linreg = bt.core.bet(data, a_o)
mask = bt.core.combine_masks(data, linreg, nm)
masked_sa = np.multiply(sa, mask)
masked_c = np.multiply(c, mask)
masked_err = np.multiply(err, mask)
bt.vis.ssa_heatmap(data, masked_sa, file)
bt.vis.ascii_tables(masked_c, masked_sa, masked_err, data)
