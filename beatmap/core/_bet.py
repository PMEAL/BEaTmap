import numpy as np
import scipy as sp
import logging
from beatmap import io as io
from beatmap import utils as util
from beatmap import vis as figs
from collections import namedtuple


__all__ = [
    "bet",
    "single_point_bet",
    "check_y_intercept_positive",
    "check_pressure_increasing",
    "check_absorbed_amount",
    "check_pressure_consistency",
    "check_enough_datapoints",
    "rouq_mask",
    "ssa_answer",
    "run_beatmap",
]


def bet(iso_df, a_o, info, *args):
    """
    Performs BET analysis on isotherm data for all relative pressure ranges.

    This function performs BET analysis of any relative pressure range where
    the starting relative pressure is less than the ending relative pressure.

    Results of the analysis are written to arrays, the indexes of the arrays
    correspond to the starting and ending relative pressure.

    eg the specific surface area value with the indicies [3,9] is the specific
    surface area for the relative pressure range that begins with the 4th data
    point and ends with the 10th.

    Arrays of results are stored in the bet_results named tuple.

    Indexing of named tuple elements is in order of priority, data used by
    other function are given priority.

    Rather than pass individual parameters, this function can accept
    ``isotherm_data`` (where ``isotherm_data`` is a named tuple output by
    a data import function).

    Parameters
    ----------
    iso_df: DataFrame
        Isotherm data, output by a data import function.
    a_o : float
        Cross sectional area of adsorbate, in square Angstrom, output by a
        data import function.
    info : str
        Adsorbate-adsorbent information, output by a data import function.

    Returns
    -------
    bet_results : namedtuple
        Contains the results of BET analysis. Tuple elements are:

        - ``bet_results.intercept`` (ndarray) : 2D array of intercept
          values for the BET plot trendline. Indicies correspond to
          first and last datapoint used in the analysis.
        - ``bet_results.iso_df`` (DataFrame) : Experimental isotherm data.
        - ``bet_results.nm`` (ndarray) : 2D array of monolayer adsorbed
          amounts, in mol/g, indicies correspond to first and last
          datapoint used in the analysis.
        - ``bet_results.slope`` (ndarray) : 2D array of slope values
          for the BET plot trendline. Indicies correspond to first and
          last datapoint used in the analysis.
        - ``bet_results.ssa`` (ndarray) : 2D array of specific surface
          area values, in m^2/g, indicies correspond to first and last
          datapoint used in the analysis.
        - ``bet_results.c`` (ndarray) : 2D array of BET constants
          values, indicies correspond to first and last datapoint used
          in the analysis.
        - ``bet_results.err`` (ndarray) : 2D array of average error
          between a datapoint and the theoretical BET isotherm.
          Indicies correspond to first and last datapoint used in the
          analysis.
        - ``bet_results.r`` (ndarray) : 2D array of r values for the
          BET plot trendline. Indicies correspond to first and last
          datapoint used in the analysis.
        - ``bet_results.num_pts`` (ndarray) : 2D array of the number of
          experimental data points per relative pressure range.
        - ``bet_results.info`` (str) : string of adsorbate-adsorbent
          info by other functions to name files.

    """
    ssa_array = np.zeros((len(iso_df), len(iso_df)))
    c_array = np.zeros((len(iso_df), len(iso_df)))
    nm_array = np.zeros((len(iso_df), len(iso_df)))
    err_array = np.zeros((len(iso_df), len(iso_df)))
    slope = np.zeros((len(iso_df), len(iso_df)))
    intercept = np.zeros((len(iso_df), len(iso_df)))
    r = np.zeros((len(iso_df), len(iso_df)))
    bet_c = np.zeros(len(iso_df))
    number_pts = np.zeros((len(iso_df), len(iso_df)))

    for i in range(len(iso_df)):
        for j in range(len(iso_df)):
            if i > j:
                a = iso_df.iloc[j : i + 1]
                X = a.relp
                y = a.bet
                m, b, r_value, p_value, std_err = sp.stats.linregress(X, y)
                slope[i, j] = m
                intercept[i, j] = b
                r[i, j] = r_value
                c = 0
                nm = 0
                bet_c = 0
                if b != 0:
                    c = m / b + 1  # avoiding divide by zero issues
                    nm = 1 / (b * c)
                    bet_c = (1 / (nm * c)) + (c - 1) * iso_df.relp / (nm * c)
                spec_sa = nm * 6.022 * 10 ** 23 * a_o * 10 ** -20
                ssa_array[i, j] = spec_sa
                c_array[i, j] = c
                nm_array[i, j] = nm
                number_pts[i, j] = i - j + 1
                errors = np.nan_to_num(abs(bet_c - iso_df.bet) / bet_c)
                if i - j == 1:
                    err_array[i, j] = 0
                else:
                    err_array[i, j] = 100 * sum(errors[j : i + 1]) / (i + 1 - j)
                # error is normalized for the interval of relative pressures
                # used to compute C, so, min and max error corresponds to the
                # best and worst fit over the interval used in BET analysis,
                # not the entire isotherm
                tuple_fields = "intercept iso_df nm slope ssa c err r num_pts info"
                results = namedtuple("results", tuple_fields)
                bet_results = results(np.nan_to_num(intercept),
                                      iso_df,
                                      nm_array,
                                      slope,
                                      ssa_array,
                                      c_array,
                                      err_array,
                                      r,
                                      number_pts,
                                      info)
    return bet_results


