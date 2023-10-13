import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import seaborn as sns
from matplotlib.ticker import AutoMinorLocator, MaxNLocator

from beatmap import utils as util

log = util.get_logger(__name__)

__all__ = [
    "experimental_data_plot",
    "ssa_heatmap",
    "err_heatmap",
    "bet_combo_plot",
    "iso_combo_plot",
]


def experimental_data_plot(isotherm_data, save_file=False):
    """Creates a scatter plot of experimental data.

    Typical isotherm presentation where x-axis is relative pressure,
    y-axis is specific amount adsorbed.

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
    None

    """
    df = isotherm_data.iso_df
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    # ax.set_xlim(0, 1.0)
    # ax.set_ylim(0, df['n'].iloc[-1] * 1.05)
    ax.set_title("experimental isotherm")
    ax.set_ylabel("n [mol/g]")
    ax.set_xlabel("P/Po")
    ax.grid(which="major", color="gray", linestyle=":")
    ax.plot(df.relp, df.n, c="k", marker="o", markerfacecolor="w", linewidth=0)

    if save_file is True:
        fig.savefig(f"expdata_{isotherm_data.info}.png", bbox_inches="tight")
        log.info(f"Experimental data plot saved as: expdata_{isotherm_data.info}.png")


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
    save_file : bool
        When save_file = True a png of the figure is created in the
        working directory.
    gradient : str
        Color gradient for heatmap, must be a vaild color gradient name
        in the seaborn package.

    Returns
    -------
    None

    """
    mask = mask_results.mask

    if mask.all():
        log.warning("No valid relative pressure range found; Aborting.")
        return

    df = bet_results.iso_df

    # creating a masked array of ssa values
    ssa = np.ma.array(bet_results.ssa, mask=mask)

    # finding max and min sa to normalize heatmap colours
    ssamax, ssa_max_idx, ssamin, ssa_min_idx = util.max_min(ssa)
    hm_labels = round(df.relp * 100, 1)
    fig, ax = plt.subplots(figsize=(6, 6))
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
        linecolor="whitesmoke",
        cbar_kws={"shrink": 0.73, "aspect": len(df.relp)},
    )
    ax.invert_yaxis()
    ax.set_title(r"specific surface area (m$^2$/g)")
    ax.set_xlabel("start relative pressure")
    ax.set_ylabel("end relative pressure")

    # only keep a few labels on each axis for readability
    num_ticks = 15
    xticks = np.linspace(0, len(hm_labels) - 1, num_ticks, dtype=int)
    yticks = np.linspace(0, len(hm_labels) - 1, num_ticks, dtype=int)

    # Set the ticks on the axes
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)

    # Format labels
    xticklabels = [f"{val:.0f}" for val in hm_labels[xticks]]
    yticklabels = [f"{val:.0f}" for val in hm_labels[yticks]]    

    # Set the tick labels with desired rotation and horizontal alignment
    ax.set_xticklabels(labels=xticklabels, rotation=45, ha='right')
    ax.set_yticklabels(labels=yticklabels, rotation=45, ha='right')

    # add borders
    for _, spine in ax.spines.items():
        spine.set_visible(True)

    fig.tight_layout()
    
    if save_file is True:
        fig.savefig("ssa_heatmap_%s.png" % (bet_results.info), bbox_inches="tight")
        log.info(f"Specific surface area heatmap saved as: ssa_heatmap_{bet_results.info}.png")
    
    return fig, ax


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
    None

    """
    mask = mask_results.mask

    if mask.all():
        log.warning("No valid relative pressure ranges found; Aborting.")
        return

    df = bet_results.iso_df

    # creating a masked array of error values
    err = np.ma.array(bet_results.err, mask=mask)

    errormax, error_max_idx, errormin, error_min_idx = util.max_min(err)

    hm_labels = round(df.relp * 100, 1)
    fig, (ax) = plt.subplots(1, 1, figsize=(6, 6))
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
        linecolor="whitesmoke",
        cbar_kws={"shrink": 0.73, "aspect": len(df.relp)},
    )
    ax.invert_yaxis()
    ax.set_title("isotherm error")
    ax.set_xlabel("start relative pressure")
    ax.set_ylabel("end relative pressure")

    # only keep a few labels on each axis for readability
    num_ticks = 15
    xticks = np.linspace(0, len(hm_labels) - 1, num_ticks, dtype=int)
    yticks = np.linspace(0, len(hm_labels) - 1, num_ticks, dtype=int)

    # Set the ticks on the axes
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)

    # Format labels
    xticklabels = [f"{val:.0f}" for val in hm_labels[xticks]]
    yticklabels = [f"{val:.0f}" for val in hm_labels[yticks]]    

    # Set the tick labels with desired rotation and horizontal alignment
    ax.set_xticklabels(labels=xticklabels, rotation=45, ha='right')
    ax.set_yticklabels(labels=yticklabels, rotation=45, ha='right')

    fig.tight_layout()

    # add borders
    for _, spine in ax.spines.items():
        spine.set_visible(True)

    if save_file is True:
        fig.savefig("error_heatmap_%s.png" % (bet_results.info), bbox_inches="tight")
        log.info("Error heatmap saved as: error_heatmap_%s.png" % (bet_results.info))

    return fig, ax


