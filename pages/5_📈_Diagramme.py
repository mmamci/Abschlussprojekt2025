import streamlit as st
import pandas as pd
import altair as alt
from utils.variable import VariableHandle, DataEntry, Variable


class DiagrammPage:
    def __init__(self) -> None:
        st.set_page_config(page_title="Diagramme", page_icon="📆", layout="wide")
        st.title("📆 Diagramme aller Variablen")

        # ----------------------------------------------------
        # VariableHandle nur einmal im Session‑State halten
        # ----------------------------------------------------
        ss = st.session_state
        if "variableHandle" not in ss:
            ss.variableHandle = VariableHandle()        # liest sofort die JSON
        self.variables: list[Variable] = ss.variableHandle.current_variables

        # flache Liste aller Einträge
        self.entries = self._collect_entries()

        self.build_page()

    # ---------------------------------------------------------
    # Hilfsfunktion: DataEntry‑Objekte in Dict‑Zeilen umwandeln
    # ---------------------------------------------------------
    def _collect_entries(self) -> list[dict]:
        rows = []
        for var in self.variables:
            for e in var.data:               # <‑‑ e ist DataEntry
                rows.append(
                    {
                        "variable": var.name,
                        "value":    e.value,
                        "note":     e.note,
                        "date":     e.date,
                    }
                )
        return rows

    # ---------------------------------------------------------
    def build_page(self):
        if not self.entries:
            st.info("Es wurden noch keine Werte eingetragen.")
            st.stop()

        # ---------------- DataFrame aufbauen -----------------
        df = pd.DataFrame(self.entries)
        df["date"] = pd.to_datetime(df["date"])

        # ---------------- Diagramme pro Variable -------------
        for var in self.variables:
            name   = var.name
            v_type = var.variable_type          # "Quantitativ", "Checkbox", …
            unit   = var.unit or ""
            goal   = var.goal or ""
            color  = "#1f77b4"                  # Defaultfarbe (kannst du auch hinzufügen)

            st.subheader(name)
            if goal:
                st.markdown(f"**Ziel:** {goal}")

            var_df = df[df["variable"] == name].sort_values("date").copy()

            if var_df.empty:
                st.write("Noch keine Werte eingetragen.")
                st.markdown("---")
                continue

            # 1️⃣  Quantitativ / Skala
            if v_type in {"Quantitativ", "Skala 1-10"}:
                chart = (
                    alt.Chart(var_df)
                    .mark_line(point=True, color=color)
                    .encode(
                        x=alt.X("date:T",  title="Datum"),
                        y=alt.Y("value:Q", title=f"Wert ({unit})" if unit else "Wert"),
                        tooltip=["date:T", "value:Q", "note:N"],
                    )
                    .properties(height=250, width=700)
                )
                st.altair_chart(chart, use_container_width=True)

            # 2️⃣  Checkbox
            elif v_type == "Checkbox":
                var_df["value_num"] = var_df["value"].astype(int)
                chart = (
                    alt.Chart(var_df)
                    .mark_bar(color=color)
                    .encode(
                        x=alt.X("date:T",  title="Datum"),
                        y=alt.Y("value_num:Q", title="Erledigt (1 = Ja)"),
                        tooltip=["date:T", "value_num", "note:N"],
                    )
                    .properties(height=200, width=700)
                )
                st.altair_chart(chart, use_container_width=True)

            # 3️⃣  Zuletzt getan
            elif v_type == "Zuletzt getan":
                chart = (
                    alt.Chart(var_df)
                    .mark_circle(size=120, color=color)
                    .encode(
                        x=alt.X("date:T", title="Datum"),
                        y=alt.value(1),
                        tooltip=["date:T", "note:N"],
                    )
                    .properties(height=120, width=700)
                    .configure_axisY(domain=False, ticks=False, labels=False)
                )
                st.altair_chart(chart, use_container_width=True)

            # Notizen als Tabelle einblendbar
            if var_df["note"].astype(str).str.strip().any():
                with st.expander("Notizen anzeigen"):
                    st.table(
                        var_df[["date", "value", "note"]]
                        .rename(columns={"date": "Datum", "value": "Wert", "note": "Notiz"})
                    )

            st.markdown("---")


# Stand‑alone‑Start
if __name__ == "__main__":
    DiagrammPage()