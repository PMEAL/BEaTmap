import pandas as pd
import streamlit as st
from matplotlib import rcParams

import beatmap as bt
from static import altair_plots as plots
from static import texts

state = st.session_state
st.set_page_config(
    page_title="Supplemental Analysis",
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


if __name__ == "__main__":
    main()
