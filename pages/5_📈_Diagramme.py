import streamlit as st
import pandas as pd
import plotly.express as px
from utils.variable import VariableHandle, Variable, DataEntry


class DiagrammPage:
    def __init__(self) -> None:
        st.set_page_config(page_title="Diagramme", page_icon="📆", layout="wide")
        st.title("📆 Diagramme aller Variablen")

        self.ss = st.session_state

        if "variableHandle" not in self.ss:
            self.ss.variableHandle = VariableHandle()

        self.ss.variableHandle.read_variables()

        self.variables = self.ss.variableHandle.current_variables

        # Alle DataEntry-Objekte in Dicts umwandeln
        self.entries = [
            {"variable": var.name, "datum": entry.date, "wert": entry.value, "notiz": entry.note}
            for var in self.variables for entry in var.data
        ]

        self.build_page()
        
    def build_page(self):
        # Falls keine Werte vorhanden
        if not self.entries:
            st.info("Es wurden noch keine Werte eingetragen.")
            st.stop()

        # DataFrame mit Datum als Datetime
        df = pd.DataFrame(self.entries)
        df["datum"] = pd.to_datetime(df["datum"])

        # Für jede Variable ein Diagramm
        for var in self.variables:
            name   = var.name
            v_type = var.variable_type
            unit   = getattr(var, "unit", "") or ""
            goal   = getattr(var, "goal", None)

            st.subheader(f"{name}")

            # Ziel anzeigen, falls vorhanden
            if goal:
                st.markdown(f"**Ziel:** {goal}")

            # Filter Einträge zur Variable
            var_df = df[df["variable"] == name].sort_values("datum")

            if var_df.empty:
                st.write("Noch keine Werte eingetragen.")
                st.markdown("---")
                continue

            if v_type in ["Quantitativ", "Skala 1-10"]:
                fig = px.line(var_df, x="datum", y="wert", markers=True, title=name)
                fig.update_layout(yaxis_title=f"Wert ({unit})" if unit else "Wert", xaxis_title="Datum", height=300)
                st.plotly_chart(fig, use_container_width=True)

            elif v_type == "Checkbox":
                var_df["wert_num"] = var_df["wert"].astype(int)
                fig = px.bar(var_df, x="datum", y="wert_num", title=name)
                fig.update_layout(yaxis_title="Erledigt (1 = Ja)", xaxis_title="Datum", height=200)
                st.plotly_chart(fig, use_container_width=True)

            elif v_type == "Zuletzt getan":
                fig = px.scatter(var_df, x="datum", y=[1]*len(var_df), size_max=10, title=name)
                fig.update_traces(marker=dict(size=16))
                fig.update_layout(yaxis=dict(showticklabels=False, showgrid=False, zeroline=False), height=120)
                st.plotly_chart(fig, use_container_width=True)

            # Notizen als Tabelle unter dem Diagramm (optional)
            if var_df["notiz"].astype(str).str.strip().any():
                with st.expander("Notizen anzeigen"):
                    st.table(var_df[["datum", "wert", "notiz"]].rename(columns={
                        "datum": "Datum", "wert": "Wert", "notiz": "Notiz"
                    }))

            st.markdown("---")

DiagrammPage()