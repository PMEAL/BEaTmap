# Basic Usage

An "envelope" function, that will import data, perform BET analysis, evaluate the Rouquerol criteria, and produce all figures for the user has been built. The file path, information about the data (later used for naming exported files), and the adsorbate cross sectional area in square Angstrom need to be specified. It allows the user to access much of BEaTmap's functionality in one line.

```python
import beatmap as bt
import matplotlib.pylot as plt

# Define path to the Vulcan isotherm dataset
fpath = bt.utils.get_datasets_path() / 'vulcan_chex.csv'

rouq_criteria = {
    "enforce_y_intercept_positive": True,
    "enforce_pressure_increasing": True,
    "enforce_absorbed_amount": True,
    "enforce_relative_pressure": True,
    "enforce_enough_datapoints": True,
    "min_num_points": 5
}

aux_params = {
    "save_figures": True,
    "export_data": False,
    "ssa_gradient": "Greens",
    "err_gradient": "Greys"
}

results = bt.run_beatmap(
    file=fpath,
    info="chex on vulcan"
    a_o=39,
    ssa_criterion="error",
    **rouq_criteria,
    **aux_params
)
```