def bet_combo_plot(bet_results, mask_results, save_file=True):
    """Creates a BET plots for the minimum and maxium error data sets.

    Only datapoints in the minimum and maximum error data sets are plotted.
    Equation for best fit line and R2 value are annotated on plot.

    Parameters
    ----------
    bet_results : namedtuple
        Namedtuple where the bet_results.iso_df element is used to
        create a plot of isotherm BET values.
    mask_results : namedtuple
        The mask_results.mask element is used to mask the BET results so that
        only valid results are displayed.
    save_file : bool
        When save_file = True a png of the figure is created in the
        working directory.

    Returns
    -------
    figure : matplotlib figure
        Figure object containing the plot.
    ax : matplotlib axes
        Axes object containing the plot.

    """
    mask = mask_results.mask

    if mask.all():
        log.warning("No valid relative pressure ranges; Aborting.")
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

    slope_max, intercept_max, r_value_max, p_value_max, std_err_max = sp.stats.linregress(
        df.relp[max_start : max_stop + 1], df.bet[max_start : max_stop + 1]
    )
    max_liney = np.zeros(2)
    max_liney[0] = slope_max * (df.relp[max_start] - 0.01) + intercept_max
    max_liney[1] = slope_max * (df.relp[max_stop] + 0.01) + intercept_max
    max_linex = np.zeros(2)
    max_linex[0] = df.relp[max_start] - 0.01
    max_linex[1] = df.relp[max_stop] + 0.01

    figure, ax = plt.subplots(1, figsize=(6, 5))

    ax.set_title("BET plot")
    # ax.set_xlim(0, max(min_linex[1], max_linex[1]) * 1.1)
    ax.set_ylabel("1/[n(P/Po-1)]")
    # ax.set_ylim(0, max(min_liney[1] * 1.1, max_liney[1] * 1.1))
    ax.set_xlabel("P/Po")
    ax.grid(which="major", color="gray", linestyle="-", alpha=0.1)

    ax.plot(
        df.relp[min_start : min_stop + 1],
        df.bet[min_start : min_stop + 1],
        # label="min error (exp.)",
        c="blue",
        marker="o",
        linewidth=0,
        fillstyle="none",
    )

    ax.plot(
        min_linex,
        min_liney,
        color="blue",
        label="min error"
    )
    
    ax.plot(
        df.relp[max_start : max_stop + 1],
        df.bet[max_start : max_stop + 1],
        # label="max error (exp.)",
        c="red",
        marker="x",
        linewidth=0,
    )
    
    ax.plot(
        max_linex,
        max_liney,
        color="red",
        linestyle="--",
        label="max error",
    )
    
    ax.annotate(
        f"min error fit \n    m = {slope:.3f}\n    b = {intercept:.3f}\n    R = {r_val:.3f}\n\n"
        f"max error fit \n    m = {slope_max:.3f}\n    b = {intercept_max:.3f}\n    R = {r_value_max:.3f}",
        bbox=dict(boxstyle="round, pad=0.5", fc="white", ec="gray", alpha=0.0),
        textcoords="axes fraction",
        xytext=(1.075, 0.35),
        xy=(df.relp[min_stop], df.bet[min_start]),
        size=11,
    )
    ax.legend(loc="upper left", framealpha=0.0, borderpad=0.5)

    if save_file is True:
        figure.savefig("betplot_%s.png" % (bet_results.info), bbox_inches="tight")
        log.info("BET plot saved as: betplot_%s.png" % (bet_results.info))

    return ax.figure, ax


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
    figure : matplotlib figure
        Figure object containing the plot.
    ax : matplotlib axes
        Axes object containing the plot.

    """
    mask = mask_results.mask

    if mask.all():
        log.warning("No valid relative pressure ranges; Aborting.")
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

    f, ax = plt.subplots(1, 1, figsize=(6, 5))

    ax.set_title("BET isotherm vs. experiment")
    ax.set_ylim(0, synth_min[-2] + 1)
    ax.set_xlim(0, 1)
    ax.set_ylabel("n/nm")
    ax.set_xlabel("P/Po")
    ax.grid(which="major", color="gray", linestyle="-", alpha=0.1)
    ax.plot(
        ppo,
        synth_min,
        linestyle="-",
        linewidth=1,
        c="blue",
        label="isotherm (model)",
        marker="",
    )
    ax.plot(
        ppo_expnnm_min_used,
        expnnm_min_used,
        c="lightgreen",
        label="isotherm (exp); used data",
        marker="o",
        linewidth=0,
    )
    ax.plot(
        df.relp,
        expnnm_min,
        c="grey",
        fillstyle="none",
        label="isotherm (exp)",
        marker="o",
        linewidth=0,
    )
    ax.plot([0, 1], [1, 1], c="grey", linestyle="--", linewidth=1, marker="")
    ax.legend(loc="upper left", framealpha=0)

    if save_file is True:
        f.savefig("isothermcomp_%s.png" % (bet_results.info), bbox_inches="tight")
        log.info(f"Experimental and theoretical isotherm plot saved as: isothermcomp_{bet_results.info}.png")
    
    return ax.figure, ax
