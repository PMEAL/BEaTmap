import numpy as np
import scipy as sp
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from beatmap import utils as util
import matplotlib.ticker as ticker


__all__ = [
    "experimental_data_plot",
    "ssa_heatmap",
    "err_heatmap",
    "bet_combo_plot",
    "iso_combo_plot",
]


def experimental_data_plot(isotherm_data, save_file=False):
    """Creates a scatter plot of experimental data.

    Typical isotherm presentation where
    x-axis is relative pressure, y-axis is specific amount adsorbed.

    Parameters
    ----------
    isotherm_data : namedtuple
        The isotherm_data.iso_df element is used to
        create a plot of isotherm data.

    save_file : boolean
        When save_file=True a .png of the figure is created in the
        working directory.

    Returns
    -------

    """

    df = isotherm_data.iso_df
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.set_xlim(0, 1.0)
    # ax.set_ylim(0, df['n'].iloc[-1] * 1.05)
    ax.set_title("Experimental Isotherm")
    ax.set_ylabel("n [mol/g]")
    ax.set_xlabel("P/Po")
    ax.grid(b=True, which="major", color="gray", linestyle=":")
    ax.plot(df.relp, df.n, c="k", marker="o", markerfacecolor="w", linewidth=0)

    if save_file is True:
        fig.savefig(
            "experimentaldata_%s.png" % (isotherm_data.info), bbox_inches="tight"
        )
        logging.info(
            "Experimental data plot saved as: experimentaldata_%s.png"
            % (isotherm_data.info)
        )
    return


def ssa_heatmap(bet_results, mask_results, save_file=True, gradient="Greens"):
    """Creates a heatmap of specific surface areas.

    Shading corresponds to specific surface area, normalized for the minimum
    and maximum specific sa values.

    Parameters
    ----------
    bet_results : namedtuple
        The bet_results.ssa element is used to create a heatmap of specific
        surface area answers.

    mask_results : namedtuple
        The mask_results.mask element is used to mask the
        specific surface area heatmap so that only valid results are
        displayed.

    save_file : boolean
        When save_file = True a png of the figure is created in the
        working directory.

    gradient : string
        Color gradient for heatmap, must be a vaild color gradient name
        in the seaborn package.

    Returns
    -------

    """

    mask = mask_results.mask

    if mask.all():
        logging.warning(
            "No valid relative pressure ranges. Specific surface area"
            " heatmap not created."
        )
        return

    df = bet_results.iso_df

    # creating a masked array of ssa values
    ssa = np.ma.array(bet_results.ssa, mask=mask)

    # finding max and min sa to normalize heatmap colours
    ssamax, ssa_max_idx, ssamin, ssa_min_idx = util.max_min(ssa)
    hm_labels = round(df.relp * 100, 1)
    fig, (ax) = plt.subplots(1, 1, figsize=(13, 13))
    sns.heatmap(
        ssa,
        vmin=ssamin,
        vmax=ssamax,
        square=True,
        cmap=gradient,
        mask=(ssa == 0),
        xticklabels=hm_labels,
        yticklabels=hm_labels,
        linewidths=1,
        linecolor="w",
        cbar_kws={"shrink": 0.78, "aspect": len(df.relp)},
    )
    ax.invert_yaxis()
    ax.set_title(
        "Specific Surface Area m^2/g"
    )
    plt.xticks(rotation=45, horizontalalignment="right")
    plt.xlabel("Start Relative Pressure")
    plt.yticks(rotation=45, horizontalalignment="right")
    plt.ylabel("End Relative Pressure")

    if save_file is True:
        fig.savefig("ssa_heatmap_%s.png" % (bet_results.info), bbox_inches="tight")
        logging.info(
            "Specific surface area heatmap saved as: ssa_heatmap_%s.png"
            % (bet_results.info)
        )
    return


