import pandas as pd
import streamlit as st
from matplotlib import rcParams
from static import altair_plots as plots
from static import texts

import beatmap as bt

st.set_page_config(
    page_title="References",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto"
)

st.sidebar.title(":maple_leaf: BEaTmap")
st.sidebar.markdown(texts.intro_sidebar)

st.markdown("# :books: References")
st.markdown(texts.references)
