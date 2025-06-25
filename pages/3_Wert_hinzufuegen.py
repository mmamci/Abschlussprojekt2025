import streamlit as st
from datetime import datetime
from utils.json_storage import load_entries, save_entries
from utils.fitfiles import read_fit_file  # Optional

class AddValuePage:
    def __init__(self):
        self.ss = st.session_state

        # 1) Prüfen, ob Variablen vorhanden sind
        if "variables" not in self.ss or not self.ss.variables:
            st.info("⚠️ Bitte erst eine Variable erstellen, bevor du Werte hinzufügen kannst.")
            return

        # 2) Einträge einmalig laden
        if "entries" not in self.ss:
            self.ss.entries = load_entries()

        self.build_page()

    # ------------------------------------------------------------------
    def build_page(self):
        st.title("➕ Neuen Wert hinzufügen")

        # ---------- Kopfzeile: Variable + Datum ----------
        variable_names = [
            v.get("name") or v.get("shortname")
            for v in self.ss.variables
        ]

        col1, col2 = st.columns(2)
        with col1:
            selected_var_name = st.selectbox("Variable auswählen", variable_names, key="selected_var")
        with col2:
            selected_date = st.date_input("Datum", datetime.today(), key="selected_date")

        selected_var = next(
            v for v in self.ss.variables
            if (v.get("name") or v.get("shortname")) == selected_var_name
        )

        st.divider()

        # ---------- FIT‑Datei (optional) ----------
        uploaded_file = st.file_uploader("FIT-Datei hochladen (optional)", type=["fit"])
        if uploaded_file:
            fit_data = read_fit_file(uploaded_file)
            st.success("FIT-Datei erfolgreich gelesen.")
            st.write("📄 Vorschau (erste 3 Zeilen):")
            st.write(fit_data[:3])

        st.divider()

        # ---------- Werterfassung je nach Typ ----------
        user_value = None
        var_type   = selected_var.get("type")
        unit       = selected_var.get("unit", "")

        if var_type == "Quantitativ":
            label = f"Wert eingeben ({unit})" if unit else "Wert eingeben"
            user_value = st.number_input(label, key="quant_input")

        elif var_type == "Checkbox":
            user_value = st.checkbox("Heute erledigt?", key="checkbox_input")

        elif var_type == "Zuletzt getan":
            st.info("Diese Variable verwendet automatisch das ausgewählte Datum als Wert.")
            user_value = selected_date.strftime("%Y-%m-%d")

        elif var_type == "Skala 1-10":
            user_value = st.slider("Wert auf der Skala", 1, 10, key="scale_input")

        note = st.text_area("📝 Notiz (optional)", key="user_note")

        # ---------- Speichern ----------
        if st.button("📥 Wert speichern"):
            new_entry = {
                "variable": selected_var_name,
                "datum":    selected_date.strftime("%Y-%m-%d"),
                "wert":     user_value,
                "notiz":    note,
                "fit_datei_vorhanden": bool(uploaded_file),
            }
            self.ss.entries.append(new_entry)
            save_entries(self.ss.entries)

            st.success("✅ Wert gespeichert!")
            st.json(new_entry)

        # ---------- Letzte Einträge + Lösch‑Option ----------
        st.divider()
        st.subheader("📜 Letzte gespeicherte Einträge")

        # Filter & sortiere die letzten 5 zu dieser Variable
        related_entries = [e for e in self.ss.entries if e["variable"] == selected_var_name]
        if related_entries:
            last_five = related_entries[-5:][::-1]  # umgekehrte Reihenfolge (neuester oben)

            for idx, entry in enumerate(last_five):
                col_entry, col_del = st.columns([5, 1])
                with col_entry:
                    st.markdown(f"📅 **{entry['datum']}** – Wert: `{entry['wert']}`")
                    if entry.get("notiz"):
                        st.markdown(f"📝 *{entry['notiz']}*")
                # Ein eindeutiger Key pro Button: Kombination aus Datum & Loop‑Index
                if col_del.button("🗑️", key=f"del_{entry['datum']}_{idx}"):
                    # Entfernen aus Session & Datei
                    self.ss.entries.remove(entry)
                    save_entries(self.ss.entries)
                    st.experimental_rerun()
        else:
            st.info("Noch keine Einträge gespeichert.")

# ---------------- Aufruf der Seite ----------------
page = AddValuePage()