def err_heatmap(bet_results, mask_results, save_file=True, gradient="Greys"):
    """Creates a heatmap of error values.

    Shading corresponds to average error between experimental data and the
    the theoretical BET isotherm, normalized so that, with default shading,
    0 is displayed as white and the maximum error value is black.


    Parameters
    ----------
    bet_results : namedtuple
        The bet_results.err element is used to create a heatmap of error
        values.

    mask_results : namedtuple
        The mask_results.mask element is used to mask the error heatmap so that
        only valid results are displayed.

    save_file : boolean
        When save_file = True a png of the figure is created in the
        working directory.

    gradient : string
        Color gradient for heatmap, must be a vaild color gradient name
        in the seaborn package, default is grey.

    Returns
    -------

    """
    mask = mask_results.mask

    if mask.all():
        logging.warning(
            "No valid relative pressure ranges. Error heat map not created."
        )
        return

    df = bet_results.iso_df

    # creating a masked array of error values
    err = np.ma.array(bet_results.err, mask=mask)

    errormax, error_max_idx, errormin, error_min_idx = util.max_min(err)

    hm_labels = round(df.relp * 100, 1)
    fig, (ax) = plt.subplots(1, 1, figsize=(13, 13))
    sns.heatmap(
        err,
        vmin=0,
        vmax=errormax,
        square=True,
        cmap=gradient,
        mask=(err == 0),
        xticklabels=hm_labels,
        yticklabels=hm_labels,
        linewidths=1,
        linecolor="w",
        cbar_kws={"shrink": 0.78, "aspect": len(df.relp)},
    )
    ax.invert_yaxis()
    ax.set_title(
        "Average Error per Point Between Experimental and" " Theoretical Isotherms"
    )
    plt.xticks(rotation=45, horizontalalignment="right")
    plt.xlabel("Start Relative Pressure")
    plt.yticks(rotation=45, horizontalalignment="right")
    plt.ylabel("End Relative Pressure")

    if save_file is True:
        fig.savefig("error_heatmap_%s.png" % (bet_results.info), bbox_inches="tight")
        logging.info("Error heatmap saved as: error_heatmap_%s.png" % (bet_results.info))
    return


def bet_combo_plot(bet_results, mask_results, save_file=True):
    """Creates a BET plots for the minimum and maxium error data sets.

    Only datapoints in the minimum and maximum error data sets are plotted.
    Equation for best fit line and corresponding R value are annotated on plot.

    Parameters
    ----------

    bet_results : namedtuple
        Namedtuple where the bet_results.iso_df element is used to
        create a plot of isotherm BET values.

    mask_results : namedtuple
        The mask_results.mask element is used to mask the BET results so that
        only valid results are displayed.

    save_file : boolean
        When save_file = True a png of the figure is created in the
        working directory.

    Returns
    -------

    """

    mask = mask_results.mask

    if mask.all():
        logging.warning(
            "No valid relative pressure ranges. BET combo plot not created."
        )
        return

    df = bet_results.iso_df
    err = np.ma.array(bet_results.err, mask=mask)

    err_max, err_max_idx, err_min, err_min_idx = util.max_min(err)

    min_start = int(err_min_idx[1])
    min_stop = int(err_min_idx[0])
    max_start = int(err_max_idx[1])
    max_stop = int(err_max_idx[0])

    slope, intercept, r_val, p_value, std_err = sp.stats.linregress(
        df.relp[min_start : min_stop + 1], df.bet[min_start : min_stop + 1]
    )

    min_liney = np.zeros(2)
    min_liney[0] = slope * (df.relp[min_start] - 0.01) + intercept
    min_liney[1] = slope * (df.relp[min_stop] + 0.01) + intercept
    min_linex = np.zeros(2)
    min_linex[0] = df.relp[min_start] - 0.01
    min_linex[1] = df.relp[min_stop] + 0.01

    (
        slope_max,
        intercept_max,
        r_value_max,
        p_value_max,
        std_err_max,
    ) = sp.stats.linregress(
        df.relp[max_start : max_stop + 1], df.bet[max_start : max_stop + 1]
    )
    max_liney = np.zeros(2)
    max_liney[0] = slope_max * (df.relp[max_start] - 0.01) + intercept_max
    max_liney[1] = slope_max * (df.relp[max_stop] + 0.01) + intercept_max
    max_linex = np.zeros(2)
    max_linex[0] = df.relp[max_start] - 0.01
    max_linex[1] = df.relp[max_stop] + 0.01

    figure, ax1 = plt.subplots(1, figsize=(10, 10))

    ax1.set_title("BET Plot")
    ax1.set_xlim(0, max(min_linex[1], max_linex[1]) * 1.1)
    ax1.set_ylabel("1/[n(P/Po-1)]")
    ax1.set_ylim(0, max(min_liney[1] * 1.1, max_liney[1] * 1.1))
    ax1.set_xlabel("P/Po")
    ax1.grid(b=True, which="major", color="gray", linestyle="-")
    ax1.plot(
        df.relp[min_start : min_stop + 1],
        df.bet[min_start : min_stop + 1],
        label="min error (exp. data)",
        c="grey",
        marker="o",
        linewidth=0,
        fillstyle="none",
    )
    ax1.plot(min_linex, min_liney, color="black", label="min error (linear regression)")
    ax1.plot(
        df.relp[max_start : max_stop + 1],
        df.bet[max_start : max_stop + 1],
        label="Max Error Experimental Data",
        c="grey",
        marker="x",
        linewidth=0,
    )
    ax1.plot(
        max_linex,
        max_liney,
        color="black",
        linestyle="--",
        label="max error (linear regression)",
    )
    ax1.legend(loc="upper left", framealpha=1)
    ax1.annotate(
        "min error (linear regression): \nm = %.3f \nb = %.3f \nR = \
%.3f \n\nmax error (linear regression): \nm = %.3f \nb = %.3f \
\nR = %.3f"
        % (slope, intercept, r_val, slope_max, intercept_max, r_value_max),
        bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=1),
        textcoords="axes fraction",
        xytext=(0.695, 0.017),
        xy=(df.relp[min_stop], df.bet[min_start]),
        size=11,
    )

    if save_file is True:
        figure.savefig("betplot_%s.png" % (bet_results.info), bbox_inches="tight")
        logging.info("BET plot saved as: betplot_%s.png" % (bet_results.info))
    return