def single_point_bet(df, a_o):
    """
    Performs single point BET analysis on an isotherm data set for all
    relative pressure ranges. Can be used to check for agreement between BET
    and single point BET.

    Parameters
    ----------
    bet_results : namedtuple
        Contains all information required for BET analysis. Results of BET
        analysis are also stored in this named tuple. Relevant fields are:

        - ``bet_results.raw_data`` (DataFrame) : experimental isotherm data.
        - ``bet_results.a_o`` (flaot) : the cross sectional area of the
          adsorbate molecule, in square angstrom.

    Returns
    -------
    singlept_results : namedtuple
        Contains the results of single point BET analysis. Relevant fields are:

        - ``singlept_results.ssa`` (ndarray) : 2D array of specific surface
          area values, in m^2/g, indicies correspond to first and last
          datapoint used in the analysis.
        - ``singlept_results.nm`` (ndarray) : 2D array of monolayer adsorbed
          amounts, in mol/g, indicies correspond to first and last datapoint
          used in the analysis.

    """

    ssa_array = np.zeros((len(df), len(df)))
    nm_array = np.zeros((len(df), len(df)))

    for i in range(len(df)):
        for j in range(len(df)):
            if i > j:
                n_range = df.n[j:i]
                relp_range = df.relp[j:i]
                n = np.ma.median(n_range)
                relp = np.ma.median(relp_range)

                nm_array[i, j] = n * (1 - relp)
                ssa_array[i, j] = n * 6.022 * 10 ** 23 * a_o * 10 ** -20

    singlept_results = namedtuple("singlept_results", ("ssa", "nm"))
    singlept_results.ssa = ssa_array
    singlept_results.nm = nm_array

    return singlept_results


def check_y_intercept_positive(intercept):
    """
    Checks that y intercept of the BET plot's linear regression is positive.

    Parameters
    ----------
    intercept : ndarray
        2D array of y-intercept values.

    Returns
    -------
    ndarray
        Array of 1s and 0s where 0 corresponds to relative pressure ranges
        where the y-intercept is negative or zero, ie ranges that fail this
        check.

    """
    check1 = intercept[:, :] > 0

    if np.any(check1) is False:
        logging.warning("All relative pressure ranges fail check 1.")

    return check1


