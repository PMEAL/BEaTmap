import texts
import beatmap as bt
import pandas as pd
import numpy as np
import scipy as sp
import streamlit as st
from matplotlib import rcParams
from stateful import *
import altair as alt


st.set_option('deprecation.showfileUploaderEncoding', False)
rcParams["axes.formatter.limits"] = 0, 0
rcParams['font.sans-serif'] = [
    'Lucida Sans Unicode', 'Lucida Grande', 'DejaVu Sans', 'Tahoma'
]


def main():
    state = _get_state()
    pages = {
        "Upload Data": page_upload,
        "BEaTmap Analysis": page_beatmap,
        "Supplimental Analysis": page_supplimental,
        "About BEaTmap": page_about
        # "References": page_references
    }

    st.sidebar.title(":maple_leaf: BEaTmap")
    st.sidebar.markdown(texts.intro_sidebar)
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks w/ widgets
    # must be called at the end the app
    state.sync()


def page_upload(state):
    r"""Upload Isotherm Data"""

    st.markdown("# :duck: Getting started")
    st.markdown(texts.getting_started)

    st.markdown("## Upload Isotherm Data")
    st.markdown(texts.upload_instruction)
    state.uploaded_file = st.file_uploader(
        label="Upload a CSV file", type="csv"
    )
    upload_success = st.empty()
    st.markdown("### Adsorbate area")
    st.markdown(texts.area_instruction)
    state.a_o = st.number_input(
        label="Enter adsorbate cross-sectional area (Angstrom per molecule)",
        value=state.a_o or 16.2
    )
    if state.uploaded_file and state.a_o:
        upload_success.success("File uploaded!")
        # Fetch and analyze the uploaded data
        state.isotherm_data = fetch_isotherm_data(state.uploaded_file,
                                                  state.a_o)
        state.bet_results = fetch_bet_results(state.isotherm_data)
        # Plot isotherm data
        plot_isotherm_data(state.isotherm_data)


def page_beatmap(state):
    st.markdown("# :maple_leaf: BEaTmap Analysis")
    st.markdown("## BET model assumptions")
    try:
        state.check_values = [value for value in state.checks]
    except TypeError:
        state.check_values = [True] * 5
    state.checks = [
        st.checkbox(
            label=texts.checks[i], value=state.check_values[i]
        ) for i in range(5)
    ]
    state.points = st.slider(
        label="Minimum number of points",
        min_value=2,
        max_value=27,
        value=state.points
    )

    # Bypass calculations if no data is found
    if not state.bet_results:
        st.error("You need to upload isotherm data first!")
        return
    state.mask_results = bt.core.rouq_mask(
        intercept=state.bet_results.intercept,
        iso_df=state.bet_results.iso_df,
        nm=state.bet_results.nm,
        slope=state.bet_results.slope,
        check1=state.checks[0],
        check2=state.checks[1],
        check3=state.checks[2],
        check4=state.checks[3],
        check5=state.checks[4],
        points=state.points
    )

    if state.mask_results.mask.all() == True:
        st.error("No valid relative pressure ranges. \
Adjust settings to proceede with analysis.")
        return

    # st.markdown(r"BET Specific Surface Area \[$\frac{m^2}{g}$\]")
    st.markdown(r"## Specific surface area heatmap")
    st.markdown(texts.ssa_instruction)
    plot_ssa_heatmap(state.bet_results, state.mask_results)


