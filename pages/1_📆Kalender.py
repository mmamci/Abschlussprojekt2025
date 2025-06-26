import streamlit as st
from streamlit_calendar import calendar
from utils.calendar_events import build_calendar_events
from utils.css_snippets import write_as_pills




class CalendarPage():
    def __init__(self):
        self.events, self.variables = build_calendar_events()
        # Kalender-Ereignisse und Variablen laden
        
        st.title("📆 Kalender Ansicht")
        # Kalender anzeigen
        selected = calendar(events=self.events, options={"selectable": True})

        # Legende anzeigen
        st.write("### Legende")
        for v in self.variables:
            st.markdown(
                f"<div style='display:flex; align-items:center; margin-bottom:6px;'>"
                f"<div style='background-color:{v['color']}; width:20px; height:20px; margin-right:10px; border-radius:4px;'></div>"
                f"<span style='color:white; background-color:#333; padding:4px 8px; border-radius:4px;'>{v['name']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        # Wenn ein Datum gewählt wurde, zeige die Details
        if selected and selected.get("start"):
            st.markdown("### 📋 Details zum ausgewählten Datum")
            selected_date = selected["start"][:10]  # Format: YYYY-MM-DD

            # Suche Events zum gewählten Datum
            date_events = [e for e in self.events if e["start"].startswith(selected_date)]

            if not date_events:
                st.info("Keine Einträge für dieses Datum.")
            else:
                for e in date_events:
                    st.markdown(
                        f"**🟢 {e['title']}**  \n"
                        f"<span style='color:gray'>📅 {selected_date}</span><br>"
                        f"{e.get('description', 'Keine Notiz vorhanden')}",
                        unsafe_allow_html=True
                    )
                    st.markdown("---")