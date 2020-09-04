import scipy as sp
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import beatmap as bt


__all__ = [
    "plot_isotherm_data",
    "plot_ssa_heatmap",
    "plot_err_heatmap",
    "plot_bet",
    "plot_isotherm_data",
    "plot_isotherm_combo",
    "plot_bet_combo",
]


figure_title_size = 18
legend_label_size = 14
legend_title_size = 16
axis_label_size = 16
axis_title_size = 16


def plot_isotherm_data(isotherm_data):
    r"""Plot BET experimental isotherm data"""
    source = pd.DataFrame(
        {"P/Po": isotherm_data.iso_df.relp, "n (mol/g)": isotherm_data.iso_df.n}
    )
    temp = (
        alt.Chart(source)
        .mark_point(filled=True)
        .encode(
            y=alt.Y("n (mol/g)", axis=alt.Axis(format="~e", tickCount=len(source) / 4)),
            x=alt.X("P/Po", axis=alt.Axis(format=".1")),
            tooltip=["n (mol/g)", "P/Po"],
        )
        .configure_mark(opacity=0.7)
        .configure_axis(
            labelFontSize=axis_label_size, titleFontSize=axis_title_size, grid=True
        )
        .properties(title="Experimental isotherm data", height=500, width=500)
        .configure_title(fontSize=figure_title_size)
        .interactive()
    )

    st.altair_chart(temp, use_container_width=True)


def plot_ssa_heatmap(bet_results, mask_results):
    r"""Plot SSA heatmap"""
    x, y = np.meshgrid(bet_results.iso_df.relp, bet_results.iso_df.relp)
    temp = np.round(bet_results.ssa.copy(), 2)
    temp[mask_results.mask] = 0
    dmin = np.amin(temp[~mask_results.mask])
    dmax = np.amax(temp[~mask_results.mask])
    source = pd.DataFrame(
        {
            "Start relative pressure": x.ravel(),
            "End relative pressure": y.ravel(),
            "SSA": temp.ravel(),
        }
    )
    hmap = (
        alt.Chart(source)
        .mark_rect(stroke="gray", strokeWidth=0.5)
        .encode(
            x=alt.X(
                "Start relative pressure:O",
                sort=alt.EncodingSortField(
                    "Start relative pressure", order="ascending",
                ),
                axis=alt.Axis(
                    tickMinStep=2, tickCount=10, labelSeparation=5, format=",.2r"
                ),
            ),
            y=alt.Y(
                "End relative pressure:O",
                sort=alt.EncodingSortField("End relative pressure", order="descending"),
                axis=alt.Axis(
                    tickMinStep=2, tickCount=10, labelSeparation=5, format=",.2r"
                ),
            ),
            color=alt.Color(
                "SSA:Q", scale=alt.Scale(domain=[dmin, dmax], scheme="Greens")
            ),
            tooltip=["SSA", "Start relative pressure", "End relative pressure"],
        )
        .configure_view(strokeWidth=0)
        .configure_scale(bandPaddingInner=0.15)
        .configure_axis(
            labelFontSize=axis_label_size,
            titleFontSize=axis_title_size,
            domainColor="white",
        )
        .properties(title="Specific surface area [m^2/g]", height=600, width=670)
        .configure_title(fontSize=figure_title_size)
        .configure_legend(
            padding=10,
            strokeColor="white",
            cornerRadius=10,
            labelFontSize=legend_label_size,
            titleFontSize=legend_title_size,
            gradientLength=250,
            tickCount=5,
            offset=40,
        )
        .interactive()
    )

    st.altair_chart(hmap, use_container_width=True)


def plot_err_heatmap(bet_results, mask_results):
    r"""Plot Error heatmap"""
    x, y = np.meshgrid(bet_results.iso_df.relp, bet_results.iso_df.relp)
    temp = np.round(bet_results.err.copy(), 2)
    temp[mask_results.mask] = 0
    dmin = np.amin(temp[~mask_results.mask])
    dmax = np.amax(temp[~mask_results.mask])
    source = pd.DataFrame(
        {
            "Start relative pressure": x.ravel(),
            "End relative pressure": y.ravel(),
            "Error": temp.ravel(),
        }
    )
    hmap = (
        alt.Chart(source)
        .mark_rect(stroke="gray", strokeWidth=0.5)
        .encode(
            x=alt.X(
                "Start relative pressure:O",
                sort=alt.EncodingSortField(
                    "Start relative pressure", order="ascending",
                ),
                axis=alt.Axis(
                    tickMinStep=2, tickCount=10, labelSeparation=5, format=",.2r"
                ),
            ),
            y=alt.Y(
                "End relative pressure:O",
                sort=alt.EncodingSortField("End relative pressure", order="descending"),
                axis=alt.Axis(
                    tickMinStep=2, tickCount=10, labelSeparation=5, format=",.2r"
                ),
            ),
            color=alt.Color(
                "Error:Q", scale=alt.Scale(domain=[dmin, dmax], scheme="Greys")
            ),
            tooltip=["Error", "Start relative pressure", "End relative pressure"],
        )
        .configure_view(strokeWidth=0)
        .configure_scale(bandPaddingInner=0.15)
        .configure_axis(
            labelFontSize=axis_label_size,
            titleFontSize=axis_title_size,
            domainColor="white",
        )
        .properties(title="Error", height=600, width=670,)
        .configure_title(fontSize=figure_title_size)
        .configure_legend(
            padding=10,
            strokeColor="white",
            cornerRadius=10,
            labelFontSize=legend_label_size,
            titleFontSize=legend_title_size,
            gradientLength=250,
            tickCount=5,
            offset=40,
        )
        .interactive()
    )

    st.altair_chart(hmap, use_container_width=True)


