
import streamlit as st
from utils.json_storage import load_variables, load_entries
from utils.variable import Variable, VariableHandle

st.session_state.variableHandle = VariableHandle()

st.set_page_config(page_title="Tracking-App", layout="centered")

st.title("📱 Startseite")

st.write("Navigiere über die Seitenleiste zu den Funktionen:")
st.markdown("- ➕ Neue Variable hinzufügen")