def page_supplimental(state):
    r"""Supplimental Analysis"""
    st.markdown("# :chart_with_upwards_trend: Supplimental Analysis")
    # Bypass calculations if no data is found
    if not state.bet_results:
        st.error("You need to upload isotherm data first!")
        return

    if state.mask_results.mask.all() == True:
        st.error("No valid relative pressure ranges. \
Adjust settings to proceede with analysis.")
        return

    st.markdown("## BET calculation criteria")
    options = ["Minimum error", "Maximum data points",
               "Minimum Specific Surface Area",
               "Maximum Specific Surface Area"]
    state.criterion = st.radio(
        label="Select the BET calculation criteria:",
        options=options,
        index=options.index(state.criterion) if state.criterion else 0
    )
    if state.criterion == "Minimum error":
        state.criterion_str = "error"
    if state.criterion == "Maximum data points":
        state.criterion_str = "points"
    if state.criterion == "Minimum Specific Surface Area":
        state.criterion_str = "min"
    if state.criterion == "Maximum Specific Surface Area":
        state.criterion_str = "max"

    ssa_answer = bt.core.ssa_answer(
        state.bet_results, state.mask_results, state.criterion_str
    )
    st.success(f"The specific surface area value is \
**{ssa_answer:.2f}** $m^2/g$")

    st.markdown(r"## BET plot")

    ssa_table, c_table, ssa_ssd, c_std = bt.vis.dataframe_tables(
        state.bet_results, state.mask_results
    )
    ssa_table.set_index(' ', inplace=True)
    c_table.set_index(' ', inplace=True)
    st.markdown("## Specific surface area")
    st.success(f"Standard deviation of specific surface area: \
**{ssa_ssd:.3f}** $m^2/g$")
    st.write(ssa_table)
    st.markdown("## BET constant (C)")
    st.success(f"Standard deviation of BET constant (C): **{c_std:.3f}**")
    st.write(c_table)
    st.markdown("## Isotherm combination plot")
    st.markdown(texts.iso_combo_instruction)
    plot_isotherm_combo(state.bet_results, state.mask_results)
    st.markdown("## BET minimum and maxium error plot")
    st.markdown(texts.bet_combo_instruction)
    linreg_table = plot_bet_combo(state.bet_results, state.mask_results)
    linreg_table.set_index(' ', inplace=True)
    st.write(linreg_table)
    st.markdown("## Error heatmap")
    st.markdown(texts.err_instruction)
    plot_err_heatmap(state.bet_results, state.mask_results)


def page_about(state):
    r"""BEaTmap quick summary"""
    st.markdown("# :maple_leaf: About BEaTmap")
    st.markdown(texts.intro)
    st.markdown("# :books: References")
    st.markdown(texts.references)


def page_references(state):
    r"""References used in BEaTmap"""
    st.markdown("# :books: References")
    st.markdown(texts.references)


@st.cache(allow_output_mutation=True)
def fetch_isotherm_data(uploaded_file, a_o):
    r"""Extracts and returns isotherm data given a .csv file (or buffer)"""
    isotherm_data = bt.io.import_data(uploaded_file, info="test", a_o=a_o)
    return isotherm_data


@st.cache(allow_output_mutation=False)
def fetch_bet_results(isotherm_data):
    r"""Analyzes isotherm data and returns results as a named tuple"""
    bet_results = bt.core.bet(
        isotherm_data.iso_df,
        isotherm_data.a_o,
        isotherm_data.info
    )
    return bet_results


def plot_isotherm_data(isotherm_data):
    r"""Plot BET experimental isotherm data"""
    source = pd.DataFrame(
        {
            "P/Po": isotherm_data.iso_df.relp,
            "n (mol/g)": isotherm_data.iso_df.n
        }
    )
    temp = alt.Chart(source).mark_point().encode(
        y=alt.Y("n (mol/g)", axis=alt.Axis(format='~e',
                                           tickCount=len(source)/4)),
        x=alt.X("P/Po", axis=alt.Axis(format='.1'))
    ).configure_mark(
        opacity=0.7
    ).configure_axis(
        labelFontSize=16,
        titleFontSize=16,
        grid=False
    ).properties(
        title="Experimental isotherm data",
        height=600,
        width=600
    ).configure_title(
        fontSize=18
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
            "SSA": temp.ravel()
        }
    )
    hmap = alt.Chart(source).mark_rect(stroke='gray', strokeWidth=0.5).encode(
        x=alt.X(
            "Start relative pressure:O",
            sort=alt.EncodingSortField(
                "Start relative pressure",
                order="ascending",
            ),
            axis=alt.Axis(tickMinStep=2, tickCount=10, labelSeparation=5,
                          format=',.2r')
        ),
        y=alt.Y(
            "End relative pressure:O",
            sort=alt.EncodingSortField(
                "End relative pressure",
                order="descending"
            ),
            axis=alt.Axis(tickMinStep=2, tickCount=10, labelSeparation=5,
                          format=',.2r')
        ),
        color=alt.Color("SSA:Q", scale=alt.Scale(domain=[dmin, dmax],
                                                 scheme="Greens")),
        tooltip=['SSA', 'Start relative pressure', 'End relative pressure']
    ).configure_view(
        strokeWidth=0
    ).configure_scale(
        bandPaddingInner=0.15
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20,
        domainColor='white'
    ).properties(
        title="Specific surface area [m^2/g]",
        height=600,
        width=670
    ).configure_title(
        fontSize=24
    ).configure_legend(
        padding=10,
        strokeColor='white',
        cornerRadius=10,
        labelFontSize=20,
        titleFontSize=20,
        gradientLength=250,
        tickCount=5,
        offset=40
    ).interactive()

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
            "Error": temp.ravel()
        }
    )
    hmap = alt.Chart(source).mark_rect(stroke='gray', strokeWidth=0.5).encode(
        x=alt.X(
            "Start relative pressure:O",
            sort=alt.EncodingSortField(
                "Start relative pressure",
                order="ascending",
            ),
            axis=alt.Axis(tickMinStep=2, tickCount=10, labelSeparation=5,
                          format=',.2r')
        ),
        y=alt.Y(
            "End relative pressure:O",
            sort=alt.EncodingSortField(
                "End relative pressure",
                order="descending"
            ),
            axis=alt.Axis(tickMinStep=2, tickCount=10, labelSeparation=5,
                          format=',.2r')
        ),
        color=alt.Color("Error:Q", scale=alt.Scale(domain=[dmin, dmax],
                                                   scheme="Greys")),
        tooltip=['Error', 'Start relative pressure', 'End relative pressure']
    ).configure_view(
        strokeWidth=0
    ).configure_scale(
        bandPaddingInner=0.15
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20,
        domainColor='white'
    ).properties(
        title="Error",
        height=600,
        width=670,
    ).configure_title(
        fontSize=24
    ).configure_legend(
        padding=10,
        strokeColor='white',
        cornerRadius=10,
        labelFontSize=20,
        titleFontSize=20,
        gradientLength=250,
        tickCount=5,
        offset=40
    ).interactive()

    st.altair_chart(hmap, use_container_width=True)


