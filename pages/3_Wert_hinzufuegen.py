import streamlit as st
from utils.fitfiles import read_fit_file
from datetime import datetime

class AddValuePage:
    def __init__(self):
        self.ss = st.session_state
        if "variables" not in self.ss or not self.ss.variables:
            st.info("⚠️ Bitte erst eine Variable erstellen, bevor du Werte hinzufügen kannst.")
            return

        self.main_page()

    def main_page(self):
        st.title("➕ Neuen Wert hinzufügen")

        col1, col2 = st.columns(2)

        variable_names = [
            var["name"] for var in self.ss.variables
            if isinstance(var, dict) and "name" in var
        ]

        with col1:
            selected_var_name = st.selectbox("Variable auswählen", variable_names, key="selected_var")
        with col2:
            selected_date = st.date_input("Datum auswählen", datetime.today(), key="selected_date")

        selected_var = next((v for v in self.ss.variables if isinstance(v, dict) and v.get("name") == selected_var_name), None)
   
        st.divider()

        # FIT-Datei optional
        uploaded_file = st.file_uploader("FIT-Datei hochladen (optional)", type=["fit"])
        if uploaded_file is not None:
            fit_data = read_fit_file(uploaded_file)
            st.success("FIT-Datei erfolgreich gelesen.")
            st.write("📄 Vorschau der ersten 3 Einträge:")
            st.write(fit_data[:3])

        st.divider()

        user_value = None
        if selected_var:
            var_type = selected_var.get("type")
            unit = selected_var.get("unit", "")

            if var_type == "Quantitativ":
                label = f"Wert eingeben ({unit})" if unit else "Wert eingeben"
                user_value = st.number_input(label, key="quant_input")

            elif var_type == "Checkbox":
                user_value = st.checkbox("Heute erledigt?", key="checkbox_input")

            elif var_type == "Zuletzt getan":
                st.info("Diese Variable verwendet automatisch das ausgewählte Datum als Wert.")
                user_value = selected_date

            elif var_type == "Skala 1-10":
                user_value = st.slider("Wert auf der Skala", 1, 10, key="scale_input")

        st.text_area("📝 Eigene Notiz (optional)", key="user_note")

        if st.button("📥 Wert speichern"):
            if "entries" not in self.ss:
                self.ss.entries = []

            self.ss.entries.append({
                "variable": selected_var_name,
                "datum": selected_date.strftime("%Y-%m-%d"),
                "wert": user_value,
                "notiz": self.ss.get("user_note", ""),
                "fit_datei_vorhanden": bool(uploaded_file)
            })

            st.success("✅ Wert gespeichert!")
            st.write("🔍 Gespeicherter Eintrag:")
            st.json(self.ss.entries[-1])

# Aufruf der Seite
page = AddValuePage()