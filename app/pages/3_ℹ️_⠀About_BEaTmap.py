import streamlit as st
from static import texts, utils

st.set_page_config(
    page_title="About BEaTmap",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto"
)

utils.fill_sidebar()

st.markdown("# About BEaTmap")
st.markdown(texts.intro)
st.markdown("# :books: References")
st.markdown(texts.references)
