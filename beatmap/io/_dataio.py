from re import I
import numpy as np
import pandas as pd
import scipy as sp
import logging
from beatmap import core as bet
from collections import namedtuple


__all__ = [
    "import_data",
    "export_raw_data",
    "export_processed_data",
    "import_list_data",
]


def check_header(file, th=0.9):
    """Checks csv file being imported for headers.

    Parameters
    ----------
    file : str
        File name or filepath.
    th : float
        Threshold value that must be met to determine file has no headers.

    Returns
    -------
    str or None
        If threshold not met the file is determined to have headers and 'infer'
        is returned to pass to header parameter in pandas.read_csv().

    """

    df1 = pd.read_csv(file, header="infer")
    df2 = pd.read_csv(file, header=None)
    sim = (df1.dtypes.values == df2.dtypes.values).mean()
    if sim < th:
        return "infer"
    else:
        return None


def import_data(file=None, info=None, a_o=None):
    """Imports isothermal adsoprtion data from a csv file.

    The .csv file format expected is a two column table,
    the first column being "n" (specific amount adsorbed, mol/g)
    and the second being the relative pressure.

    Parameters
    ----------
    file : str or buffer
        Path to the csv file that contains BET data
    info : str
        Short description of data, will be used as identifier
    a_o : float
        Cross sectional area of the adsorbate molecule, in square angstrom.

    Returns
    -------
    isotherm_data : namedtuple
        Contains all information required for BET analysis. Relevant fields are:

        - ``isotherm_data.iso_data`` (DataFrame) : imported isotherm data.
        - ``isotherm_data.a_o`` (float) : adsorbate cross sectional area.
        - ``isotherm_data.info`` (str) : string of adsorbate-adsorbent info.
        - ``isotherm_data.file`` (str) : file name or path.

    """
    msg = f"Adsorbate has an adsorbed cross sectional area of {a_o:.2f} sq. Angstrom."
    logging.info(msg)

    if not isinstance(file, pd.DataFrame):  # workaround for streamlit app cache to work
        data = pd.read_csv(file, header="infer")
    else:
        data = file

    try:
        header = data.columns
        temp = pd.DataFrame([header.astype(float)], columns=["relp", "n"])
        data = data.rename(columns={header[0]: "relp", header[1]: "n"})
        data = pd.concat([temp, data], ignore_index=True)
    except TypeError:
        pass

    labels = list(data)
    data.rename(columns={labels[0]: "relp", labels[1]: "n"}, inplace=True)

    if type(a_o) == str:
        raise ValueError("a_o must be int or float.")

    if (data["n"] == 0).any():
        raise ValueError("Cannot have n = 0 values in dataframe.")

    data["n"] = data.n  # necessary? why that here?
    data["bet"] = (1 / data.n) * (data.relp / (1 - data.relp))

    # checking data quality
    test = np.zeros(len(data))
    minus1 = np.concatenate(([0], data.n[:-1]))
    test = data.n - minus1
    test_sum = sum(x < 0 for x in test)
    if test_sum > 0:
        logging.info("Isotherm data is suspect. moles do not consistantly"
                     " increase as relative pressure increases.")
    else:
        logging.info("Isotherm data quality appears good. Adsorbed molar"
                     " amounts are increasing as relative pressure increases.")

    # checking isotherm type
    x = data.relp.values
    y = data.n.values

    dist = np.sqrt((x[:-1] - x[1:]) ** 2 + (y[:-1] - y[1:]) ** 2)
    dist_along = np.concatenate(([0], dist.cumsum()))

    # build a spline representation of the contour
    spline, u = sp.interpolate.splprep(
        [x, y], u=dist_along, w=np.multiply(1, np.ones(len(x))), s=1e-10
    )
    interp_d = np.linspace(dist_along[0], dist_along[-1], 50)
    interp_x, interp_y = sp.interpolate.splev(interp_d, spline)

    # take derivative of the spline (to find inflection points)
    spline_1deriv = np.diff(interp_y) / np.diff(interp_x)
    spline_2deriv = np.diff(spline_1deriv) / np.diff(interp_x[1:])

    zero_crossings = np.where(np.diff(np.sign(spline_2deriv)))[0]

    if len(zero_crossings) == 0 and np.sign(spline_2deriv[0]) == -1:
        logging.info("Isotherm is type I.")
    elif len(zero_crossings) == 0 and np.sign(spline_2deriv[0]) == 1:
        logging.info("Isotherm is type III.")
    elif len(zero_crossings) == 1 and np.sign(spline_2deriv[0]) == -1:
        logging.info("Isotherm is type II.")
    elif len(zero_crossings) == 1 and np.sign(spline_2deriv[0]) == 1:
        logging.info("Isotherm is type V.")
    elif len(zero_crossings) == 2 and np.sign(spline_2deriv[0]) == -1:
        logging.info("Isotherm is type IV.")
    else:
        logging.info("Isotherm is type VI.")

    iso_data = namedtuple("iso_data", "iso_df a_o info file")
    isotherm_data = iso_data(data, a_o, info, file)

    return isotherm_data


