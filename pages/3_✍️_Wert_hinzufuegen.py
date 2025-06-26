import streamlit as st
from datetime import datetime
from utils.json_storage import load_entries, save_entries
from utils.fitfiles import read_fit_file  # optional

class AddValuePage:
    def __init__(self):
        ss=st.session_state
        if not ss.get("variables"):
            st.info("⚠️ Erst Variable anlegen."); return
        if "entries" not in ss:
            ss.entries=load_entries()
        self.ss=ss; self.build()

    def build(self):
        st.title("➕ Wert erfassen")

        names=[v["name"] for v in self.ss.variables]
        c1,c2=st.columns(2)
        with c1: sel_var=st.selectbox("Variable",names)
        with c2: sel_date=st.date_input("Datum",datetime.today())
        var_info=next(v for v in self.ss.variables if v["name"]==sel_var)
        st.divider()

        file=st.file_uploader("FIT-Datei (optional)",type=["fit"])
        if file:
            st.success("FIT gelesen"); st.write(read_fit_file(file)[:3])
        st.divider()

        
        val=None
        if var_info["type"]=="Quantitativ":
            label="Wert" + (f" ({var_info['unit']})" if var_info["unit"] else "")
            val=st.number_input(label)
        elif var_info["type"]=="Checkbox":
            val=st.checkbox("Heute erledigt?")
        elif var_info["type"]=="Zuletzt getan":
            st.info("Datum wird übernommen.")
            val=sel_date.strftime("%Y-%m-%d")
        else:
            val=st.slider("Wert (1-10)",1,10)

        note=st.text_area("📝 Notiz (optional)")

        if st.button("📥 Wert speichern"):
            entry={
                "variable":sel_var,
                "datum":sel_date.strftime("%Y-%m-%d"),
                "wert":val,
                "notiz":note,
                "fit_datei_vorhanden":bool(file),
            }
            self.ss.entries.append(entry); save_entries(self.ss.entries)
            st.success("Gespeichert.")

        
        st.divider(); st.subheader("Letzte Einträge")
        rel=[e for e in self.ss.entries if e["variable"]==sel_var][-5:][::-1]
        if not rel: st.info("Noch keine Einträge."); return
        for i,e in enumerate(rel):
            c_txt,c_btn=st.columns([5,1])
            with c_txt:
                st.markdown(f"📅 **{e['datum']}** – **{e['variable']}**: `{e['wert']}`")
                if e.get("notiz"): st.markdown(f"*{e['notiz']}*")
            if c_btn.button("🗑️",key=f"del_{i}"):
                self.ss.entries.remove(e); save_entries(self.ss.entries)

AddValuePage()