def plot_bet(bet_results, mask_results, ssa_answer):

    mask = mask_results.mask

    df = bet_results.iso_df
    ssa = np.ma.array(bet_results.ssa, mask=mask)

    index = bt.utils.index_of_value(ssa, ssa_answer)

    start = int(index[1])
    stop = int(index[0])

    slope, intercept, r_val, p_value, std_err = sp.stats.linregress(
        df.relp[start : stop + 1], df.bet[start : stop + 1]
    )

    liney = np.zeros(2)
    liney[0] = slope * (df.relp[start] - 0.01) + intercept
    liney[1] = slope * (df.relp[stop] + 0.01) + intercept
    linex = np.zeros(2)
    linex[0] = df.relp[start] - 0.01
    linex[1] = df.relp[stop] + 0.01

    linreg_dict = {
        " ": ["Slope", "Intercept", "r"],
        "Trendline": [slope, intercept, r_val],
    }

    linreg_table = pd.DataFrame(data=linreg_dict)

    line_source = pd.DataFrame({"P/Po": linex, "1/(n(P/Po-1))": liney})

    line = (
        alt.Chart(line_source)
        .mark_line()
        .encode(
            y=alt.Y("1/(n(P/Po-1))", axis=alt.Axis(grid=False)),
            x=alt.X("P/Po", axis=alt.Axis(format=".2", grid=False)),
        )
        .properties(title="BET plot", height=500, width=500)
    )

    line = (
        alt.layer(line)
        .configure_axis(
            labelFontSize=axis_label_size, titleFontSize=axis_title_size, grid=True
        )
        .configure_title(fontSize=figure_title_size)
    )

    data_source = pd.DataFrame(
        {
            "P/Po": df.relp[start : stop + 1],
            "1/(n(P/Po-1))": np.round(df.bet[start : stop + 1], 2),
            " ": len(df.bet[start : stop + 1])
            * [
                "Min. Error \
Experimental Data"
            ],
        }
    )

    data = (
        alt.Chart(data_source)
        .mark_point(filled=True)
        .encode(
            y=alt.Y("1/(n(P/Po-1))", axis=alt.Axis(grid=False)),
            x=alt.X("P/Po", axis=alt.Axis(format=".2", grid=False)),
            tooltip=["1/(n(P/Po-1))", "P/Po"],
        )
        .interactive()
    )

    st.altair_chart(line + data, use_container_width=True)

    return linreg_table


def plot_isotherm_combo(bet_results, mask_results, ssa_answer):
    r"""Plot BET experimental isotherm data"""

    mask = mask_results.mask

    df = bet_results.iso_df
    nm = np.ma.array(bet_results.nm, mask=mask)
    c = np.ma.array(bet_results.c, mask=mask)
    ssa = np.ma.array(bet_results.ssa, mask=mask)

    index = bt.utils.index_of_value(ssa, ssa_answer)
    start = int(index[0])
    stop = int(index[1])

    c_value = c[start, stop]

    nnm = nm[start, stop]
    ppo = np.arange(0, 0.9001, 0.001)
    synth = 1 / (1 - ppo) - 1 / (1 + (c_value - 1) * ppo)
    expnnm = df.n / nnm

    expnnm_min_used = expnnm[stop : start + 1]
    ppo_expnnm_min_used = df.relp[stop : start + 1]

    model_source = pd.DataFrame(
        {"P/Po": ppo, "n/nm": synth, " ": len(synth) * ["Model Isotherm"]}
    )
    model = (
        alt.Chart(model_source)
        .mark_line()
        .encode(
            y=alt.Y("n/nm", axis=alt.Axis(grid=False)),
            x=alt.X("P/Po", axis=alt.Axis(format=".2", grid=False)),
            color=" ",
        )
        .properties(title="Experimental data and model isotherm", height=480, width=622)
    )

    experimental_source = pd.DataFrame(
        {
            "P/Po": bet_results.iso_df.relp,
            "n/nm": np.round(expnnm, 2),
            " ": len(expnnm) * ["Experimental Data"],
        }
    )
    experimental = (
        alt.Chart(experimental_source)
        .mark_point()
        .encode(
            y=alt.Y("n/nm", axis=alt.Axis(grid=False)),
            x=alt.X("P/Po", axis=alt.Axis(format=".2", grid=False)),
            opacity=" ",
            tooltip=["n/nm", "P/Po"],
        )
        .interactive()
    )

    used_source = pd.DataFrame(
        {
            "P/Po": ppo_expnnm_min_used,
            "n/nm": expnnm_min_used,
            " ": len(expnnm_min_used) * ["Min. Error Experimental Data"],
        }
    )
    experimental_used = (
        alt.Chart(used_source)
        .mark_point(filled=True)
        .encode(
            y=alt.Y("n/nm", axis=alt.Axis(grid=False)),
            x=alt.X("P/Po", axis=alt.Axis(format=".2", grid=False)),
            shape=" ",
        )
    )

    chart = (
        alt.layer(model, experimental, experimental_used)
        .configure_axis(
            labelFontSize=axis_label_size, titleFontSize=axis_title_size, grid=True
        )
        .configure_title(fontSize=figure_title_size)
        .configure_legend(labelFontSize=legend_label_size)
    )

    st.altair_chart(chart)


