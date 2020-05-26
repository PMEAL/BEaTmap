import beatmap as bt

"""
import the data from a .cvs file using the import_data() function
data may be imported from lists using import_list_data()
"""
bet_results = bt.io.import_data()

"""
relp = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.125,
0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6,
0.7, 0.8, 0.9]
n = [0, 0.00055797, 0.0006805, 0.00076186, 0.00082042, 0.00086352,
0.00089899, 0.00093262, 0.00095784, 0.00098287, 0.00100306, 0.0010508,
0.00108762, 0.00111806, 0.00114453, 0.00116956, 0.00119198, 0.00121517,
0.00123701, 0.00127731, 0.00132157, 0.00136776, 0.00141743, 0.00147319,
0.00153784, 0.0017082, 0.00198351, 0.00256767]

bet_results  = bt.io.import_list_data(relp, n)
"""
"""
experimental_data_plot() may be used to visualize the isotherm
"""
bt.vis.experimental_data_plot(bet_results, True)

"""
the bet() function applies BET theory to the isotherm and returns arrays of
surface area, monolayer amounts, bet constant, error,
and linear regression values
"""
bet_results = bt.core.bet(bet_results)

"""
the combine_masks() function is used to create a mask that may be applied to
the arrays (specific surface area, bet constant, etc)
by default all checks are applied
"""
rouq_mask = bt.core.rouq_mask(bet_results, check1=True, check2=True,
                              check3=True, check4=True, check5=True, points=5)

ssa_ans = bt.core.ssa_answer(bet_results, rouq_mask, criterion='points')

"""
heatmaps, plots, and tables created from the masked arrays allow the
valid results of BET theory to be visualized by applying mask
ssa_heatmap() creates a heatmap of specific surface area values
"""
bt.vis.ssa_heatmap(bet_results, rouq_mask)

"""
err_heatmap() creates a heatmap of error values
"""
bt.vis.err_heatmap(bet_results, rouq_mask)

"""
bet_combo_plot() compares the two unmasked relative pressure ranges
that have the lowest and highest error (best and worst agreement
between experimental data and theoretical values)
"""
bt.vis.bet_combo_plot(bet_results, rouq_mask)

"""
bet_iso_combo_plot() also compares relative pressure ranges with the
highest and lowest error. The BET equation is visualized in the 'decomposed'
form, the y - axis is normalized, n/nm. The point where the experimental data
crosses n/nm = 1 shows where monolayer coverage occurs
"""
bt.vis.bet_iso_combo_plot(bet_results, rouq_mask)

"""
ascii_tables() creates two tables summarizing
the valid results of applying BET theory
"""
bt.vis.ascii_tables(bet_results, rouq_mask)

"""
export_raw_data() creates a .csv file of the isotherm data
"""
bt.io.export_processed_data(bet_results, points=5)

ssa_table, c_table, ssa_std, c_std = bt.vis.dataframe_tables(bet_results, rouq_mask)

