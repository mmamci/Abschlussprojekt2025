import streamlit as st
import json
from pathlib import Path
from utils.css_snippets import write_as_pills
from utils.variable import Variable, VariableHandle


class AddVariablePage:
    def __init__(self):
        self.ss = st.session_state
        self.initialize_variables()

        self.ss.variableHandle.read_variables()
        self.variables = self.ss.variableHandle.current_variables

        self.main_page()

    def initialize_variables(self):
        if "name" not in self.ss:
            self.ss.name = ""
        if "goal" not in self.ss:
            self.ss.goal = ""
        if "var_type" not in self.ss:
            self.ss.var_type = "Quantitativ"
        if "unit" not in self.ss:
            self.ss.unit = ""
        if "decrease_preferred" not in self.ss:
            self.ss.decrease_preferred = False
        if "notification_type" not in self.ss:
            self.ss.notification_type = "Daily"
        if "notification_times" not in self.ss:
            self.ss.notification_times = []

    def main_page(self):
        st.title("📊 Neue Variable hinzufügen")

        self.name_and_unit_selection()

        self.variable_type_selection()
        st.divider()

        self.create_notification_display()

        st.divider()
        if st.button("✅ Variable erstellen"):
            self.save_variable()

        self.show_existing_variables()

    def name_and_unit_selection(self):
        col1, col2 = st.columns([1, 2])
        with col1:
            self.ss.name = st.text_input(
                "Kurztitel der Variable",
                key="var_shortname",
                help="Kurzer Name, z.B. 'Schritte', 'Kalorien', 'Wasser'"
            )
        with col2:
            self.ss.goal = st.text_input(
                "Ziel dieser Variable",
                key="var_goal",
                help="Was möchtest du erreichen? Z.B. 10.000 Schritte pro Tag"
            )

    def variable_type_selection(self):
        variable_types = ["Quantitativ", "Checkbox",
                          "Zuletzt getan", "Skala 1-10"]

        st.subheader("Art der Variable")
        self.ss.var_type = st.selectbox(
            "Wie soll die Variable gemessen werden?",
            variable_types,
            key="type_selection",
            help="Wähle die passende Art, z.B. Anzahl, Ja/Nein, Datum, Bewertung"
        )

        if self.ss.var_type == "Quantitativ":
            st.info(
                "Diese Variable wird durch Zahlen beschrieben, z.B. Schritte oder Kalorien.")

            col1, col2 = st.columns(2)
            with col1:
                self.ss.unit = st.selectbox(
                    "Einheit der Variable",
                    ["", "kg", "km", "h", "min", "Stück", "m"],
                    key="unit_selection",
                    help="Welche Maßeinheit passt zur Variable?"
                )

            with col2:
                if "Je mehr desto besser" == st.selectbox(
                    "Was ist besser?",
                    ["Je mehr desto besser", "Je weniger desto besser"],
                    key="quant_preference",
                    help="Beispiel: Mehr Schritte sind besser → 'Je mehr desto besser'"
                ):
                    self.ss.decrease_preferred = False
                else:
                    self.ss.decrease_preferred = True

        elif self.ss.var_type == "Checkbox":
            st.info(
                "Diese Variable ist eine Ja/Nein-Antwort. Z.B. 'Sport gemacht heute?'")

        elif self.ss.var_type == "Zuletzt getan":
            st.info(
                "Diese Variable speichert, wann du zuletzt etwas getan hast. Z.B. 'Zuletzt geraucht'")

        elif self.ss.var_type == "Skala 1-10":
            st.info(
                "Diese Variable beschreibt deine Einschätzung auf einer Skala, z.B. 'Motivation heute'")

    def create_notification_display(self):
        st.subheader("Benachrichtigungen")

        if len(self.ss.notification_times) == 0:
            st.button("+ Benachrichtigung hinzufügen",
                      on_click=self.create_notification_dialog)
        else:
            st.write(f"🔔 {self.ss.notification_type} Benachrichtigung(en):")
            if self.ss.notification_type == "Daily":
                times = [t.strftime("%H:%M")
                         for t in self.ss.notification_times]
                write_as_pills(times)
            elif self.ss.notification_type == "Weekly":
                write_as_pills(self.ss.notification_times)

            st.button("🗑️ Alle Benachrichtigungen löschen",
                      on_click=lambda: self.ss.notification_times.clear())

    @st.dialog("Benachrichtigung erstellen")
    def create_notification_dialog(self):
        st.write("Wähle aus, wann du an diese Variable erinnert werden möchtest.")

        notification_types = ["Daily", "Weekly"]
        self.ss.notification_type = st.selectbox(
            "Benachrichtigungstyp", notification_types)

        if self.ss.notification_type == "Weekly":
            weekdays = ["Montag", "Dienstag", "Mittwoch",
                        "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            selected_days = st.multiselect(
                "An welchen Tagen möchtest du erinnert werden?", weekdays, key="weekly_input")

            if st.button("Fertig"):
                self.ss.notification_times = selected_days
                st.rerun()

        elif self.ss.notification_type == "Daily":
            times_per_day = st.selectbox(
                "Wie oft pro Tag möchtest du erinnert werden?", [1, 2, 3])
            for i in range(1, times_per_day + 1):
                st.time_input(f"{i}. Erinnerungszeitpunkt",
                              key=f"time_input_{i}")

            if st.button("Fertig"):
                self.ss.notification_times = [
                    self.ss[f"time_input_{i}"] for i in range(1, times_per_day + 1)]
                st.rerun()

    def save_variable(self):
        if not self.ss.name:
            st.warning("Bitte gib einen Namen für die Variable ein.")
            return

        if any(v.name == self.ss.name for v in self.variables):
            st.warning("Diese Variable existiert bereits.")
            return

        new_variable = Variable(
            self.ss.name,
            self.ss.goal,
            self.ss.notification_times,
            self.ss.var_type,
            self.ss.unit,
            self.ss.decrease_preferred
        )

        self.variables.append(new_variable)
        self.ss.variableHandle.write_variables()
        st.success(f"Variable '{self.ss.name}' wurde erstellt!")

    def show_existing_variables(self):
        st.divider()
        st.subheader("📋 Bereits erstellte Variablen")

        for i, var in enumerate(self.variables):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(
                    f"**{var.name}** — Typ: {var.variable_type} — Einheit: {var.unit}")
            with col2:
                if st.button("🗑️ Löschen", key=f"delete_{i}"):
                    self.variables.pop(i)
                    self.ss.variableHandle.write_variables()
                    st.rerun()


AddVariablePage()