def check_pressure_increasing(df):
    """
    Checks that n(p-po) aka check2 is increasing.

    This is a necessary condition for linearity of the BET dataset.

    Parameters
    ----------
    df : dataframe
        Dataframe of imported experimental isothermal adsorption data.

    Returns
    -------
    ndarray
        Array of 1s and 0s where 0 corresponds to relative pressure ranges
        where n(p-po) isn't consistently increasing with relative pressure, ie
        ranges that fail this check.

    """
    df["check2"] = df.n * (1 - df.relp)
    check2 = np.ones((len(df), len(df)))
    minus1 = np.concatenate(([0], df.check2[:-1]))
    test = df.check2 - minus1 >= 0
    test = np.tile(test, (len(df), 1))
    check2 = check2 * test
    check2 = check2.T

    if np.any(check2) is False:
        logging.warning("All relative pressure ranges fail check 2.")

    return check2


def check_absorbed_amount(df, nm):
    """
    Checks that nm, amount adsorbed in the monolayer, is in the range of
    data points used in BET analysis.

    Parameters
    ----------
    df : dataframe
        Dataframe of imported experimental isothermal adsorption data.
    nm : array
        2D array of BET specific amount of adsorbate in the monolayer, the
        coordinates of the array corresponding to relative pressures, units
        [moles / gram].

    Returns
    -------
    ndarray
        Array of 1s and 0s where 0 corresponds to relative pressure ranges nm
        is not included in the range of experimental n values, ie ranges that
        fail this check.

    """

    check3 = np.zeros((len(df), len(df)))

    for i in range(np.shape(check3)[0]):
        for j in range(np.shape(check3)[1]):
            if df.iloc[j, 1] <= nm[i, j] <= df.iloc[i, 1]:
                check3[i, j] = 1

    if np.any(check3) is False:
        logging.warning("All relative pressure ranges fail check 3.")

    return check3


def check_pressure_consistency(df, nm, slope, intercept):
    """
    Checks that relative pressure is consistent.

    The relative pressure corresponding to nm is found from linear
    interpolation of the experiemental data.

    A second relative pressure is found by setting n to nm in the BET equation
    and solving for relative pressure.

    The two relative pressures are compared and must agree within 10% to pass
    this check.

    Parameters
    ----------
    df : dataframe
        Dataframe of imported experimental isothermal adsorption data.
    nm : array
        2D array of BET specific amount of adsorbate in the monolayer,
        the coordinates of the array corresponding to relative pressures,
        units [moles / gram].
    slope : array
        2D array of slope values resulting from linear regression applied to
        relevant experimental data.
    intercept : array
        2D array of y-intercept values resulting from linear regression applied
        to relevant experimental data.

    Returns
    -------
    ndarray
        Array of 1s and 0s where 0 corresponds to relative pressure values that
        do not agree within 10%, ie ranges that fail this check.

    """

    check4 = np.zeros((len(df), len(df)))

    for i in range(np.shape(check4)[0]):
        for j in range(np.shape(check4)[1]):
            if nm[i, j] != 0 and i > 0 and j > 0:
                # find relp corresponding to nm
                relpm = util.lin_interp(df, nm[i, j])
                # BET eq solved for relp is a quadratic, coeff = [a, b, c]
                coeff = [
                    -1 * slope[i, j] * nm[i, j],
                    slope[i, j] * nm[i, j] - 1 - intercept[i, j] * nm[i, j],
                    intercept[i, j] * nm[i, j],
                ]
                # find roots
                # (relp value where nm occurs on theoretical isotherm)
                roots = np.roots(coeff)  # note: some roots are imaginary
                roots = [item.real for item in roots if len(roots) == 2]
                # find the difference between
                relp_m_1 = roots[0]
                diff_1 = abs((relp_m_1 - relpm) / relpm)
                relp_m_2 = roots[1]
                diff_2 = abs((relp_m_2 - relpm) / relpm)
                diff = min(diff_1, diff_2)

                if diff < 0.1:
                    check4[i, j] = 1

    if np.any(check4) is False:
        logging.warning("All relative pressure ranges fail check 4.")

    return check4


