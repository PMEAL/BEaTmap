<p align="center">
  <img src="https://github.com/PMEAL/beatmap/raw/main/docs/source/_static/logo-light-mode.png" width="50%"></img>
</p>

# What is BEaTmap?

[![image](https://github.com/PMEAL/beatmap/actions/workflows/tests.yml/badge.svg)](https://github.com/PMEAL/beatmap/actions)
[![codecov](https://codecov.io/gh/PMEAL/beatmap/branch/main/graph/badge.svg?token=3ZBPKC3QXW)](https://codecov.io/gh/PMEAL/beatmap)
[![image](https://img.shields.io/pypi/v/beatmap.svg)](https://pypi.python.org/pypi/beatmap/)

Obtaining surface area of a porous sample from the interpretation of gas adsorption isotherms is very widely done using the theory developed by Brunauer, Emmett, and Teller in the 1950s. The BET (or BEaT) theory is so commonly place
that the acronym has is synonymous with surface area. The BET theory was derived with several assumptions, and these must be met for the predicted surface area to be valid.

Rouquerol et al have put forth criteria to evaluate whether isothermal adsoprtion data meets the assumptions of BET analysis. Applying these criteria to all relative pressure ranges of an isotherm allows one to eliminate relative pressure ranges that do not adhere to BET theory. Visualizing the results of BET analysis as a heatmap where "invalid" relative pressure ranges are masked provides a quick and comprehensive representation of BET results for an isotherm.

BEaTmap was developed as a conceptulization and vizualization tool for BET analysis utilizing the "Rouquerol criteria".

## Capabilities

BEaTmap consists of the following modules:

  - `core`: Functions that perform BET analysis, evaluate Rouquerol critieria, and provide a single specific surface area answer
  - `io`: Functions for import data from .csv files or lists, and exporting processed data to .xlsx files
  - `utils`: Various small functions used in other BEaTmap modules
  - `vis`: Functions to create heatmaps, BET plots, isotherm plots, tables of BET analysis results, etc
  
## Try It Live

We have created a web-based GUI for BEaTmap using Streamlit.  This app is hosted on the Streamlit servers and is available [here](https://beatmap.streamlit.app). If the app is not used for a certain period then Streamlit will hibernate it then wake it up on request, so it may take a few moments to load. The app includes a link to some sample data which you can use to explore the interface. Enjoy.

## Installation

BEaTmap depends heavily on the Scipy Stack. The best way to get a fully functional environment is the [Anaconda distribution](https://www.anaconda.com/download/). Be sure to get the **Python 3.9+ version**.

Once you've installed `conda`, you can then install BEaTmap. It is available on the [Python Package Index](https://pypi.org/project/beatmap/) and can be installed by typing the following at the *conda* prompt:

    pip install beatmap

On Windows, you should have a shortcut to the "Anaconda Prompt" in the start menu. This will open a Windows command console with access to the Python features added by `conda`, such as installing things via `pip`.

On Mac or Linux, you need to open a normal terminal window, then type `source activate {env}` where you replace `{env}` with the name of the environment you want to install BEaTmap. If you don't know what this means, then use `source activate base`, which will install BEaTmap in the base environment which is the default.

If you think you may be interested in contributing to BEaTmap and wish to both *use* and *edit* the source code, then you should clone the [repository](https://github.com/PMEAL/beatmap) to your local machine, and install it using the following `pip` command:

    pip install -e path/to/beatmap/root/folder

For information about contributing, refer to the [contributors guide](https://github.com/PMEAL/beatmap/blob/master/CONTRIBUTING.md).

## Examples

The following code snippets illustrate how to import data, perform BET analysis, evaluate Rouquerol criteria, and produce figures in BEaTmap. An example is included in this repo, and can be [browsed here](https://github.com/PMEAL/beatmap/blob/main/examples/BEaTmap_example.ipynb).

## Automated BET analysis

An "envelope" function, that will import data, perform BET analysis, evaluate the Rouquerol criteria, and produce all figures for the user has been built. The file path, information about the data (later used for naming exported files), and the adsorbate cross sectional area in square Angstrom need to be specified. It allows the user to access much of BEaTmap's functionality in one line.

```python
import beatmap as bt
import matplotlib.pylot as plt

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

## Manual BET analysis

Alternatively, you can use the individual functions in BEaTmap to perform BET analysis and evaluate the Rouquerol criteria. This allows the user to access more of BEaTmap's functionality, and to customize the analysis.
### Import the dataset

The `import_data` function can be used to import a isotherm data from a .csv file where the first column is relative pressure and the second column is the amount adsorbed.

The function returns a named tuple where the first entry is a dataframe of the imported isotherm, and the 2nd-4th fields are the cross sectional area of the adsorbate, information about the data, and file path, respectively. Indexing of named tuple elements is in order of priority, data used by other function are given priority.


``` python
import beatmap as bt
import matplotlib.pylot as plt

isotherm_data = bt.io.load_vulcan_dataset()

# Alternatively, you can manually import the CSV data as shown below
# fpath = bt.utils.get_datasets_path() / 'vulcan_chex.csv'
# isotherm_data = bt.io.import_data(file=fpath, info='vulcan-chex', a_o=39)
```

### BET analysis

BET analysis is performed on every relative pressure range within the isotherm data by the `bet` function. The function accepts the dataframe of isotherm data, cross sectional area of the adsorbate, and information about the data (information stored in the named tuple created by the import_data function). Rather than pass individual parameters, this function can accept *isotherm_data (where isotherm_data is a named tuple output by a data import function).

The function returns a named tuple containing the results of BET analysis as well as information about the isotherm (raw data, file path, etc). Again, the indexing of named tuple elements is in order of priority, data used by other function are given priority.

```python
bet_results = bt.core.bet(
    iso_df=isotherm_data.iso_df,
    a_o=isotherm_data.a_o,
    info=isotherm_data.info
)
```

### Rouquerol criteria

The Rouquerol criteria, used to mask out results of BET analysis for invalid relative pressure ranges are evaluated by the `rouq_mask` function. Rather than pass individual parameters, this function can accept `*bet_results` (where bet_results is a named tuple output by the bet function).

The function returns a named tuple containing a numpy mask array, and individual arrays corresponding to the results of each criterion.


```python
mask_results = bt.core.rouq_mask(
    intercept=bet_results.intercept,
    iso_df=bet_results.iso_df,
    nm=bet_results.nm,
    slope=bet_results.slope,
    enforce_y_intercept_positive=True,
    enforce_pressure_increasing=True,
    enforce_absorbed_amount=True,
    enforce_relative_pressure=True,
    enforce_enough_datapoints=True,
    min_num_points=5
)
```

### Supplementary analysis

The `bet_results` and `mask_results` can used to create a heatmap of specific surface area values for each relative pressure range. This visualization concept is the central idea of BEaTmap. The `ssa_heatmap` function requires the named tuples produced by the bet function and the rouq_mask function.

Other figures, such as a plot of experimental data and the model isotherm can be created in this manner. See the documentation for a full summary of figures.

```python
bt.vis.ssa_heatmap(bet_results, mask_results)
bt.vis.iso_combo_plot(bet_results, mask_results, save_file=True)
```

![ssa_heatmap-combo_plot](https://github.com/PMEAL/BEaTmap/assets/14086031/fee31e9a-ffac-4b5d-ad3d-685bfe0ab99e)

### Export the results

It might be desireable to have a spreadsheet that contains all results of BET analysis and the Rouquerol criteria. This sheet can be created and saved in the parent directory with the `export_processed_data` function.

```python
bt.io.export_processed_data(bet_results)
```
