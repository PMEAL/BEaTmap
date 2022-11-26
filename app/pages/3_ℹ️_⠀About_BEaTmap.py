import pandas as pd
import streamlit as st
from matplotlib import rcParams

import beatmap as bt
from static import altair_plots as plots
from static import texts

state = st.session_state
st.set_page_config(
    page_title="About BEaTmap",
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

st.markdown("# :maple_leaf: About BEaTmap")
st.markdown(texts.intro)
st.markdown("# :books: References")
st.markdown(texts.references)
