import texts
import beatmap as bt
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
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
        "About": page_about,
        "Upload data": page_upload_data,
        "Settings": page_settings,
        "BET analysis": page_analysis,
        "Summary": page_summary,
        "References": page_references
    }

    st.sidebar.title(":maple_leaf: BEaTmap")
    st.sidebar.markdown(texts.intro_sidebar)
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page](state)

    # Mandatory to avoid rollbacks w/ widgets, must be called at the end the app
    state.sync()


def page_about(state):
    r"""BEaTmap quick summary"""
    st.markdown("# :maple_leaf: BEaTmap")
    st.markdown(texts.intro)
    st.markdown("# :duck: Getting started")
    st.markdown(texts.getting_started)


def page_upload_data(state):
    r"""File uploader widget"""
    st.markdown("# :file_folder: Upload isotherm data")
    st.markdown(texts.upload_instruction)
    state.uploaded_file = st.file_uploader(
        label="Upload a CSV file", type="csv"
    )
    upload_success = st.empty()
    st.markdown("### Adsorbate area")
    st.markdown(texts.area_instruction)
    state.a_o = st.number_input(
        label="Enter adsorbate cross-sectional area (Angstrom per molecule)",
        value=state.a_o or 10
    )
    if state.uploaded_file and state.a_o:
        upload_success.success("File uploaded!")
        # Fetch and analyze the uploaded data
        state.isotherm_data = fetch_isotherm_data(state.uploaded_file, state.a_o)
        state.bet_results = fetch_bet_results(state.isotherm_data)
        # Plot isotherm data
        plot_isotherm_data(state.isotherm_data)


def page_settings(state):
    """BET model settings"""
    st.markdown("# :wrench: Settings")
    st.markdown("## Model assumptions")
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
    st.markdown("## BET calculation criteria")
    options = ["Minimum error", "Maximum data points"]
    state.criterion = st.radio(
        label="Select the BET calculation criteria:",
        options=options,
        index=options.index(state.criterion) if state.criterion else 0
    )
    if state.criterion == "Minimum error":
        state.criterion_str = "error"
    else:
        state.criterion_str = "points"


def page_analysis(state):
    """BET analysis and results"""
    st.markdown("# :straight_ruler:BET analysis")
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
    ssa_answer = bt.core.ssa_answer(
        state.bet_results, state.mask_results, state.criterion_str
    )
    st.success(f"The specific surface area value is **{ssa_answer:.2f}** $m^2/g$")
    # st.markdown(r"BET Specific Surface Area \[$\frac{m^2}{g}$\]")
    st.markdown(r"## Specific surface area heatmap")
    st.markdown(texts.ssa_instruction)
    plot_ssa_heatmap(state.bet_results, state.mask_results)


def page_summary(state):
    r"""Summary of the analysis"""
    ssa_table, c_table, ssa_ssd, c_std = bt.vis.dataframe_tables(
        state.bet_results, state.mask_results
    )
    st.markdown("# :chart_with_upwards_trend: Summary of the analysis")
    st.markdown("## Specific surface area")
    st.success(f"Standard deviation of specific surface area: **{ssa_ssd:.3f}** $m^2/g$")
    st.write(ssa_table)
    st.markdown("## BET constant (C)")
    st.success(f"Standard deviation of BET constant (C): **{c_std:.3f}**")
    st.write(c_table)


def page_references(state):
    r"""References used in BEaTmap"""
    st.markdown("# References")
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
        y=alt.Y("n (mol/g)", axis=alt.Axis(format='~e')),
        x=alt.X("P/Po", axis=alt.Axis(format='.1'))
    ).configure_mark(
        opacity=0.7
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20
    ).properties(
        title="Experimental isotherm data",
        height=400
    ).configure_title(
        fontSize=24
    )
    st.altair_chart(temp, use_container_width=True)