def iso_combo_plot(bet_results, mask_results, save_file=True):
    """Creates an image displaying the relative pressure range with minimum
    error and the BET isotherm on the same plot. The point where n/nm = 1 is
    is the point where the BET monolayer loading occurs.

    Parameters
    ----------

    bet_results : named tuple
        The bet_results.iso_df element is used to
        create a plot of isotherm data.

    mask_results : named tuple
        The mask_results.mask element is used to mask the BET results so that
        only valid results are displayed.

    save_file : boolean
        When save_file = True a png of the figure is created in the
        working directory.

    Returns
    -------

    """

    mask = mask_results.mask

    if mask.all():
        logging.warning(
            "No valid relative pressure ranges. BET isotherm combo plot not created."
        )
        return

    df = bet_results.iso_df
    nm = np.ma.array(bet_results.nm, mask=mask)
    c = np.ma.array(bet_results.c, mask=mask)
    err = np.ma.array(bet_results.err, mask=mask)

    err_max, err_max_idx, err_min, err_min_idx = util.max_min(err)
    c_min_err = c[err_min_idx[0], err_min_idx[1]]

    nnm_min = nm[err_min_idx[0], err_min_idx[1]]
    ppo = np.arange(0, 0.9001, 0.001)
    synth_min = 1 / (1 - ppo) - 1 / (1 + (c_min_err - 1) * ppo)
    expnnm_min = df.n / nnm_min
    err_min_i = int(err_min_idx[0] + 1)
    err_min_j = int(err_min_idx[1])
    expnnm_min_used = expnnm_min[err_min_j:err_min_i]
    ppo_expnnm_min_used = df.relp[err_min_j:err_min_i]

    f, ax1 = plt.subplots(1, 1, figsize=(10, 10))

    ax1.set_title("BET Isotherm and Experimental data")
    ax1.set_ylim(0, synth_min[-2] + 1)
    ax1.set_xlim(0, 1)
    ax1.set_ylabel("n/nm")
    ax1.set_xlabel("P/Po")
    ax1.grid(b=True, which="major", color="gray", linestyle="-")
    ax1.plot(
        ppo,
        synth_min,
        linestyle="-",
        linewidth=1,
        c="black",
        label="Theoretical isotherm",
        marker="",
    )
    ax1.plot(
        ppo_expnnm_min_used,
        expnnm_min_used,
        c="gray",
        label="Experimental isotherm - used data",
        marker="o",
        linewidth=0,
    )
    ax1.plot(
        df.relp,
        expnnm_min,
        c="grey",
        fillstyle="none",
        label="Experimental isotherm",
        marker="o",
        linewidth=0,
    )
    ax1.plot([0, 1], [1, 1], c="grey", linestyle="--", linewidth=1, marker="")
    ax1.legend(loc="upper left", framealpha=1)

    if save_file is True:
        f.savefig("isothermcomp_%s.png" % (bet_results.info), bbox_inches="tight")
        logging.info(
            "Experimental and theoretical isotherm plot saved as:\
isothermcomp_%s.png"
            % (bet_results.info)
        )
    return
