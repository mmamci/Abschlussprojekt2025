import streamlit as st
from streamlit_calendar import calendar
from utils.variable import VariableHandle
from utils.css_snippets import write_as_pills
import itertools



class CalendarPage:
    def __init__(self):
        ss = st.session_state

        ss.variableHandle.read_variables()
        self.variables = ss.variableHandle.current_variables

        # 🔁 Farben rotieren lassen, wenn keine vorhanden sind
        palette = itertools.cycle([
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
            "#9467bd", "#8c564b", "#e377c2", "#7f7f7f",
            "#bcbd22", "#17becf"
        ])
        color_map = {}

        self.events = []
        for var in self.variables:
            color = getattr(var, "color", None) or color_map.get(var.name) or next(palette)
            color_map[var.name] = color  # speichern

            for entry in var.data:
                self.events.append({
                    "title": f"{var.name}: {entry.value}",
                    "start": str(entry.date),
                    "color": color,
                    "description": entry.note or ""
                })

        st.title("📆 Kalender Ansicht")
        selected = calendar(events=self.events, options={"selectable": True})

        # 🎨 Legende
        st.write("### Legende")
        for name, color in color_map.items():
            st.markdown(
                f"<div style='display:flex; align-items:center; margin-bottom:6px;'>"
                f"<div style='background-color:{color}; width:20px; height:20px; margin-right:10px; border-radius:4px;'></div>"
                f"<span style='color:white; background-color:#333; padding:4px 8px; border-radius:4px;'>{name}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        # Details zum ausgewählten Datum
        if selected and selected.get("start"):
            st.markdown("### 📋 Details zum ausgewählten Datum")
            selected_date = selected["start"][:10]
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

# Aufruf der Seite
CalendarPage()