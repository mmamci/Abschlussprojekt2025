import streamlit as st
from streamlit_calendar import calendar
from kalender import get_calendar_events


st.title ("📆 Kalender Ansicht" )

events = get_calendar_events()
calender_options = {}
calendar(events=events, options=calender_options)