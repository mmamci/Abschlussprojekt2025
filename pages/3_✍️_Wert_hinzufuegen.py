import streamlit as st
from datetime import datetime
from utils.fitfiles import read_fit_file 
from utils.variable import Variable, VariableHandle, DataEntry

class AddValuePage:
    def __init__(self):
        self.ss = st.session_state

        # VariableHandle initialisieren, falls nötig
        if "variableHandle" not in self.ss:
            self.ss.variableHandle = VariableHandle()
        self.ss.variableHandle.read_variables()

        self.variables = self.ss.variableHandle.current_variables
        self.new_entry = None

        if not self.variables:
            st.info("⚠️ Bitte erst eine Variable erstellen, bevor du Werte hinzufügen kannst.")
            return

        self.build_page()

    def build_page(self):
        st.title("➕ Neuen Wert hinzufügen")

        variable_names = [v.name for v in self.variables]

        col1, col2 = st.columns(2)
        with col1:
            self.selected_var_name = st.selectbox("Variable auswählen", variable_names, key="selected_var")
        with col2:
            self.selected_date = st.date_input("Datum", datetime.today(), key="self.selected_date")

        self.selected_var = next(v for v in self.variables if v.name == self.selected_var_name)

        st.divider()

        self.uploaded_file = st.file_uploader("FIT-Datei hochladen (optional)", type=["fit"])
        if self.uploaded_file:
            fit_data = read_fit_file(self.uploaded_file)
            st.success("FIT-Datei erfolgreich gelesen.")
            st.write("📄 Vorschau (erste 3 Zeilen):")
            st.write(fit_data[:3])

        st.divider()
        self.type_dependent_input()
                
        if st.button("📥 Wert speichern"):
            self.save_entry()

        self.show_entries()

    def type_dependent_input(self):
        self.user_value = None
        var_type = self.selected_var.variable_type
        unit = self.selected_var.unit

        if var_type == "Quantitativ":
            label = f"Wert eingeben ({unit})" if unit else "Wert eingeben"
            self.user_value = st.number_input(label, key="quant_input")

        elif var_type == "Checkbox":
            self.user_value = st.checkbox("Heute erledigt?", key="checkbox_input")

        elif var_type == "Zuletzt getan":
            st.info("Diese Variable verwendet automatisch das ausgewählte Datum als Wert.")
            self.user_value = self.selected_date.strftime("%Y-%m-%d")

        elif var_type == "Skala 1-10":
            self.user_value = st.slider("Wert auf der Skala", 1, 10, key="scale_input")

        self.note = st.text_area("📝 Notiz (optional)", key="user_note")

    def save_entry(self):
        self.new_entry = DataEntry(
            self.selected_date,
            self.user_value,
            self.note,
            bool(self.uploaded_file)
        )

        # ✅ Neuen Eintrag anhängen
        self.selected_var.data.append(self.new_entry)

        # ✅ In Datei speichern
        self.ss.variableHandle.write_variables()

        st.success("Eintrag gespeichert!")

    def show_entries(self):
        st.divider()
        st.subheader("📜 Letzte gespeicherte Einträge")
        related_entries = self.selected_var.data
        if related_entries:
            last_five = related_entries[-5:][::-1]
            for idx, entry in enumerate(last_five):
                col_entry, col_del = st.columns([5, 1])
                with col_entry:
                    st.markdown(f"📅 **{entry.date}** – Wert: `{entry.value}`")
                    if entry.note:
                        st.markdown(f"📝 *{entry.note}*")
                if col_del.button("🗑️", key=f"del_{entry.date}_{idx}"):
                    self.selected_var.data.remove(entry)
                    self.ss.variableHandle.write_variables()
                    st.rerun()
        else:
            st.info("Noch keine Einträge gespeichert.")

# Aufruf der Seite
page = AddValuePage()