import beatmap as bt
import numpy as np

file_name, data, adsorbate, a_o = bt.io.import_data()

bt.vis.experimental_data_plot(data, file_name)

sa, c, nm, err, linreg = bt.core.bet(data, a_o)

mask = bt.core.combine_masks(data, linreg, nm, check1=False, check2=False, check3=False,
                  check4=False, check5=False, points=5)

masked_sa = np.ma.array(sa, mask=mask)
masked_c = np.ma.array(c, mask=mask)
masked_err = np.ma.array(err, mask=mask)
masked_nm = np.ma.array(nm, mask=mask)

bt.vis.ssa_heatmap(data, masked_sa, file_name)
bt.vis.err_heatmap(data, masked_err, file_name)
bt.vis.bet_combo_plot(masked_c, masked_err, data, file_name)
bt.vis.bet_iso_combo_plot(masked_c, masked_err, masked_sa, masked_nm, data, file_name)
bt.vis.ascii_tables(masked_c, masked_sa, masked_err, data)
