
import streamlit as st
from streamlit_calendar import calendar
from kalender import get_calendar_events

st.set_page_config(
    page_title="Kalender",
    layout="wide",
    page_icon="📅",
    initial_sidebar_state="expanded"
)

st.title("📆 Kalender Ansicht")

events = get_calendar_events()

calendar_options = {}


calendar(events=events, options=calendar_options)

pages = st.navigation(
    [
        st.Page("pages/ansicht.py", title="Anischt", icon=":material/monitoring:"),
        st.Page("pages/highlights.py", title="Highlights"),
        st.Page("pages/variable_hinzufuegen.py", title="Variable Hinzufügen"),
    ]
)
pages.run()