def check_enough_datapoints(df, points=5):
    """
    Checks that relative pressure ranges contain a minium number of data points.

    Parameters
    ----------
    df : dataframe
        Dataframe of imported experimental isothermal adsorption data.

    points : int
        Minimum number of data points required for BET analysis to be
        considered valid, default value is 5.

    Returns
    -------
    ndarray
        Array of 1s and 0s where 0 corresponds to ranges of experimental data
        that contain less than the minimum number of points.

    """
    check5 = np.ones((len(df), len(df)))

    for i in range(len(df)):
        for j in range(len(df)):
            if i - j < points - 1:
                check5[i, j] = 0

    if np.any(check5) is False:
        logging.warning("All relative pressure ranges fail check 5.")

    return check5


def rouq_mask(intercept, iso_df, nm, slope, *args,
              enforce_y_intercept_positive=True,
              enforce_pressure_increasing=True,
              enforce_absorbed_amount=True,
              enforce_relative_pressure=True,
              enforce_enough_datapoints=True,
              points=5):
    """
    Calls all check functions and combines their masks into one "rouqerol mask".

    Rather than pass individual parameters, this function can accept
    ``bet_results`` (where ``bet_results`` is a named tuple output by the bet
    function).

    Parameters
    ----------
    intercept : ndarray
        2D array of intercept values, used in check1.
    iso_df : DataFrame
        Dataframe of isotherm data, used in check2.
    nm : ndarray
        2D array of amount in the monolayer values, used in check3 and check4.
    slope : ndarray
        2D array of slope values, used in check4
    enforce_y_intercept_positive : bool
        If True, this check will be evaluated, otherwise skipped.
    enforce_pressure_increasing : bool
        If True, this check will be evaluated, otherwise skipped.
    enforce_absorbed_amount_valid : bool
        If True, this check will be evaluated, otherwise skipped.
    enforce_relative_pressure_valid : bool
        If True, this check will be evaluated, otherwise skipped.
    enforce_enough_datapoints : bool
        If True, this check will be evaluated, otherwise skipped.
    points : int
        The minimum number of experimental data points for a relative pressure
        interval to be considered valid.

    Returns
    -------
    rouq_mask : namedtuple
        Contains arrays for the result of each check and a masked array that is
        the result of all selected checks. Fields of the named tuple are:

        - ``rouq_mask.mask`` (MaskedArray) : object where invalid BET results
          are masked.
        - ``rouq_mask.check1`` (ndarray) : array of 1s and 0s where 0 corresponds
          failing check1.
        - ``rouq_mask.check2`` (ndarray) : array of 1s and 0s where 0 corresponds
          failing check2.
        - ``rouq_mask.check3`` (ndarray) : array of 1s and 0s where 0 corresponds
          failing check3.
        - ``rouq_mask.check4`` (ndarray) : array of 1s and 0s where 0 corresponds
          failing check4.
        - ``rouq_mask.check5`` (ndarray) : array of 1s and 0s where 0 corresponds
          failing check5.

    """

    mask = np.ones((len(iso_df), len(iso_df)))
    for i in range(len(iso_df)):
        for j in range(len(iso_df)):
            if j >= i:
                mask[i, j] = 0

    if enforce_y_intercept_positive is True:
        check1 = check_y_intercept_positive(intercept)
    else:
        check1 = np.ones((len(iso_df), len(iso_df)))

    if enforce_pressure_increasing is True:
        check2 = check_pressure_increasing(iso_df)
    else:
        check2 = np.ones((len(iso_df), len(iso_df)))

    if enforce_absorbed_amount is True:
        check3 = check_absorbed_amount(iso_df, nm)
    else:
        check3 = np.ones((len(iso_df), len(iso_df)))

    if enforce_relative_pressure is True:
        check4 = check_pressure_consistency(iso_df, nm, slope, intercept)
    else:
        check4 = np.ones((len(iso_df), len(iso_df)))

    if enforce_enough_datapoints is True:
        check5 = check_enough_datapoints(iso_df, points)
    else:
        check5 = np.ones((len(iso_df), len(iso_df)))

    mask = np.multiply(check1, mask)
    mask = np.multiply(check2, mask)
    mask = np.multiply(check3, mask)
    mask = np.multiply(check4, mask)
    mask = np.multiply(check5, mask)

    mask = mask.astype(bool)  # converting mask to boolean
    # inverting mask so that 0 = valid, 1 = invalid, to work well with numpy masks
    invertedmask = np.logical_not(mask)

    rouq_mask = namedtuple("rouq_mask", "mask check1 check2 check3 check4 check5")
    mask_results = rouq_mask(invertedmask, check1, check2, check3, check4, check5)

    return mask_results


