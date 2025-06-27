import streamlit as st
<<<<<<< HEAD
from utils.json_storage import load_variables, load_entries
from utils.variable import Variable, VariableHandle

st.session_state.variableHandle = VariableHandle()

st.set_page_config(page_title="Tracking-App", layout="centered")

st.title("📱 Startseite")

st.write("Navigiere über die Seitenleiste zu den Funktionen:")
st.markdown("- ➕ Neue Variable hinzufügen")
=======
from utils.authenticator import Authenticator
from utils.variable import VariableHandle

ss = st.session_state
if "variableHandle" not in ss:
    ss.variableHandle = VariableHandle()

authenticator = Authenticator()
>>>>>>> b3bc77684f5a5ea7fc1bd02d92b0f7e474f80be2