def plot_isotherm_combo(bet_results, mask_results):
    r"""Plot BET experimental isotherm data"""

    mask = mask_results.mask

    df = bet_results.iso_df
    nm = np.ma.array(bet_results.nm, mask=mask)
    c = np.ma.array(bet_results.c, mask=mask)
    err = np.ma.array(bet_results.err, mask=mask)

    err_max, err_max_idx, err_min, err_min_idx = bt.utils.max_min(err)
    c_min_err = c[err_min_idx[0], err_min_idx[1]]

    nnm_min = nm[err_min_idx[0], err_min_idx[1]]
    ppo = np.arange(0, .9001, .001)
    synth_min = 1 / (1 - ppo) - 1 / (1 + (c_min_err - 1) * ppo)
    expnnm_min = df.n / nnm_min

    err_min_i = int(err_min_idx[0] + 1)
    err_min_j = int(err_min_idx[1])
    expnnm_min_used = expnnm_min[err_min_j:err_min_i]
    ppo_expnnm_min_used = df.relp[err_min_j:err_min_i]

    model_source = pd.DataFrame(
        {
            "P/Po": ppo,
            "n/nm": synth_min,
            " ": len(synth_min) * ['Model Isotherm']
        }
    )
    model = alt.Chart(model_source).mark_line().encode(
        y=alt.Y("n/nm", axis=alt.Axis(grid=False)),
        x=alt.X("P/Po", axis=alt.Axis(format='.2', grid=False)),
        color=" "
        ).properties(
        title="Experimental isotherm data",
        height=480,
        width=622
        )

    experimental_source = pd.DataFrame(
        {
            "P/Po": bet_results.iso_df.relp,
            "n/nm": np.round(expnnm_min, 2),
            " ": len(expnnm_min) * ['Experimental Data']
        }
    )
    experimental = alt.Chart(experimental_source).mark_point().encode(
        y=alt.Y("n/nm", axis=alt.Axis(grid=False)),
        x=alt.X("P/Po", axis=alt.Axis(format='.2', grid=False)),
        opacity=" ",
        tooltip=['n/nm', 'P/Po']).interactive()

    used_source = pd.DataFrame(
        {
            "P/Po": ppo_expnnm_min_used,
            "n/nm": expnnm_min_used,
            " ": len(expnnm_min_used) * ['Min. Error Experimental Data']
        }
    )
    experimental_used = alt.Chart(used_source).mark_point(filled=True).encode(
        y=alt.Y("n/nm", axis=alt.Axis(grid=False)),
        x=alt.X("P/Po", axis=alt.Axis(format='.2', grid=False)),
        shape=" ")

    st.altair_chart(model + experimental + experimental_used)