def ssa_answer(bet_results, mask_results, criterion="error"):
    """
    Logs a single specific surface area answer from the valid relative
    pressure range with the lowest error, most number of points, maximum
    specific surface area, or minimum specific surface area.

    Parameters
    ----------
    bet_results : named tuple
        ``bet_results.ssa`` contains the array of specific surface values.
    rouq_mask : named tuple
        ``rouq_mask.mask`` contains the mask used to remove invaid specific
        surface area values from consideration.
    criterion : str
        Used to specify the criterion for a final specific surface area answer,
        either 'error', 'points', 'max', or 'min. Defaults to 'error'.

    Returns
    -------
    ssa_ans : float
        Specific surface answer corresponding to user defined criteria.

    """

    mask = mask_results.mask

    if mask.all():
        msg = "No valid relative pressure ranges. Specific surface area not calculated."
        raise ValueError(msg)

    ssa = np.ma.array(bet_results.ssa, mask=mask)

    if criterion == "points":
        pts = np.ma.array(bet_results.num_pts, mask=mask)
        max_pts = np.max(pts)
        ssa_ans_array = np.ma.masked_where(pts < max_pts, ssa)
        try:
            ssa_ans = float(ssa_ans_array.compressed())
        except ValueError:
            raise Exception(
                "Error, so single specific surface area answer. Multiple"
                + "relative pressure ranges with the maximum number of points."
            )
            return 0
        logging.info(
            "The specific surface area value, based on %s is %.2f m2/g."
            % (criterion, ssa_ans)
        )
        return ssa_ans

    if criterion == "error":
        err = np.ma.array(bet_results.err, mask=mask)
        errormax, error_max_idx, errormin, error_min_idx = util.max_min(err)
        ssa_ans = ssa[int(error_min_idx[0]), int(error_min_idx[1])]
        logging.info(
            "The specific surface area value, based on %s is %.2f m2/g."
            % (criterion, ssa_ans)
        )
        return ssa_ans

    if criterion == "max":
        ssa_ans = np.max(ssa)
        logging.info(
            "The specific surface area value, based on %s is %.2f m2/g."
            % (criterion, ssa_ans)
        )
        return ssa_ans

    if criterion == "min":
        ssa_ans = np.min(ssa)
        logging.info(
            "The specific surface area value, based on %s is %.2f m2/g."
            % (criterion, ssa_ans)
        )
        return ssa_ans

    else:
        raise ValueError("Invalid criterion, must be points, error, min, or max.")


