import streamlit as st
import pandas as pd
import altair as alt
from utils.json_storage import load_variables, load_entries

st.set_page_config(page_title="Diagramme", page_icon="📆", layout="wide")
st.title("📆 Diagramme aller Variablen")

# Lade Daten
variables = load_variables()            
entries   = load_entries()    
          
# Falls keine Werte vorhanden
if not entries:
    st.info("Es wurden noch keine Werte eingetragen.")
    st.stop()

# DataFrame mit Datum als Datetime
df = pd.DataFrame(entries)
df["datum"] = pd.to_datetime(df["datum"])

# Für jede Variable ein Diagramm
for var in variables:
    name   = var["name"]
    v_type = var["type"]
    unit   = var.get("unit", "")
    color  = var.get("color", "#1f77b4")
    goal   = var.get("goal", None)  # Ziel holen, falls vorhanden

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
        chart = (
            alt.Chart(var_df)
            .mark_line(point=True, color=color)
            .encode(
                x=alt.X("datum:T", title="Datum"),
                y=alt.Y("wert:Q", title=f"Wert ({unit})" if unit else "Wert"),
                tooltip=["datum:T", "wert:Q", "notiz:N"],
            )
            .properties(height=250, width=700)
        )
        st.altair_chart(chart, use_container_width=True)

    elif v_type == "Checkbox":
        # Checkbox True/False als 1/0 für Balken
        var_df["wert_num"] = var_df["wert"].astype(int)
        chart = (
            alt.Chart(var_df)
            .mark_bar(color=color)
            .encode(
                x=alt.X("datum:T", title="Datum"),
                y=alt.Y("wert_num:Q", title="Erledigt (1 = Ja)"),
                tooltip=["datum:T", "wert_num", "notiz:N"],
            )
            .properties(height=200, width=700)
        )
        st.altair_chart(chart, use_container_width=True)

    elif v_type == "Zuletzt getan":
        chart = (
            alt.Chart(var_df)
            .mark_circle(size=120, color=color)
            .encode(
                x=alt.X("datum:T", title="Datum"),
                y=alt.value(1),  # Punkte auf einer Linie
                tooltip=["datum:T", "notiz:N"],
            )
            .properties(height=120, width=700)
            .configure_axisY(domain=False, ticks=False, labels=False)
        )
        st.altair_chart(chart, use_container_width=True)

    # Notizen als Tabelle unter dem Diagramm (optional)
    if var_df["notiz"].str.strip().any():
        with st.expander("Notizen anzeigen"):
            st.table(var_df[["datum", "wert", "notiz"]].rename(columns={
                "datum": "Datum", "wert": "Wert", "notiz": "Notiz"
            }))

    st.markdown("---")