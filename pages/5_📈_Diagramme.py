import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
            self.name = var.name
            v_type = var.variable_type
            self.unit = var.unit or ""
            goal = var.goal or ""

            st.subheader(self.name)
            if goal:
                st.markdown(f"**Ziel:** {goal}")

            self.var_df = df[df["variable"] ==
                             self.name].sort_values("date").copy()

            if self.var_df.empty:
                st.write("Noch keine Werte eingetragen.")
                st.markdown("---")
                continue

            if v_type in {"Quantitativ", "Skala 1-10"}:
                self.plot_quantitative_or_one_to_ten()
            elif v_type == "Checkbox":
                self.plot_checkbox()

            # Notizen anzeigen
            if self.var_df["note"].astype(str).str.strip().any():
                with st.expander("Notizen anzeigen"):
                    st.table(
                        self.var_df[["date", "value", "note"]]
                        .rename(columns={"date": "Datum", "value": "Wert", "note": "Notiz"})
                    )

            st.markdown("---")

    def plot_checkbox(self):
        self.var_df["value_num"] = self.var_df["value"].astype(int)
        # Prepare a DataFrame with all days of the year
        if not self.var_df.empty:
            var_df = self.var_df.copy()
            var_df["date"] = pd.to_datetime(var_df["date"])
            var_df["week"] = var_df["date"].dt.isocalendar().week
            var_df["weekday"] = var_df["date"].dt.weekday  # 0=Monday
            # Create a matrix for 7 days x 48 weeks
            heatmap = pd.DataFrame(
                0, index=range(7), columns=range(1, 49))
            for _, row in var_df.iterrows():
                week = int(row["week"])
                day = int(row["weekday"])
                if 1 <= week <= 48 and 0 <= day <= 6:
                    heatmap.at[day, week] = row["value_num"]

            z = heatmap.values
            colorscale = [[0, "gray"], [1, "green"]]
            fig = go.Figure(data=go.Heatmap(
                z=z,
                x=list(heatmap.columns),
                y=["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
                colorscale=colorscale,
                showscale=False,
                hovertemplate="Woche: %{x}<br>Tag: %{y}<br>Erledigt: %{z}<extra></extra>",
                xgap=2,  # horizontal gap between squares
                ygap=2   # vertical gap between squares
            ))
            fig.update_layout(
                yaxis=dict(autorange="reversed"),
                xaxis_title="Kalenderwoche",
                yaxis_title="Wochentag",
                height=180,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

    def plot_quantitative_or_one_to_ten(self):
        self.fig = go.Figure()
        self.fig.add_trace(go.Scatter(
            x=self.var_df["date"],
            y=self.var_df["value"],
            mode="lines+markers",
            text=self.var_df["note"],
            hovertemplate="Datum: %{x}<br>Wert: %{y}<br>Notiz: %{text}<extra></extra>",
            name=self.name
        ))

        self.fig.update_layout(
            yaxis_title=f"Wert ({self.unit})" if self.unit else "Wert",
            xaxis_title="Datum",
            height=300,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(self.fig, use_container_width=True)


DiagrammPage()
