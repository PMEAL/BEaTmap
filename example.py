import beatmap as bt
import numpy as np

# import the data from a .cvs file using the import_data() function
# data may be imported from lists using import_list_data()
file_name, data, adsorbate, a_o = bt.io.import_data()

# experimental_data_plot() may be used to visualize the isotherm
bt.vis.experimental_data_plot(data, file_name)

# the bet() function applies BET theory to the isotherm and returns arrays of
# surface area, monolayer amounts, bet constant, error,
# and linear regression values
ssa, nm, c, err, linreg = bt.core.bet(data, a_o)

# the combine_masks() function is used to create a mask that may be applied to
# the arrays (specific surface area, bet constant, etc)
# by default all checks are applied
mask = bt.core.rouq_mask(data, nm, linreg, check1=False, check2=False, check3=False,
                  check4=False, check5=True, points=3)

# applying the mask to the arrays, creating numpy mask objects
masked_ssa = np.ma.array(ssa, mask=mask)
masked_nm = np.ma.array(nm, mask=mask)
masked_c = np.ma.array(c, mask=mask)
masked_err = np.ma.array(err, mask=mask)

# heatmaps, plots, and tables created from the masked arrays allow the
# valid results of BET theory to be visualized

# ssa_heatmap() creates a heatmap of specific surface area values
bt.vis.ssa_heatmap(data, masked_ssa, file_name)

# err_heatmap() creates a heatmap of error values
bt.vis.err_heatmap(data, masked_err, file_name)

# bet_combo_plot() compares the two unmasked relative pressure ranges
# that have the lowest and highest error (best and worst agreement
# between experimental data and theoretical values)
bt.vis.bet_combo_plot(data, masked_c, masked_err, file_name)

# bet_iso_combo_plot() also compares relative pressure ranges with the
# highest and lowest error. The BET equation is visualized in the 'decomposed'
# form, the y - axis is normalized, n/nm. The point where the experimental data
# crossed n/nm = 1 shows where in the relative pressure range monolayer coverage occurs
bt.vis.bet_iso_combo_plot(data, masked_ssa, masked_nm, masked_c, masked_err, file_name)

# ascii_tables() creates two tables summarizing the valid results of applying BET theory
bt.vis.ascii_tables(data, masked_ssa, masked_c, masked_err)

# export_raw_data() creates a .csv file of the isotherm data
bt.io.export_raw_data(data, file_name)

# export_processed_data() creates a .csv file of data, bet results,
# linear regression data, and rouq checks
bt.io.export_processed_data(data, ssa, nm, c, linreg, file_name, points=5)
