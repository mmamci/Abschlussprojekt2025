import streamlit as st
import pandas as pd
import altair as alt
from utils.variable import VariableHandle, Variable, DataEntry

class DiagrammPage:
    def __init__(self) -> None:
        st.set_page_config(page_title="Diagramme", page_icon="📆", layout="wide")
        st.title("📈 Diagramme aller Variablen")

        self.ss = st.session_state
        self.ss.variableHandle.read_variables()
        self.variables = self.ss.variableHandle.current_variables

        # Alle DataEntries aller Variablen in eine flache Liste von Dicts umwandeln
        self.entries = []
        for var in self.variables:
            for entry in var.data:
                # Defensive: Nur Einträge mit Datum und Wert aufnehmen
                if hasattr(entry, "date") and hasattr(entry, "value"):
                    self.entries.append({
                        "variable": var.name,
                        "type": var.variable_type,
                        "unit": var.unit,
                        "goal": var.goal,
                        "decrease_preferred": var.decrease_preferred,
                        "date": entry.date,
                        "value": entry.value,
                        "note": getattr(entry, "note", ""),
                        "isFromFitFile": getattr(entry, "isFromFitFile", False)
                    })

        self.build_page()

    def build_page(self):
        if not self.entries:
            st.info("Es wurden noch keine Werte eingetragen.")
            return

        df = pd.DataFrame(self.entries)
        if not df.empty and "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        for var in self.variables:
            name = var.name
            v_type = var.variable_type
            unit = var.unit or ""
            goal = var.goal

            st.subheader(f"{name}")
            if goal:
                st.markdown(f"**Ziel:** {goal}")

            # Filter Einträge zur Variable
            if df.empty or "variable" not in df.columns:
                st.write("Noch keine Werte eingetragen.")
                st.markdown("---")
                continue
            var_df = df[df["variable"] == name].sort_values("date")
            if var_df.empty:
                st.write("Noch keine Werte eingetragen.")
                st.markdown("---")
                continue

            if v_type in ["Quantitativ", "Skala 1-10"]:
                chart = (
                    alt.Chart(var_df)
                    .mark_line(point=True)
                    .encode(
                        x=alt.X("date:T", title="Datum"),
                        y=alt.Y("value:Q", title=f"Wert ({unit})" if unit else "Wert"),
                        tooltip=["date:T", "value:Q", "note:N"],
                    )
                    .properties(height=250, width=700)
                )
                st.altair_chart(chart, use_container_width=True)

            elif v_type == "Checkbox":
                var_df = var_df.copy()
                var_df["value_num"] = var_df["value"].astype(int)
                chart = (
                    alt.Chart(var_df)
                    .mark_bar()
                    .encode(
                        x=alt.X("date:T", title="Datum"),
                        y=alt.Y("value_num:Q", title="Erledigt (1 = Ja)"),
                        tooltip=["date:T", "value_num", "note:N"],
                    )
                    .properties(height=200, width=700)
                )
                st.altair_chart(chart, use_container_width=True)

            elif v_type == "Zuletzt getan":
                chart = (
                    alt.Chart(var_df)
                    .mark_circle(size=120)
                    .encode(
                        x=alt.X("date:T", title="Datum"),
                        y=alt.value(1),
                        tooltip=["date:T", "note:N"],
                    )
                    .properties(height=120, width=700)
                    .configure_axisY(domain=False, ticks=False, labels=False)
                )
                st.altair_chart(chart, use_container_width=True)

            # Notizen als Tabelle unter dem Diagramm (optional)
            required_cols = ["date", "value", "note"]
            if all(col in var_df.columns for col in required_cols):
                notes_df = var_df[required_cols]
                if not notes_df.empty and notes_df["note"].astype(str).str.strip().any():
                    with st.expander("Notizen anzeigen"):
                        st.table(notes_df.rename(columns={
                            "date": "Datum", "value": "Wert", "note": "Notiz"
                        }))

            st.markdown("---")

DiagrammPage()