def run_beatmap(file=None,
                info=None,
                a_o=None,
                check1=True,
                check2=True,
                check3=True,
                check4=True,
                check5=True,
                points=5,
                save_figures=True,
                export_data=False,
                ssa_criterion="error",
                ssa_gradient="Greens",
                err_gradient="Greys"):
    """
    A single function that executes all necessary BEaTmap algorithims.

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
    file : str
        File name (if file is in parent directory) or file path.
    info : str
        Adsorbate-adsorbent information.
    a_o : float
        Cross sectional area of adsorbate, in square Angstrom.
    check1 : bool
        If check1 is True any relative pressure ranges with a negative y
        intercept are considered invalid.
    check2 : bool
        If check2 is True any relative pressure ranges where n(p-po) is
        decreasing are considered invalid.
    check3 : bool
        If check3 is True any relative pressure ranges where the monolayer
        amount falls outside of the relative pressure range are considered
        invalid.
    check4 : bool
        If check4 is True any relative pressure range where there is
        disagreement of more than 10% between the actual relative pressure
        where monolayer coverage occurs and the relative pressure where
        monolayer coverage occurs on the theoretical isotherm are considered
        invalid.
    check5 : bool
        If check5 is True relative pressure ranges that contain fewer points
        than specified by the user are considered invalid.
    points : int
        The minimum number of points for a valid relative pressure range.
    save_figures : bool
        If save_figures is True any figures created by this function will be
        saved as .png files in the parent directory.
    export_data : bool
        If export data is True .csv files of the isotherm data and the BEaTmap
        results will be created and saved in the parent directory.
    ssa_criterion : str
        Used to set which criterion is used to provide a single specific
        surface area value. 'error' will output the valid ssa answer with the
        lowest error, 'points' will output the ssa answer with the most
        datapoints.
    ssa_gradient : str
        Color gradient for heatmap, must be a vaild color gradient name
        in the seaborn package.
    err_gradient : str
        Color gradient for heatmap, must be a vaild color gradient name
        in the seaborn package, default is grey.

    Returns
    -------
    None

    """

    # run_beatmap_import_data imports isotherm data from a .csv file and returns
    # the results in the isotherm_data namedtuple
    isotherm_data = io.import_data(file, info, a_o)

    figs.experimental_data_plot(isotherm_data, save_file=save_figures)

    # bet_results uses isotherm_data, applies BET analysis and returns the results
    # in the bet_results namedtuple

    bet_results = bet(isotherm_data.iso_df, isotherm_data.a_o, isotherm_data.info)

    # mask_results uses isotherm_data and bet_results, applies the roquerol
    # criteria specified by the user, and returns the results in the
    # mask_results named tuple

    mask_results = rouq_mask(bet_results.intercept,
                             bet_results.iso_df,
                             bet_results.nm,
                             bet_results.slope,
                             enforce_y_intercept_positive=check1,
                             enforce_pressure_increasing=check2,
                             enforce_absorbed_amount=check3,
                             enforce_relative_pressure=check4,
                             enforce_enough_datapoints=check5,
                             points=points)

    # mask_results are used to highlight the valid bet_results in the
    # following functions

    # ssa_ans = ssa_answer(bet_results, mask_results, ssa_criterion)

    figs.ssa_heatmap(bet_results, mask_results, save_figures)
    figs.err_heatmap(bet_results, mask_results, save_figures)
    figs.bet_combo_plot(bet_results, mask_results, save_figures)
    figs.iso_combo_plot(bet_results, mask_results, save_figures)
    figs.ascii_tables(bet_results, mask_results)

    if export_data is True:
        io.export_raw_data(isotherm_data)
        io.export_processed_data(bet_results, points)

    fields = (
        "ssa c nm err intercept slope r mask check1 check2 check3 check4 check5 num_pts"
    )
    combo_results = namedtuple("results", fields)

    results = combo_results(bet_results.ssa,
                            bet_results.c,
                            bet_results.nm,
                            bet_results.err,
                            bet_results.intercept,
                            bet_results.slope,
                            bet_results.r,
                            mask_results.mask,
                            mask_results.check1,
                            mask_results.check2,
                            mask_results.check3,
                            mask_results.check4,
                            mask_results.check5,
                            bet_results.num_pts)

    return results
