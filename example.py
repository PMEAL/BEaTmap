import beatmap as bt

# """
# import the data from a .cvs file using the import_data() function
# data may be imported from lists using import_list_data()
# """

# isotherm_data = bt.io.import_data()

# """
# relp = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.125,
# 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6,
# 0.7, 0.8, 0.9]
# n = [0, 0.00055797, 0.0006805, 0.00076186, 0.00082042, 0.00086352,
# 0.00089899, 0.00093262, 0.00095784, 0.00098287, 0.00100306, 0.0010508,
# 0.00108762, 0.00111806, 0.00114453, 0.00116956, 0.00119198, 0.00121517,
# 0.00123701, 0.00127731, 0.00132157, 0.00136776, 0.00141743, 0.00147319,
# 0.00153784, 0.0017082, 0.00198351, 0.00256767]

# bet_results  = bt.io.import_list_data(relp, n)
# """
# """
# experimental_data_plot() may be used to visualize the isotherm
# """
# bt.vis.experimental_data_plot(isotherm_data, save_file=True)

# """
# the bet() function applies BET theory to the isotherm and returns arrays of
# surface area, monolayer amounts, bet constant, error,
# and linear regression values
# """

# bet_results = bt.core.bet(isotherm_data.iso_df, isotherm_data.a_o,
#                           isotherm_data.info)

# """
# alternative parameter declaration:
# bet_results = bt.core.bet(*isotherm_data)
# """

# """
# the combine_masks() function is used to create a mask that may be applied to
# the arrays (specific surface area, bet constant, etc)
# by default all checks are applied
# """

# mask_results = bt.core.rouq_mask(bet_results.intercept, bet_results.iso_df,
#                                  bet_results.nm, bet_results.slope,
#                                  check1=True, check2=True, check3=True,
#                                  check4=True, check5=True, points=5)

# """
# alternative parameter declaration:
# mask_results = bt.core.rouq_mask(*bet_results, check1=True, check2=True,
#                                  check3=True, check4=True, check5=True,
#                                  points=5)
# """

# ssa_ans = bt.core.ssa_answer(bet_results, mask_results, criterion='points')

# """
# heatmaps, plots, and tables created from the masked arrays allow the
# valid results of BET theory to be visualized by applying mask
# ssa_heatmap() creates a heatmap of specific surface area values
# """

# bt.vis.ssa_heatmap(bet_results, mask_results)

# """
# err_heatmap() creates a heatmap of error values
# """

# bt.vis.err_heatmap(bet_results, mask_results)

# """
# bet_combo_plot() compares the two unmasked relative pressure ranges
# that have the lowest and highest error (best and worst agreement
# between experimental data and theoretical values)
# """

# bt.vis.bet_combo_plot(bet_results, mask_results)

# """
# bet_iso_combo_plot() also compares relative pressure ranges with the
# highest and lowest error. The BET equation is visualized in the 'decomposed'
# form, the y - axis is normalized, n/nm. The point where the experimental data
# crosses n/nm = 1 shows where monolayer coverage occurs
# """

# bt.vis.iso_combo_plot(bet_results, mask_results)

# """
# ascii_tables() creates two tables summarizing
# the valid results of applying BET theory
# """

# bt.vis.ascii_tables(bet_results, mask_results)

# """
# export_raw_data() creates a .csv file of the isotherm data
# """

# bt.io.export_processed_data(bet_results, points=5)

# ssa_table, c_table, ssa_std, c_std = \
#     bt.vis.dataframe_tables(bet_results, mask_results)


