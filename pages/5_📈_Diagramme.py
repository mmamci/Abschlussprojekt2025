import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils.variable import VariableHandle, DataEntry, Variable


class DiagrammPage:
    def __init__(self) -> None:
        st.set_page_config(page_title="Diagramme",
                           page_icon="📆", layout="wide")
        st.title("📈 Diagramme aller Variablen")

        ss = st.session_state
        if "variableHandle" not in ss:
            ss.variableHandle = VariableHandle()
        self.variables = ss.variableHandle.current_variables

        self.entries = self._collect_entries()

        self.build_page()

    def _collect_entries(self):
        rows = []
        for var in self.variables:
            for e in var.data:
                rows.append({
                    "variable": var.name,
                    "value": e.value,
                    "note": e.note,
                    "date": e.date,
                })
        return rows

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
            goal = var.goal or ""

            st.subheader(name)
            if goal:
                st.markdown(f"**Ziel:** {goal}")

            var_df = df[df["variable"] == name].sort_values("date").copy()

            if var_df.empty:
                st.write("Noch keine Werte eingetragen.")
                st.markdown("---")
                continue

            if v_type in {"Quantitativ", "Skala 1-10"}:
                chart = (
                    alt.Chart(var_df)
                    .mark_line(point=True)
                    .encode(
                        x=alt.X("date:T", title="Datum"),
                        y=alt.Y(
                            "value:Q", title=f"Wert ({unit})" if unit else "Wert"),
                        tooltip=["date:T", "value:Q", "note:N"],
                    )
                    .properties(height=250, width=700)
                )
                st.altair_chart(chart, use_container_width=True)

            elif v_type == "Checkbox":
                var_df["value_num"] = var_df["value"].astype(int)
                chart = (
                    alt.Chart(var_df)
                    .mark_bar()
                    .encode(
                        x=alt.X("date:T", title="Datum"),
                        y=alt.Y("value_num:Q", title="Erledigt (1=Ja)"),
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

            if var_df["note"].astype(str).str.strip().any():
                with st.expander("Notizen anzeigen"):
                    st.table(
                        var_df[["date", "value", "note"]]
                        .rename(columns={"date": "Datum", "value": "Wert", "note": "Notiz"})
                    )

            st.markdown("---")


DiagrammPage()
