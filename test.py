import beatmap as bt
import numpy as np

file_name, data, adsorbate, a_o = bt.io.import_data()

bet_results = bt.core.bet(data, a_o)

mask = bt.core.rouq_mask(data, bet_results, check1=False, check2=False,
                         check3=False, check4=False, check5=False, points=3)

print(mask)

bt.vis.ssa_heatmap(data, bet_results, mask, file_name)
