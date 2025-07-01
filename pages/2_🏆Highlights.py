import streamlit as st
from datetime import datetime
from ..utils.variable import VariableHandle


class HighlightsPage:
    def __init__(self):
        st.set_page_config(
            page_title="🏆 Highlights",
            page_icon="🏆",
            layout="wide"
        )
        st.title("🏆 Highlights entdecken")
        st.write(
            "Hier findest du für jede Variable den besten Wert oder besonderen Erfolg auf einen Blick.")
        st.markdown("---")

        ss = st.session_state
        if "variableHandle" not in ss:
            ss.variableHandle = VariableHandle()
        ss.variableHandle.read_variables()

        self.variables = ss.variableHandle.current_variables

        if not self.variables:
            st.info("ℹ️ Noch keine Variablen vorhanden.")
            return

        self.display_highlights()

    def display_highlights(self):
        cols = st.columns(3)

        for i, var in enumerate(self.variables):
            with cols[i % 3]:
                with st.container():
                    st.markdown(
                        f"## {self.get_emoji(var.variable_type)} {var.name}")

                    var_type = var.variable_type
                    entries = sorted(var.data, key=lambda e: e.date)

                    if not entries:
                        st.info("Keine Einträge vorhanden.")
                        continue

                    if var_type == "Quantitativ":
                        best = max(entries, key=lambda e: e.value if isinstance(
                            e.value, (int, float)) else float("-inf"))
                        self.show_summary(best, "Dein bester Wert")

                    elif var_type == "Skala 1-10":
                        best = max(entries, key=lambda e: int(
                            e.value) if str(e.value).isdigit() else -1)
                        self.show_summary(best, "Deine beste Bewertung")

                    elif var_type == "Checkbox":
                        streak = self.calculate_longest_streak(entries)
                        if streak:
                            st.markdown("##### Deine längste Serie:")
                            st.success(f"**{streak['length']} Tage in Folge**")
                            st.markdown(
                                f"*Von {streak['start'].strftime('%d.%m.%Y')} bis {streak['end'].strftime('%d.%m.%Y')}*")
                        else:
                            st.info("Keine Checkbox-Daten vorhanden.")

                    elif var_type == "Zuletzt getan":
                        best = max(entries, key=lambda e: e.date)
                        # Calculate days since last event
                        if isinstance(best.date, datetime):
                            last_date = best.date.date()
                        else:
                            last_date = datetime.strptime(
                                str(best.date).split()[0], "%Y-%m-%d").date()
                        days_ago = (datetime.now().date() - last_date).days
                        self.show_summary(
                            best, f"Zuletzt getan: {days_ago} Tag(e) her")

                    st.markdown("---")

    def get_emoji(self, var_type):
        mapping = {
            "Quantitativ": "💪",
            "Checkbox": "✅",
            "Zuletzt getan": "📅",
            "Skala 1-10": "🌟"
        }
        return mapping.get(var_type, "📊")

    def calculate_longest_streak(self, entries):
        true_dates = sorted([e.date for e in entries if e.value is True])
        if not true_dates:
            return None

        longest = {"length": 1, "start": true_dates[0], "end": true_dates[0]}
        current = {"length": 1, "start": true_dates[0], "end": true_dates[0]}

        for i in range(1, len(true_dates)):
            if (true_dates[i] - true_dates[i-1]).days == 1:
                current["length"] += 1
                current["end"] = true_dates[i]
            else:
                if current["length"] > longest["length"]:
                    longest = current.copy()
                current = {"length": 1,
                           "start": true_dates[i], "end": true_dates[i]}

        if current["length"] > longest["length"]:
            longest = current
        return longest

    def show_summary(self, entry, title):
        if isinstance(entry.date, datetime):
            date_str = entry.date.strftime("%d.%m.%Y")
        else:
            date_str = datetime.strptime(str(entry.date).split()[
                                         0], "%Y-%m-%d").strftime("%d.%m.%Y")
        value_str = f"{entry.value}"

    # Titel klein
        st.markdown(f"##### {title}:")

    # Wert groß und fett, linksbündig
        st.markdown(f"## **{value_str}**")

    # Blaue Info-Box für den Kontext (leichte Farbe)
        st.info(f"Datum: {date_str}")

    # Notiz kursiv, falls vorhanden
        if entry.note:
            st.markdown(f"_📝 {entry.note}_")


HighlightsPage()