def plot_ssa_heatmap(bet_results, mask_results):
    r"""Plot SSA heatmap"""
    num_p = len(bet_results.iso_df.relp)
    x, y = np.meshgrid(range(num_p), range(num_p))
    temp = bet_results.ssa.copy()
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
            axis=alt.Axis(tickMinStep=2, tickCount=10, labelSeparation=10)
        ),
        y=alt.Y(
            "End relative pressure:O",
            sort=alt.EncodingSortField(
                "End relative pressure",
                order="descending"
            ),
            axis=alt.Axis(tickMinStep=2, tickCount=10, labelSeparation=10)
        ),
        color=alt.Color("SSA:Q", scale=alt.Scale(domain=[dmin, dmax], scheme="Greens"))
        # color=alt.Color('z:Q', scale=alt.Scale(range=["white", "green"]))
    ).configure_scale(
        bandPaddingInner=0.15
    ).configure_axis(
        labelFontSize=20,
        titleFontSize=20
    ).properties(
        title="Specific surface area [m^2/g]",
    ).configure_title(
        fontSize=24
    ).configure_legend(
        padding=10,
        strokeColor='gray',
        cornerRadius=10,
        labelFontSize=20,
        titleFontSize=20,
        gradientLength=250,
        tickCount=5,
        offset=40
    )
    st.altair_chart(hmap)

# # BEaTmap quick summary
# intro_state = st.sidebar.radio(
#     label="BEaTmap quick summary",
#     options=("Show app info", "Hide app info"),
#     index=0
# )

# st.markdown("# BEaTmap")
# if intro_state == "Show app info":
#     st.markdown(texts.intro)

# # File uploader widget
# st.sidebar.markdown("# Upload isotherm data")
# uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
# st.sidebar.success("Uploaded!")

# # Fetch and analyze the uploaded data
# isotherm_data = fetch_isotherm_data(uploaded_file)
# bet_results = fetch_bet_results(isotherm_data)

# # Visualize isotherm data
# st.sidebar.markdown("# Plot isotherm data")
# plot_isotherm_state = st.sidebar.radio(
#     label="Take a quick look at your data", options=("Show", "Hide"), index=1
# )

# if plot_isotherm_state == "Show":
#     st.markdown("## Isotherm data")
#     plot_bet_data(isotherm_data)

# # Model assumptions and settings
# st.sidebar.markdown("# Settings")
# settings_state = st.sidebar.radio(
#     label="Assumptions considered in the model.",
#     options=("Show settings", "Hide settings"),
#     index=1
# )

# if settings_state == "Show settings":
#     st.markdown("## Settings")
#     st.markdown("### Model assumptions")
#     checks = [st.checkbox(label=texts.checks[i], value=True) for i in range(5)]
#     points = st.slider(
#         label="Minimum number of points", min_value=2, max_value=27, value=5
#     )
#     st.markdown("### BET calculation criteria")
#     criterion = st.radio(
#         label="Select the BET calculation criteria:",
#         options=("Minimum error", "Maximum data points")
#     )
#     criterion = "error" if "error" in criterion else "points"

#     mask_results = bt.core.rouq_mask(
#         intercept=bet_results.intercept,
#         iso_df=bet_results.iso_df,
#         nm=bet_results.nm,
#         slope=bet_results.slope,
#         check1=checks[0],
#         check2=checks[1],
#         check3=checks[2],
#         check4=checks[3],
#         check5=checks[4],
#         points=points
#     )

# ssa_answer = bt.core.ssa_answer(bet_results, mask_results, criterion)
# st.success( f"The specific surface area value is **{ssa_answer:.2f}** $m^2/g$")
# # plot_ssa_heatmap(bet_results, mask_results)

# state = _get_state()
# pages = {
#     "Settings": page_settings,
#     "Analysis": page_dashboard,
# }

# st.sidebar.title(":floppy_disk: Page states")
# page = st.sidebar.radio("Select your page", tuple(pages.keys()))

# # Display the selected page with the session state
# pages[page](state)

# # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
# state.sync()


if __name__ == "__main__":
    main()
