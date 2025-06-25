import streamlit as st
from streamlit_calendar import calendar
from utils.calendar_events import build_calendar_events

st.title("📆 Kalender Ansicht")

events, variables = build_calendar_events()
calendar(events=events, options={})


for v in variables:
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        st.markdown(
            f"<div style='width: 20px; height: 20px; background-color: {v['color']}; border-radius: 4px;'></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.write(v["name"])