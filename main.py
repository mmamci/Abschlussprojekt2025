import streamlit as st
from utils.authenticator import Authenticator
from utils.variable import VariableHandle

ss = st.session_state
if "variableHandle" not in ss:
    ss.variableHandle = VariableHandle()

authenticator = Authenticator()
