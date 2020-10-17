import texts
import beatmap as bt
import streamlit as st

st.beta_set_page_config(
    page_title="BEaTmap",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto",
)

from matplotlib import rcParams
from stateful import _get_state
import altair_plots as plots


st.set_option("deprecation.showfileUploaderEncoding", False)
rcParams["axes.formatter.limits"] = 0, 0
rcParams["font.sans-serif"] = [
    "Lucida Sans Unicode",
    "Lucida Grande",
    "DejaVu Sans",
    "Tahoma",
]


def main():
    state = _get_state()
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
    pages[page](state)
    # Mandatory to avoid rollbacks w/ widgets must be called at the end the app
    state.sync()


def page_upload(state):
    r"""Upload Isotherm Data"""

    st.markdown("# :duck: Getting started")
    st.markdown(texts.getting_started)

    st.markdown("## Upload Isotherm Data")
    st.markdown(texts.upload_instruction)
    state.uploaded_file = st.file_uploader(label="Upload a CSV file", type="csv")
    upload_success = st.empty()
    st.markdown("### Adsorbate area")
    st.markdown(texts.area_instruction)
    state.a_o = st.number_input(
        label="Enter adsorbate cross-sectional area (Angstrom per molecule)",
        value=state.a_o or 16.2,
    )
    if state.uploaded_file and state.a_o:
        upload_success.success("File uploaded!")
        # Fetch and analyze the uploaded data
        state.isotherm_data = fetch_isotherm_data(state.uploaded_file, state.a_o)
        state.bet_results = fetch_bet_results(state.isotherm_data)
        # Plot isotherm data
        plots.plot_isotherm_data(state.isotherm_data)


def page_beatmap(state):
    st.markdown("# :maple_leaf: BEaTmap Analysis")
    st.markdown("## BET model assumptions")
    try:
        state.check_values = [value for value in state.checks]
    except TypeError:
        state.check_values = [True] * 5
    state.checks = [
        st.checkbox(label=texts.checks[i], value=state.check_values[i])
        for i in range(5)
    ]
    state.points = st.slider(
        label="Minimum number of points", min_value=2, max_value=27, value=state.points
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
        points=state.points,
    )

    if state.mask_results.mask.all():
        st.error(
            "No valid relative pressure ranges. Adjust settings to proceed with"
            + " analysis."
        )
        return

    # st.markdown(r"BET Specific Surface Area \[$\frac{m^2}{g}$\]")
    st.markdown(r"## Specific surface area heatmap")
    st.markdown(texts.ssa_instruction)
    plots.plot_ssa_heatmap(state.bet_results, state.mask_results)

    # to know if bet has been performed
    state.bet_analysis = True


def page_supplemental(state):
    r"""Supplemental Analysis"""
    st.markdown("# :chart_with_upwards_trend: Supplemental Analysis")

    # Bypass calculations if no analysis is found
    if not state.bet_analysis:
        st.error("You need to run BET Analysis first!")
        return
    # Bypass calculations if no data is found
    if not state.bet_results:
        st.error("You need to upload isotherm data first!")
        return

    if state.mask_results.mask.all():
        st.error(
            "No valid relative pressure ranges. Adjust settings to proceede with"
            + " analysis."
        )
        return

    st.markdown("## BET calculation criteria")
    options = [
        "Minimum error",
        "Maximum data points",
        "Minimum Specific Surface Area",
        "Maximum Specific Surface Area",
    ]
    state.criterion = st.radio(
        label="Select the BET calculation criteria:",
        options=options,
        index=options.index(state.criterion) if state.criterion else 0,
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
    st.success(f"The specific surface area value is **{ssa_answer:.2f}** $m^2/g$")

    st.markdown(r"## BET plot")
    st.markdown(texts.bet_plot_instruction)
    bet_linreg_table = plots.plot_bet(state.bet_results, state.mask_results, ssa_answer)
    bet_linreg_table.set_index(" ", inplace=True)
    st.write(bet_linreg_table)
    ssa_table, c_table, ssa_ssd, c_std = bt.vis.dataframe_tables(
        state.bet_results, state.mask_results
    )
    ssa_table.set_index(" ", inplace=True)
    c_table.set_index(" ", inplace=True)
    st.markdown("## Specific surface area")
    st.success(
        f"Standard deviation of specific surface area: **{ssa_ssd:.3f}** $m^2/g$"
    )
    st.write(ssa_table)
    st.markdown("## BET constant (C)")
    st.success(f"Standard deviation of BET constant (C): **{c_std:.3f}**")
    st.write(c_table)
    st.markdown("## Isotherm combination plot")
    st.markdown(texts.iso_combo_instruction)
    plots.plot_isotherm_combo(state.bet_results, state.mask_results, ssa_answer)
    st.markdown("## BET minimum and maxium error plot")
    st.markdown(texts.bet_combo_instruction)
    linreg_table = plots.plot_bet_combo(state.bet_results, state.mask_results)
    linreg_table.set_index(" ", inplace=True)
    st.write(linreg_table)
    st.markdown("## Error heatmap")
    st.markdown(texts.err_instruction)
    plots.plot_err_heatmap(state.bet_results, state.mask_results)


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


@st.cache(allow_output_mutation=True)
def fetch_bet_results(isotherm_data):
    r"""Analyzes isotherm data and returns results as a named tuple"""
    bet_results = bt.core.bet(
        isotherm_data.iso_df, isotherm_data.a_o, isotherm_data.info
    )
    return bet_results


if __name__ == "__main__":
    main()
