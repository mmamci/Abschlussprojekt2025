import streamlit as st
import json
from pathlib import Path
from utils.css_snippets import write_as_pills  # falls du das nutzt

DATA_PATH = Path("data")
VARIABLES_FILE = DATA_PATH / "variables.json"

class AddVariablePage:
    def __init__(self):
        self.ss = st.session_state

        # Ordner und Datei vorbereiten
        DATA_PATH.mkdir(exist_ok=True)
        if not VARIABLES_FILE.exists():
            VARIABLES_FILE.write_text("[]", encoding="utf-8")

        # Variablen laden, falls nicht im session_state
        if "variables" not in self.ss:
            self.ss.variables = self.load_variables()

        if "notification_times" not in self.ss:
            self.ss.notification_times = []
        if "notification_type" not in self.ss:
            self.ss.notification_type = ""

        self.main_page()

    def load_variables(self):
        try:
            with open(VARIABLES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_variables(self):
        with open(VARIABLES_FILE, "w", encoding="utf-8") as f:
            json.dump(self.ss.variables, f, ensure_ascii=False, indent=2)

    def save_values(self):
        var_type = self.ss.get("type_selection", "")

        if "unit_selection" in self.ss:
            var_unit = self.ss["unit_selection"]
        else:
            var_unit = "None"
        
        notif_times = self.ss.notification_times
        notif_type = self.ss.notification_type
        # Hier kannst du später weitere Daten verarbeiten, wenn nötig

    def main_page(self):
        st.title("📊 Neue Variable hinzufügen")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.text_input(
                "Kurztitel der Variable",
                key="var_shortname",
                help="Kurzer Name, z. B. 'Schritte', 'Kalorien', 'Wasser'"
            )
        with col2:
            st.text_input(
                "Ziel dieser Variable",
                key="var_goal",
                help="Was möchtest du erreichen? Z. B. 10.000 Schritte pro Tag"
            )

        self.variable_type_selection()
        st.divider()

        self.create_notification_display()

        st.write("")
        if st.button("✅ Variable erstellen"):
            self.save_variable()

        if st.button("Variable Erstellen"):
            self.save_values()
        self.show_existing_variables()

    def variable_type_selection(self):
        variable_types = ["Quantitativ", "Checkbox", "Zuletzt getan", "Skala 1-10"]

        st.subheader("Art der Variable")
        var_type = st.selectbox(
            "Wie soll die Variable gemessen werden?",
            variable_types,
            key="type_selection",
            help="Wähle die passende Art, z.B. Anzahl, Ja/Nein, Datum, Bewertung"
        )

        if var_type == "Quantitativ":
            st.info("Diese Variable wird durch Zahlen beschrieben, z.B. Schritte oder Kalorien.")

            col1, col2 = st.columns(2)
            with col1:
                st.selectbox(
                    "Einheit der Variable",
                    ["", "kg", "km", "h", "min", "Stück"],
                    key="unit_selection",
                    help="Welche Maßeinheit passt zur Variable?"
                )

            with col2:
                st.selectbox(
                    "Was ist besser?",
                    ["Je mehr desto besser", "Je weniger desto besser"],
                    key="quant_preference",
                    help="Beispiel: Mehr Schritte sind besser → 'Je mehr desto besser'"
                )

        elif var_type == "Checkbox":
            st.info("Diese Variable ist eine Ja/Nein-Antwort. Z.B. 'Sport gemacht heute?'")

        elif var_type == "Zuletzt getan":
            st.info("Diese Variable speichert, wann du zuletzt etwas getan hast. Z.B. 'Zuletzt geraucht'")

        elif var_type == "Skala 1-10":
            st.info("Diese Variable beschreibt deine Einschätzung auf einer Skala, z.B. 'Motivation heute'")

    def create_notification_display(self):
        st.subheader("Benachrichtigungen")

        if len(self.ss.notification_times) == 0:
            st.button("+ Benachrichtigung hinzufügen", on_click=self.create_notification_dialog)
        else:
            st.write(f"🔔 {self.ss.notification_type} Benachrichtigung(en):")
            if self.ss.notification_type == "Daily":
                times = [t.strftime("%H:%M") for t in self.ss.notification_times]
                write_as_pills(times)
            elif self.ss.notification_type == "Weekly":
                write_as_pills(self.ss.notification_times)

            st.button("🗑️ Alle Benachrichtigungen löschen", on_click=lambda: self.ss.notification_times.clear())

    @st.dialog("Benachrichtigung erstellen")
    def create_notification_dialog(self):
        st.write("Wähle aus, wann du an diese Variable erinnert werden möchtest.")

        notification_types = ["Daily", "Weekly"]
        self.ss.notification_type = st.selectbox("Benachrichtigungstyp", notification_types)

        if self.ss.notification_type == "Weekly":
            weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            selected_days = st.multiselect("An welchen Tagen möchtest du erinnert werden?", weekdays, key="weekly_input")

            if st.button("Fertig"):
                self.ss.notification_times = selected_days
                st.experimental_rerun()

        elif self.ss.notification_type == "Daily":
            times_per_day = st.selectbox("Wie oft pro Tag möchtest du erinnert werden?", [1, 2, 3])
            for i in range(1, times_per_day + 1):
                st.time_input(f"{i}. Erinnerungszeitpunkt", key=f"time_input_{i}")

            if st.button("Fertig"):
                self.ss.notification_times = [self.ss[f"time_input_{i}"] for i in range(1, times_per_day + 1)]
                st.experimental_rerun()

    def save_variable(self):
        name = self.ss.get("var_shortname", "").strip()
        if not name:
            st.warning("Bitte gib einen Namen für die Variable ein.")
            return

        # Check, ob Variable mit gleichem Namen bereits existiert
        if any(v["name"] == name for v in self.ss.variables):
            st.warning("Diese Variable existiert bereits.")
            return

        # Variable als dict speichern inkl. Typ und Einheit
        new_var = {
            "name": name,
            "goal": self.ss.get("var_goal", "").strip(),
            "type": self.ss.get("type_selection", ""),
            "unit": self.ss.get("unit_selection", ""),
            "notification_type": self.ss.notification_type,
            "notification_times": self.ss.notification_times,
        }
        self.ss.variables.append(new_var)

        self.save_variables()  # in Datei speichern
        st.success(f"Variable '{name}' wurde erstellt!")

    def show_existing_variables(self):
        if not self.ss.variables:
            return

        st.divider()
        st.subheader("📋 Bereits erstellte Variablen")

        for i, var in enumerate(self.ss.variables):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{var['name']}** — Typ: {var.get('type', '')} — Einheit: {var.get('unit', '')}")
            with col2:
                if st.button("🗑️ Löschen", key=f"delete_{i}"):
                    self.ss.variables.pop(i)
                    self.save_variables()
                    st.experimental_rerun()


page = AddVariablePage()