def plot_bet_combo(bet_results, mask_results):

    mask = mask_results.mask

    df = bet_results.iso_df
    err = np.ma.array(bet_results.err, mask=mask)

    err_max, err_max_idx, err_min, err_min_idx = bt.utils.max_min(err)

    min_start = int(err_min_idx[1])
    min_stop = int(err_min_idx[0])
    max_start = int(err_max_idx[1])
    max_stop = int(err_max_idx[0])

    slope, intercept, r_val, p_value, std_err =\
        sp.stats.linregress(df.relp[min_start: min_stop + 1],
                            df.bet[min_start:min_stop + 1])

    min_liney = np.zeros(2)
    min_liney[0] = slope * (df.relp[min_start] - .01) + intercept
    min_liney[1] = slope * (df.relp[min_stop] + .01) + intercept
    min_linex = np.zeros(2)
    min_linex[0] = df.relp[min_start] - .01
    min_linex[1] = df.relp[min_stop] + .01

    slope_max, intercept_max, r_val_max, p_value_max, std_err_max = \
        sp.stats.linregress(df.relp[max_start: max_stop + 1],
                            df.bet[max_start: max_stop + 1])
    max_liney = np.zeros(2)
    max_liney[0] = slope_max * (df.relp[max_start] - .01) + intercept_max
    max_liney[1] = slope_max * (df.relp[max_stop] + .01) + intercept_max
    max_linex = np.zeros(2)
    max_linex[0] = df.relp[max_start] - .01
    max_linex[1] = df.relp[max_stop] + .01

    linreg_dict = {' ': ['Slope', 'Intercept', 'r'],
                   'Min. Error Trendline': [slope, intercept, r_val],
                   'Max. Error Trendline':
                       [slope_max, intercept_max, r_val_max]}

    linreg_table = pd.DataFrame(data=linreg_dict)

    minline_source = pd.DataFrame(
        {
            "P/Po": min_linex,
            "1/(n(P/Po-1))": min_liney
        }
    )

    minline = alt.Chart(minline_source).mark_line().encode(
        y=alt.Y("1/(n(P/Po-1))", axis=alt.Axis(grid=False)),
        x=alt.X("P/Po", axis=alt.Axis(format='.2', grid=False))).properties(
        title="Minimum and maximum error BET plot",
        height=480,
        width=622
        )

    mindata_source = pd.DataFrame(
        {
            "P/Po": df.relp[min_start:min_stop + 1],
            "1/(n(P/Po-1))": np.round(df.bet[min_start:min_stop + 1], 2),
            " ": len(df.bet[min_start:min_stop + 1]) * ['Min. Error \
Experimental Data']
        }
    )

    mindata = alt.Chart(mindata_source).mark_point(filled=True).encode(
        y=alt.Y("1/(n(P/Po-1))", axis=alt.Axis(grid=False)),
        x=alt.X("P/Po", axis=alt.Axis(format='.2', grid=False)),
        shape=" ",
        tooltip=['1/(n(P/Po-1))', 'P/Po']).interactive()

    maxline_source = pd.DataFrame(
        {
            "P/Po": max_linex,
            "1/(n(P/Po-1))": max_liney
        }
    )

    maxline = alt.Chart(maxline_source).mark_line(color='grey').encode(
        y=alt.Y("1/(n(P/Po-1))", axis=alt.Axis(grid=False)),
        x=alt.X("P/Po", axis=alt.Axis(format='.2', grid=False)))

    maxdata_source = pd.DataFrame(
        {
            "P/Po": df.relp[max_start:max_stop + 1],
            "1/(n(P/Po-1))": np.round(df.bet[max_start:max_stop + 1], 2),
            " ": len(df.bet[max_start:max_stop + 1]) * ['Max. Error \
Experimental Data']
        }
    )

    maxdata = alt.Chart(maxdata_source).mark_point(color='grey').encode(
        y=alt.Y("1/(n(P/Po-1))", axis=alt.Axis(grid=False)),
        x=alt.X("P/Po", axis=alt.Axis(format='.2', grid=False)),
        opacity=" ",
        tooltip=['1/(n(P/Po-1))', 'P/Po']).interactive()

    st.altair_chart(minline + mindata + maxline + maxdata)

    return linreg_table


if __name__ == "__main__":
    main()
