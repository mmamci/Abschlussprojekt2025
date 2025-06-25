
import streamlit as st
from utils.json_storage import load_variables, load_entries

if "variables" not in st.session_state:
    st.session_state.variables = load_variables()

if "entries" not in st.session_state:
    st.session_state.entries = load_entries()

st.set_page_config(page_title="Tracking-App", layout="centered")

st.title("📱 Startseite")

st.write("Navigiere über die Seitenleiste zu den Funktionen:")
st.markdown("- ➕ Neue Variable hinzufügen")