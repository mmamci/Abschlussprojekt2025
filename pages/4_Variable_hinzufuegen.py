import streamlit as st
from datetime import time

class AddVariablePage:
    def __init__(self):
        self.ss = st.session_state

        # Initialisierung
        if "notification_times" not in self.ss:
            self.ss.notification_times = []
        if "notification_type" not in self.ss:
            self.ss.notification_type = ""
        if "variables" not in self.ss:
            self.ss.variables = []

        self.main_page()

    def main_page(self):
        st.title("📊 Neue Variable hinzufügen")

        # Kurztitel und Ziel nebeneinander
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

        self.show_existing_variables()

    def variable_type_selection(self):
        variable_types = ["Quantitativ", "Checkbox", "Zuletzt getan", "Skala 1–10"]

        st.subheader("Art der Variable")
        var_type = st.selectbox(
            "Wie soll die Variable gemessen werden?",
            variable_types,
            key="type_selection",
            help="Wähle die passende Art, z. B. Anzahl, Ja/Nein, Datum, Bewertung"
        )

        if var_type == "Quantitativ":
            st.info("Diese Variable wird durch Zahlen beschrieben, z. B. Schritte oder Kalorien.")

            col1, col2 = st.columns(2)
            with col1:
                st.selectbox(
                    "Einheit der Variable",
                    ["", "kg", "km", "h", "min", "Stück"],
                    key="quant_einheit",
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
            st.info("Diese Variable ist eine Ja/Nein-Antwort. Z. B. 'Sport gemacht heute?'")

        elif var_type == "Zuletzt getan":
            st.info("Diese Variable speichert, wann du zuletzt etwas getan hast. Z. B. 'Zuletzt geraucht'")

        elif var_type == "Skala 1–10":
            st.info("Diese Variable beschreibt deine Einschätzung auf einer Skala, z. B. 'Motivation heute'")

    def create_notification_display(self):
        st.subheader("Benachrichtigungen")

        if len(self.ss.notification_times) == 0:
            st.button("+ Benachrichtigung hinzufügen", on_click=self.create_notification_dialog)
        else:
            st.write(f"🔔 {self.ss.notification_type} Benachrichtigung(en):")
            if self.ss.notification_type == "Daily":
                times = [t.strftime("%H:%M") for t in self.ss.notification_times]
                st.write(", ".join(times))
            elif self.ss.notification_type == "Weekly":
                st.write(", ".join(self.ss.notification_times))

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
                st.rerun()

        elif self.ss.notification_type == "Daily":
            times_per_day = st.selectbox("Wie oft pro Tag möchtest du erinnert werden?", [1, 2, 3])
            for i in range(1, times_per_day + 1):
                st.time_input(f"{i}. Erinnerungszeitpunkt", key=f"time_input_{i}")

            if st.button("Fertig"):
                self.ss.notification_times = [self.ss[f"time_input_{i}"] for i in range(1, times_per_day + 1)]
                st.rerun()

    def save_variable(self):
        name = self.ss.get("var_shortname", "").strip()
        if not name:
            st.warning("Bitte gib einen Namen für die Variable ein.")
            return

        if name in self.ss.variables:
            st.warning("Diese Variable existiert bereits.")
            return

        self.ss.variables.append(name)
        st.success(f"Variable '{name}' wurde erstellt!")

    def show_existing_variables(self):
        if not self.ss.variables:
            return

        st.divider()
        st.subheader("📋 Bereits erstellte Variablen")

        for i, var_name in enumerate(self.ss.variables):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{var_name}**")
            with col2:
                if st.button("🗑️ Löschen", key=f"delete_{i}"):
                    self.ss.variables.pop(i)
                    st.rerun()


# Seite aufrufen
page = AddVariablePage()