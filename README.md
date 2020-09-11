[![image](https://github.com/PMEAL/beatmap/workflows/Ubuntu/badge.svg)](https://github.com/PMEAL/beatmap/actions)
[![image](https://github.com/PMEAL/beatmap/workflows/macOS/badge.svg)](https://github.com/PMEAL/beatmap/actions)
[![image](https://github.com/PMEAL/beatmap/workflows/Windows/badge.svg)](https://github.com/PMEAL/beatmap/actions)<br/>
[![codecov](https://codecov.io/gh/PMEAL/beatmap/branch/master/graph/badge.svg?token=3ZBPKC3QXW)](https://codecov.io/gh/PMEAL/beatmap)
[![image](https://img.shields.io/badge/ReadTheDocs-GO-blue.svg)](http://beatmap.readthedocs.io/en/master/)
[![image](https://img.shields.io/pypi/v/beatmap.svg)](https://pypi.python.org/pypi/beatmap/)
[![image](https://img.shields.io/badge/DOI-10.21105/joss.01296-blue.svg)](https://doi.org/10.21105/joss.01296)

-----

**Cite as:**

> *Gostick J, Khan ZA, Tranter TG, Kok MDR, Agnaou M, Sadeghi MA, Jervis
> R.* **PoreSpy: A Python Toolkit for Quantitative Analysis of Porous Media
> Images.** Journal of Open Source Software, 2019.
> [doi:10.21105/joss.01296](https://doi.org/10.21105/joss.01296)

# What is BEaTmap?

Obtaining surface area of a porous sample from the interpretation of gas
adsorption isotherms is very widely done using the theory developed by Brunauer,
Emmett, and Teller in the 1950s.  The BET (or BEaT) theory is so commonly place
that the acronym has is synonymous with surface area.

The BET theory was derived with several assumptions, and these must be met for
the predicted surface area to be valid.

Rouquerol et al have put forth criteria to evaluate whether isothermal adsoprtion data meets the assumptions of BET analysis. Applying these criteria to all relative pressure ranges of an isotherm allows one to eliminate relative pressure ranges that do not adhere to BET theory. Visualizing the results of BET analysis as a heatmap where "invalid" relative pressure ranges are masked provides a quick and comprehensive representation of BET results for an isotherm.

BEaTmap was developed as a conceptulization and vizualization tool for BET analysis utilizing the "Rouquerol criteria".

# Capabilities

BEaTmap consists of the following modules:

  - `core`: Functions that perform BET analysis, evaluate Rouquerol critieria, and provide a single specific surface area answer
  - `io`: Functions for import data from .csv files or lists, and exporting processed data to .xlsx files
  - `utils`: Various small functions used in other BEaTmap modules
  - `vis`: Functions to create heatmaps, BET plots, isotherm plots, tables of BET analysis results, etc

# Installation

BEaTmap depends heavily on the Scipy Stack. The best way to get a fully
functional environment is the [Anaconda
distribution](https://www.anaconda.com/download/). Be sure to get the
**Python 3.6+ version**.

Once you've installed *Conda*, you can then install BEaTmap. It is
available on the [Python Package
Index](https://pypi.org/project/beatmap/) and can be installed by typing
the following at the *conda* prompt:

    pip install beatmap

On Windows, you should have a shortcut to the "anaconda prompt" in the
Anaconda program group in the start menu. This will open a Windows
command console with access to the Python features added by *Conda*,
such as installing things via `pip`.

On Mac or Linux, you need to open a normal terminal window, then type
`source activate {env}` where you replace `{env}` with the name of the
environment you want to install BEaTmap. If you don't know what this
means, then use `source activate root`, which will install BEaTmap in
the root environment which is the default.

If you think you may be interested in contributing to BEaTmap and wish
to both *use* and *edit* the source code, then you should clone the
[repository](https://github.com/PMEAL/beatmap) to your local machine,
and install it using the following PIP command:

    pip install -e "C:\path\to\the\local\files\"

For information about contributing, refer to the [contributors
guide](https://github.com/PMEAL/beatmap/blob/master/CONTRIBUTING.md)

# Examples

The following code snippets illustrate how to import data, perform BET analysis, evaluate Rouquerol criteria, and produce figures in BEaTmap. A set of examples
is included in this repo, and can be [browsed
here](https://github.com/PMEAL/beatmap/tree/master/examples).

## Using the BEaTmap 'envelope function'

An "envelope" function, that will import data, perform BET analysis, evaluate the Rouquerol criteria, and produce all figures for the user has been built. The file path, information about the data (later used for naming exported files), and the adsorbate cross sectional area in square Angstrom need to be specified. It allows the user to access much of BEaTmap's functionality in one line.

```python
import beatmap as bt
import matplotlib.pylot as plt
bt.run_beatmap(file='vulcan_chex.csv',
               info='chex on vulcan',
               a_o=39)
```

## Loading a dataset from .csv

The `import_data` function can be used to import a isotherm data from a .csv file where the first column is relative pressure and the second column is the amount adsorbed.

The function returns a named tuple where the first entry is a dataframe of the imported isotherm, and the 2nd-4th fields are the cross sectional area of the adsorbate, information about the data, and file path, respectively. Indexing of named tuple elements is in order of priority, data used by other function are given priority.


``` python
isotherm_data = bt.io.import_data(file='vulcan_chex.csv',
                                  info='chex on vulcan',
                                  a_o=39)
```

## Performing BET analysis

BET analysis is performed on every relative pressure range within the isotherm data by the `bet` function. The function accepts the dataframe of isotherm data, cross sectional area of the adsorbate, and information about the data (information stored in the named tuple created by the import_data function). Rather than pass individual parameters, this function can accept *isotherm_data (where isotherm_data is a named tuple output by a data import function).

The function returns a named tuple containing the results of BET analysis as well as information about the isotherm (raw data, file path, etc). Again, the indexing of named tuple elements is in order of priority, data used by other function are given priority.

```python
bet_results = bt.core.bet(isotherm_data.iso_df,
                          isotherm_data.a_o,
                          isotherm_data.info)
```

## Evaluating the Rouquerol criteria

The Rouquerol criteria, used to mask out results of BET analysis for invalid relative pressure ranges are evaluated by the `rouq_mask` function. Rather than pass individual parameters, this function can accept `*bet_results` (where bet_results is a named tuple output by the bet function).

The function returns a named tuple containing a numpy mask array, and individual arrays corresponding to the results of each criterion.


```python
mask_results = bt.core.rouq_mask(bet_results.intercept,
                                 bet_results.iso_df,
                                 bet_results.nm,
                                 bet_results.slope)
```

## Creating a specific surface area heatmap and other figures

The `bet_results` and `mask_results` can used to create a heatmap of specific surface area values for each relative pressure range. This visualization concept is the central idea of BEaTmap. The `ssa_heatmap` function requires the named tuples produced by the bet function and the rouq_mask function.

Other figures, such as a plot of experimental data and the model isotherm can be created in this manner. See the documentation for a full summary of figures.

```python
bt.vis.ssa_heatmap(bet_results, mask_results)
bt.vis.iso_combo_plot(bet_results, mask_results, save_file=True)
```

<p align="center">
	<img src="https://user-images.githubusercontent.com/14086031/92957429-83827e00-f436-11ea-9be7-cda8aacd4569.png" width="100%"></img>
</p>

## Exporting .xlsx files of results

It might be desireable to have a spreadsheet that contains all results of BET analysis and the Rouquerol criteria. This sheet can be created and saved in the parent directory with the `export_processed_data` function.

```python
bt.io.export_processed_data(bet_results)
```

