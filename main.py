
import streamlit as st
from utils.json_storage import load_variables, load_entries
from utils.variable import Variable, VariableHandle
from Startseite import build_main_page


st.session_state.variableHandle = VariableHandle()

build_main_page()