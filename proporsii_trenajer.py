import streamlit as st

from proporsii_trenajer_module import render_proporsii_trenajer


st.set_page_config(
    page_title="Тренажер пропорций и площадей",
    page_icon="🍫",
    layout="wide",
)

render_proporsii_trenajer()