def plot_bet_combo(bet_results, mask_results):

    mask = mask_results.mask

    df = bet_results.iso_df
    err = np.ma.array(bet_results.err, mask=mask)

    err_max, err_max_idx, err_min, err_min_idx = bt.utils.max_min(err)

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

    slope_max, intercept_max, r_val_max, p_value_max, std_err_max = sp.stats.linregress(
        df.relp[max_start : max_stop + 1], df.bet[max_start : max_stop + 1]
    )
    max_liney = np.zeros(2)
    max_liney[0] = slope_max * (df.relp[max_start] - 0.01) + intercept_max
    max_liney[1] = slope_max * (df.relp[max_stop] + 0.01) + intercept_max
    max_linex = np.zeros(2)
    max_linex[0] = df.relp[max_start] - 0.01
    max_linex[1] = df.relp[max_stop] + 0.01

    linreg_dict = {
        " ": ["Slope", "Intercept", "r"],
        "Min. Error Trendline": [slope, intercept, r_val],
        "Max. Error Trendline": [slope_max, intercept_max, r_val_max],
    }

    linreg_table = pd.DataFrame(data=linreg_dict)

    minline_source = pd.DataFrame({"P/Po": min_linex, "1/(n(P/Po-1))": min_liney})

    minline = (
        alt.Chart(minline_source)
        .mark_line()
        .encode(
            y=alt.Y("1/(n(P/Po-1))", axis=alt.Axis(grid=False)),
            x=alt.X("P/Po", axis=alt.Axis(format=".2", grid=False)),
        )
        .properties(title="Minimum and maximum error BET plot", height=480, width=622)
    )

    mindata_source = pd.DataFrame(
        {
            "P/Po": df.relp[min_start : min_stop + 1],
            "1/(n(P/Po-1))": np.round(df.bet[min_start : min_stop + 1], 2),
            " ": len(df.bet[min_start : min_stop + 1])
            * [
                "Min. Error \
Experimental Data"
            ],
        }
    )

    mindata = (
        alt.Chart(mindata_source)
        .mark_point(filled=True)
        .encode(
            y=alt.Y("1/(n(P/Po-1))", axis=alt.Axis(grid=False)),
            x=alt.X("P/Po", axis=alt.Axis(format=".2", grid=False)),
            shape=" ",
            tooltip=["1/(n(P/Po-1))", "P/Po"],
        )
        .interactive()
    )

    maxline_source = pd.DataFrame({"P/Po": max_linex, "1/(n(P/Po-1))": max_liney})

    maxline = (
        alt.Chart(maxline_source)
        .mark_line(color="grey")
        .encode(
            y=alt.Y("1/(n(P/Po-1))", axis=alt.Axis(grid=False)),
            x=alt.X("P/Po", axis=alt.Axis(format=".2", grid=False)),
        )
    )

    maxdata_source = pd.DataFrame(
        {
            "P/Po": df.relp[max_start : max_stop + 1],
            "1/(n(P/Po-1))": np.round(df.bet[max_start : max_stop + 1], 2),
            " ": len(df.bet[max_start : max_stop + 1])
            * [
                "Max. Error \
Experimental Data"
            ],
        }
    )

    maxdata = (
        alt.Chart(maxdata_source)
        .mark_point(color="grey")
        .encode(
            y=alt.Y("1/(n(P/Po-1))", axis=alt.Axis(grid=False)),
            x=alt.X("P/Po", axis=alt.Axis(format=".2", grid=False)),
            opacity=" ",
            tooltip=["1/(n(P/Po-1))", "P/Po"],
        )
        .interactive()
    )

    chart = (
        alt.layer(minline, mindata, maxline, maxdata)
        .configure_axis(
            labelFontSize=axis_label_size, titleFontSize=axis_title_size, grid=True
        )
        .configure_title(fontSize=figure_title_size)
        .configure_legend(labelFontSize=legend_label_size)
    )

    st.altair_chart(chart)

    return linreg_table