def run_beatmap(file=None, info=None, a_o=None, check1=True, check2=True,
                check3=True, check4=True, check5=True, points=5,
                save_figures=True, export_data=False, ssa_criterion='error',
                ssa_gradient='Greens', err_gradient='Greys'):
    """A single function that executes all necessary BEaTmap algorithims.

    This function is built to be as user friendly as possible. The file
    name/path of the isotherm data, information about the isotherm, and the
    cross sectional surface area of the adsorbate can be passed using the
    file, info, and a_o parameters respectively. Or, if left empty, the user
    be prompted to input them.

    eg. ``run_beatmap('myfile.csv', 'nitrogen on carbon', 16.2)`` or
    ``run_beatmap()`` will execute the function. In the later case the user
    will provide the parameters passed in the former through promts in their
    console.

    Additional parameters to set which of the Roquerol criteria are applied,
    the minimum number of data points per valid relative pressure range,
    the criteria used to select a single specific surface area, and more, are
    defined and set to reasonable default values.

    Parameters
    ----------
    file : string
        File name (if file is in parent directory) or file path.

    info : string
        Adsorbate-adsorbent information.

    a_o : float
        Cross sectional area of adsorbate, in square Angstrom.

    check1 : boolean
        If check1 is True any relative pressure ranges with a negative y
        intercept are considered invalid.

    check2 : boolean
        If check2 is True any relative pressure ranges where n(p-po) is
        decreasing are considered invalid.

    check3 : boolean
        If check3 is True any relative pressure ranges where the monolayer
        amount falls outside of the relative pressure range are considered
        invalid.

    check4 : boolean
        If check4 is True any relative pressure range where there is
        disagreement of more than 10% between the actual relative pressure
        where monolayer coverage occurs and the relative pressure where
        monolayer coverage occurs on the theoretical isotherm are considered
        invalid.

    check5 : boolean
        If check5 is True relative pressure ranges that contain fewer points
        than specified by the user are considered invalid.

    points : interger
        The minimum number of points for a valid relative pressure range.

    save_figures : boolean
        If save_figures is True any figures created by this function will be
        saved as .png files in the parent directory.

    export_data : boolean
        If export data is True .csv files of the isotherm data and the BEaTmap
        results will be created and saved in the parent directory.

    ssa_criterion : string
        Used to set which criterion is used to provide a single specific
        surface area value. 'error' will output the valid ssa answer with the
        lowest error, 'points' will output the ssa answer with the most
        datapoints.

    ssa_gradient : string
        Color gradient for heatmap, must be a vaild color gradient name
        in the seaborn package.

    err_gradient : string
        Color gradient for heatmap, must be a vaild color gradient name
        in the seaborn package, default is grey.

    Returns
    -------
    """

    if file is None:
        file = input("Enter file name/path:")
    if info is None:
        info = input("Enter adsorbate-adsorbent information (this will be \
incorporated into file names):")
    if a_o is None:
        a_o = input("Enter cross sectional area of adsorbate in \
square Angstrom:")
        try:
            a_o = float(a_o)
        except ValueError:
            print('The ao provided is not numeric.')
            a_o = input("Try again, enter the cross sectional area of \
adsorbate in square Angstrom: ")
            a_o = float(a_o)

# run_beatmap_import_data imports isotherm data from a .csv file and returns
# the results in the isotherm_data namedtuple
    isotherm_data = bt.io.run_beatmap_import_data(file, info, a_o)

    bt.vis.experimental_data_plot(isotherm_data, save_file=True)

# bet_results uses isotherm_data, applies BET analysis and returns the results
# in the bet_results namedtuple

    bet_results = bt.core.bet(isotherm_data.iso_df, isotherm_data.a_o,
                              isotherm_data.info)

# mask_results uses isotherm_data and bet_results, applies the roquerol
# criteria specified by the user, and returns the results in the
# mask_results named tuple

    mask_results = bt.core.rouq_mask(bet_results.intercept, bet_results.iso_df,
                                     bet_results.nm, bet_results.slope,
                                     check1=True, check2=True, check3=True,
                                     check4=True, check5=True, points=5)

# mask_results are used to highlight the valid bet_results in the following
# functions

    ssa_ans = bt.core.ssa_answer(bet_results, mask_results, ssa_criterion)

    bt.vis.ssa_heatmap(bet_results, mask_results, save_figures)
    bt.vis.err_heatmap(bet_results, mask_results, save_figures)
    bt.vis.bet_combo_plot(bet_results, mask_results, save_figures)
    bt.vis.iso_combo_plot(bet_results, mask_results, save_figures)
    bt.vis.ascii_tables(bet_results, mask_results)

    if export_data is True:
        bt.io.export_raw_data(isotherm_data)
        bt.io.export_processed_data(bet_results, points)

    return bet_results