def import_list_data(relp, n, a_o=None, file=None, info=None):
    """Imports isothermal adsoprtion data.

    User provides two lists, one of relative pressures and the other of amount
    adsorbed with units of [mol/g].

    Parameters
    ----------
    relp : list
        Experimental isotherm relative pressure values.
    n : list
        Experimental amount adsorbed values, mols per gram.

    Returns
    -------
    isotherm_data : namedtuple
        Contains all information required for BET analysis. Relevant fields are:

        - ``isotherm_data.iso_data`` (DataFrame) : imported isotherm data.
        - ``isotherm_data.a_o`` (float) : adsorbate cross sectional area.
        - ``isotherm_data.info`` (str) : string of adsorbate-adsorbent info.
        - ``isotherm_data.file`` (str) : file name or path.

    """
    if not isinstance(a_o, (int, float)):
        raise ValueError("a_o must be int or float.")

    logging.info(
        f"Adsorbate has an adsorbed cross sectional area of {a_o:.2f} sq. Angstrom."
    )

    # importing data and creating 'bet' and 'check2' data points
    dict_from_lists = {"relp": relp, "n": n}
    data = pd.DataFrame(dict_from_lists)
    data["bet"] = (1 / data.n) * (data.relp / (1 - data.relp))

    # checking data quality
    test = np.zeros(len(data))
    minus1 = np.concatenate(([0], data.n[:-1]))
    test = data.n - minus1
    test_sum = sum(x < 0 for x in test)
    if test_sum > 0:
        logging.info(
            "Isotherm data is suspect. Adsorbed moles do not consistantly"
            " increase as relative pressure increases"
        )
    else:
        logging.info(
            "Isotherm data quality appears good. Adsorbed molar amounts"
            " are increasing as relative pressure increases."
        )

    # checking isotherm type
    x = data.relp.values
    y = data.n.values

    dist = np.sqrt((x[:-1] - x[1:]) ** 2 + (y[:-1] - y[1:]) ** 2)
    dist_along = np.concatenate(([0], dist.cumsum()))

    # build a spline representation of the contour
    spline, u = sp.interpolate.splprep(
        [x, y], u=dist_along, w=np.multiply(1, np.ones(len(x))), s=1e-10
    )
    interp_d = np.linspace(dist_along[0], dist_along[-1], 50)  # len(x)
    interp_x, interp_y = sp.interpolate.splev(interp_d, spline)

    # take derivative of the spline (to find inflection points)
    spline_1deriv = np.diff(interp_y) / np.diff(interp_x)
    spline_2deriv = np.diff(spline_1deriv) / np.diff(interp_x[1:])

    zero_crossings = np.where(np.diff(np.sign(spline_2deriv)))[0]

    if len(zero_crossings) == 0 and np.sign(spline_2deriv[0]) == -1:
        logging.info("Isotherm is type I.")
    elif len(zero_crossings) == 0 and np.sign(spline_2deriv[0]) == 1:
        logging.info("Isotherm is type III.")
    elif len(zero_crossings) == 1 and np.sign(spline_2deriv[0]) == -1:
        logging.info("Isotherm is type II.")
    elif len(zero_crossings) == 1 and np.sign(spline_2deriv[0]) == 1:
        logging.info("Isotherm is type V.")
    elif len(zero_crossings) == 2 and np.sign(spline_2deriv[0]) == -1:
        logging.info("Isotherm is type IV.")
    else:
        logging.info("Isotherm is type VI.")

    iso_data = namedtuple("iso_data", "iso_df a_o info file")
    isotherm_data = iso_data(data, a_o, info, file)

    return isotherm_data


