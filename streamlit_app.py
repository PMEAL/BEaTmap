import beatmap as bt
from matplotlib import rcParams
import pandas as pd
import streamlit as st

from static import texts
from static import altair_plots as plots


state = st.session_state
st.set_page_config(
    page_title="BEaTmap",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto"
)
st.set_option("deprecation.showfileUploaderEncoding", False)
rcParams["axes.formatter.limits"] = 0, 0
rcParams["font.sans-serif"] = [
    "Lucida Sans Unicode",
    "Lucida Grande",
    "DejaVu Sans",
    "Tahoma"
]


def main():
    pages = {
        "Upload Data": page_upload,
        "BEaTmap Analysis": page_beatmap,
        "Supplemental Analysis": page_supplemental,
        "About BEaTmap": page_about,
    }

    st.sidebar.title(":maple_leaf: BEaTmap")
    st.sidebar.markdown(texts.intro_sidebar)
    page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    # Display the selected page with the session state
    pages[page]()


def page_upload():
    r"""Upload Isotherm Data"""

    st.markdown("# :duck: Getting started")
    st.markdown(texts.getting_started)

    st.markdown("## Upload Isotherm Data")
    st.markdown(texts.upload_instruction)
    file = st.file_uploader(label="Upload a CSV file", type="csv")

    if file:
        state.df = pd.read_csv(file)

    st.markdown("### Adsorbate area")
    st.markdown(texts.area_instruction)

    if "a_o" not in state:
        state.a_o = 16

    label = "Enter adsorbate cross-sectional area (Angstrom per molecule)"
    st.number_input(label=label, key="a_o")

    if ("df" in state) and ("a_o" in state):
        # Fetch and analyze the uploaded data
        state.isotherm_data = fetch_isotherm_data(file=state.df, a_o=state.a_o)
        state.bet_results = fetch_bet_results(state.isotherm_data)
        # Plot isotherm data
        plots.plot_isotherm_data(state.isotherm_data)


def page_beatmap():
    st.markdown("# :maple_leaf: BEaTmap Analysis")

    # Bypass calculations if no data is found
    if "bet_results" not in state:
        st.error("You need to upload isotherm data first!")
        return

    st.markdown("## BET model assumptions")
    if "checks" in state:
        state.check_values = [value for value in state.checks]
    else:
        state.check_values = [True] * 5
    state.checks = [
        st.checkbox(label=texts.checks[i], value=state.check_values[i])
        for i in range(5)
    ]
    label = "Minimum number of points"
    if "min_num_points" not in state:
        state.min_num_points = 5
    st.slider(label=label, min_value=2, max_value=27, key="min_num_points")

    state.mask_results = bt.core.rouq_mask(
        intercept=state.bet_results.intercept,
        iso_df=state.bet_results.iso_df,
        nm=state.bet_results.nm,
        slope=state.bet_results.slope,
        enforce_y_intercept_positive=state.checks[0],
        enforce_pressure_increasing=state.checks[1],
        enforce_absorbed_amount=state.checks[2],
        enforce_relative_pressure=state.checks[3],
        enforce_enough_datapoints=state.checks[4],
        points=state.min_num_points,
    )

    if state.mask_results.mask.all():
        msg = "Relative pressure ranges not valid. Adjust settings to proceed."
        st.error(msg)
        return

    # st.markdown(r"BET Specific Surface Area \[$\frac{m^2}{g}$\]")
    st.markdown(r"## Specific surface area heatmap")
    st.markdown(texts.ssa_instruction)
    plots.plot_ssa_heatmap(state.bet_results, state.mask_results)

    # to know if bet has been performed
    state.bet_analysis = True


def page_supplemental():
    r"""Supplemental Analysis"""
    st.markdown("# :chart_with_upwards_trend: Supplemental Analysis")

    # Bypass calculations if no analysis is found
    if "bet_analysis" not in state:
        st.error("You need to run BET Analysis first!")
        return
    # Bypass calculations if no data is found
    if "bet_results" not in state:
        st.error("You need to upload isotherm data first!")
        return
    # Bypass calculations is pressure range not valid
    if ("mask_results" in state) and (state.mask_results.mask.all()):
        msg = "Relative pressure ranges not valid. Adjust settings to proceed."
        st.error(msg)
        return

    st.markdown("## BET calculation criteria")

    if "criterion" not in state:
        state.criterion = "Minimum error"

    options = {
        "Minimum error": "error",
        "Maximum data points": "points",
        "Minimum specific surface area" : "min",
        "Maximum specific surface area": "max"
    }

    label = "Select the BET calculation criteria:"
    st.radio(label=label, options=options.keys(), key="criterion")

    ssa_answer = bt.core.ssa_answer(
        state.bet_results,
        state.mask_results,
        options[state.criterion]
    )
    st.success(f"The specific surface area value is **{ssa_answer:.2f}** $m^2/g$")

    st.markdown(r"## BET plot")
    st.markdown(texts.bet_plot_instruction)
    bet_linreg_table = plots.plot_bet(state.bet_results, state.mask_results, ssa_answer)
    bet_linreg_table.set_index(" ", inplace=True)
    st.table(bet_linreg_table)
    ssa_table, c_table, ssa_ssd, c_std = bt.vis.dataframe_tables(state.bet_results,
                                                                 state.mask_results)
    ssa_table.set_index(" ", inplace=True)
    c_table.set_index(" ", inplace=True)

    st.markdown("## Specific surface area")
    st.success(f"Standard deviation of specific surface area: **{ssa_ssd:.3f}** $m^2/g$")
    st.table(ssa_table.astype("string"))

    st.markdown("## BET constant (C)")
    st.success(f"Standard deviation of BET constant (C): **{c_std:.3f}**")
    st.table(c_table.astype("string"))

    st.markdown("## Isotherm combination plot")
    st.markdown(texts.iso_combo_instruction)
    plots.plot_isotherm_combo(state.bet_results, state.mask_results, ssa_answer)

    st.markdown("## BET minimum and maxium error plot")
    st.markdown(texts.bet_combo_instruction)
    linreg_table = plots.plot_bet_combo(state.bet_results, state.mask_results)
    linreg_table.set_index(" ", inplace=True)
    st.table(linreg_table.astype("string"))

    st.markdown("## Error heatmap")
    st.markdown(texts.err_instruction)
    plots.plot_err_heatmap(state.bet_results, state.mask_results)


def page_about():
    r"""BEaTmap quick summary"""
    st.markdown("# :maple_leaf: About BEaTmap")
    st.markdown(texts.intro)
    st.markdown("# :books: References")
    st.markdown(texts.references)


def page_references():
    r"""References used in BEaTmap"""
    st.markdown("# :books: References")
    st.markdown(texts.references)


@st.cache(allow_output_mutation=True)
def fetch_isotherm_data(file, a_o):
    r"""Extracts and returns isotherm data given a .csv file (or buffer)"""
    isotherm_data = bt.io.import_data(file=file, info="test", a_o=a_o)
    return isotherm_data


@st.cache(allow_output_mutation=True)
def fetch_bet_results(isotherm_data):
    r"""Analyzes isotherm data and returns results as a named tuple"""
    bet_results = bt.core.bet(isotherm_data.iso_df,
                              isotherm_data.a_o,
                              isotherm_data.info)
    return bet_results


if __name__ == "__main__":
    main()
