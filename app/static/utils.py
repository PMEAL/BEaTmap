import streamlit as st

from . import texts

logo_url = "https://raw.githubusercontent.com/PMEAL/beatmap/main/docs/source/_static/logo-light-mode.png"


def fill_sidebar():
    """Fill the sidebar with the BEaTmap logo and intro text"""
    st.sidebar.image(logo_url, width=200)
    # st.sidebar.title(":maple_leaf: BEaTmap")
    st.sidebar.markdown(texts.intro_sidebar)


def fill_header():
    """Fill the header with the BEaTmap logo"""
    st.image(logo_url, width=300)
