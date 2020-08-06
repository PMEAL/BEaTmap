import texts
import beatmap as bt
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rcParams
from stateful import *


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


def page_upload_data(state):
    r"""File uploader widget"""
    st.sidebar.markdown("# Upload isotherm data")
    state.uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
    if state.uploaded_file:
        upload_success = st.sidebar.success("File uploaded!")
        # Fetch and analyze the uploaded data
        state.isotherm_data = fetch_isotherm_data(state.uploaded_file)
        state.bet_results = fetch_bet_results(state.isotherm_data)
        # Plot isotherm data
        st.markdown("# Isotherm data")
        plot_bet_data(state.isotherm_data)


def page_settings(state):
    """BET model settings"""
    st.markdown("# Settings")
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


@st.cache(allow_output_mutation=True)
def fetch_isotherm_data(uploaded_file):
    r"""Extracts and returns isotherm data given a .csv file (or buffer)"""
    isotherm_data = bt.io.import_data(uploaded_file, info="test", a_o=10.0)
    return isotherm_data


@st.cache()
def fetch_bet_results(isotherm_data):
    r"""Analyzes isotherm data and returns results as a named tuple"""
    bet_results = bt.core.bet(
        isotherm_data.iso_df,
        isotherm_data.a_o,
        isotherm_data.info
    )
    return bet_results


def plot_bet_data(isotherm_data):
    r"""Plot BET experimental isotherm data"""
    fig, ax = bt.vis.experimental_data_plot(isotherm_data, save_file=False)
    fig.set_size_inches(7, 4.5)
    st.pyplot(dpi=300, fig=fig)


def plot_ssa_heatmap(bet_results, mask_results):
    r"""Plot SSA heatmap"""
    fig, ax = bt.vis.ssa_heatmap(bet_results, mask_results, save_file=False)
    st.pyplot(dpi=300, fig=fig)


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
