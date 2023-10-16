# Advanced Usage

Alternatively, you can use the individual functions in BEaTmap to perform BET analysis and evaluate the Rouquerol criteria. This allows the user to access more of BEaTmap's functionality, and to customize the analysis.

## Import the dataset

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

## BET analysis

BET analysis is performed on every relative pressure range within the isotherm data by the `bet` function. The function accepts the dataframe of isotherm data, cross sectional area of the adsorbate, and information about the data (information stored in the named tuple created by the import_data function). Rather than pass individual parameters, this function can accept *isotherm_data (where isotherm_data is a named tuple output by a data import function).

The function returns a named tuple containing the results of BET analysis as well as information about the isotherm (raw data, file path, etc). Again, the indexing of named tuple elements is in order of priority, data used by other function are given priority.

```python
bet_results = bt.core.bet(
    iso_df=isotherm_data.iso_df,
    a_o=isotherm_data.a_o,
    info=isotherm_data.info
)
```

## Rouquerol criteria

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

## Supplementary analysis

The `bet_results` and `mask_results` can used to create a heatmap of specific surface area values for each relative pressure range. This visualization concept is the central idea of BEaTmap. The `ssa_heatmap` function requires the named tuples produced by the bet function and the rouq_mask function.

Other figures, such as a plot of experimental data and the model isotherm can be created in this manner. See the documentation for a full summary of figures.

```python
bt.vis.ssa_heatmap(bet_results, mask_results)
bt.vis.iso_combo_plot(bet_results, mask_results, save_file=True)
```

## Export the results

It might be desireable to have a spreadsheet that contains all results of BET analysis and the Rouquerol criteria. This sheet can be created and saved in the parent directory with the `export_processed_data` function.

```python
bt.io.export_processed_data(bet_results)
```