def export_raw_data(isotherm_data):
    """Exports isothermal adsoprtion data.

    Exported data is saved as a .csv file in the parent directory.

    Parameters
    ----------

    isotherm_data : namedtuple
        Contains all information required for BET analysis. Relevant fields are:

        - ``isotherm_data.iso_df`` (DataFrame) : of the raw isotherm data
          written to a .csv
        - ``bet_results.info`` (str) : adsorbate-adsorbent information used

    Returns
    -------
    None

    """

    export_file_name = isotherm_data.info + "_raw_data_export.csv"
    df = isotherm_data.iso_df
    df.to_csv(export_file_name, index=None, header=True)
    logging.info("Raw data saved as: %s" % (export_file_name))
    return


def export_processed_data(bet_results, points=5):
    """Exports processed isothermal adsoprtion data.

    Exported data is saved as a .csv file in the parent directory.

    Parameters
    ----------

    bet_results : namedtuple
        Contains all information required for BET analysis.
        Relevant fields are:

    points : int
        The minimum number of experimental data points for a relative pressure
        interval to be considered valid. Default is 5.

    Returns
    -------
    None

    """

    df = bet_results.iso_df
    i = 0
    end_relp = np.zeros((len(df), len(df)))
    while i < len(df):
        end_relp[i:] = df.relp[i]
        i += 1

    begin_relp = np.transpose(end_relp)

    mask1 = bet.check_y_intercept_positive(bet_results.intercept)
    mask2 = bet.check_pressure_increasing(df)
    mask3 = bet.check_absorbed_amount(df, bet_results.nm)
    mask4 = bet.check_pressure_consistency(df,
                                              bet_results.nm,
                                              bet_results.slope,
                                              bet_results.intercept)
    mask5 = bet.check_enough_datapoints(df, points)

    processed_data = np.column_stack((begin_relp.flatten(), end_relp.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.ssa.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.nm.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.c.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.err.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.slope.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.intercept.flatten()))
    processed_data = np.column_stack((processed_data, bet_results.r.flatten()))
    processed_data = np.column_stack((processed_data, mask1.flatten()))
    processed_data = np.column_stack((processed_data, mask2.flatten()))
    processed_data = np.column_stack((processed_data, mask3.flatten()))
    processed_data = np.column_stack((processed_data, mask4.flatten()))
    processed_data = np.column_stack((processed_data, mask5.flatten()))

    processed_data = pd.DataFrame(
        data=processed_data,
        columns=[
            "begin relative pressure",
            "end relative pressure",
            "spec sa [m2/g]",
            "bet constant",
            "nm [mol/g]",
            "error",
            "slope",
            "y-int",
            "r value",
            "check1",
            "check2",
            "check3",
            "check4",
            "check5",
        ],
    )

    export_file_name = bet_results.info + "_processed_data_export.csv"
    processed_data.to_csv(export_file_name, index=None, header=True)
    logging.info("Processed data saved as: %s" % (export_file_name))
