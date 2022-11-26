import pathlib
import sys

path = pathlib.Path().resolve().parent
sys.path.insert(0, str(path))

import pandas as pd
import streamlit as st
from matplotlib import rcParams
from static import altair_plots as plots
from static import texts
from static.sample_data import data

import beatmap as bt

state = st.session_state
st.set_page_config(
    page_title="Upload Data",
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


st.sidebar.title(":maple_leaf: BEaTmap")
st.sidebar.markdown(texts.intro_sidebar)

st.markdown("# :duck: Getting started")
st.markdown(texts.getting_started)

st.markdown("## Upload Isotherm Data")
st.markdown(texts.upload_instruction)
file = st.file_uploader(label="Upload a CSV file", type="csv")


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


# add a button to load "examples/vulcan_chex.csv" file when clicked
st.write("Or, load an example file (adsorption of cyclohexane on Vulcan carbon powder):")
if st.button("Load sample data"):
    state.df = pd.DataFrame(data)
    st.success("Sample data loaded!")

if file:
    state.df = pd.read_csv(file)

st.markdown("### Adsorbate area")
st.markdown(texts.area_instruction)

if "a_o" not in state:
    state.a_o = 39

label = "Enter adsorbate cross-sectional area (Angstrom per molecule)"
st.number_input(label=label, key="a_o", step=0.1, format="%.1f")

if ("df" in state) and ("a_o" in state):
    # Fetch and analyze the uploaded data
    state.isotherm_data = fetch_isotherm_data(file=state.df, a_o=state.a_o)
    state.bet_results = fetch_bet_results(state.isotherm_data)
    # Plot isotherm data
    plots.plot_isotherm_data(state.isotherm_data)
