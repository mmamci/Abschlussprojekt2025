import streamlit as st, json, random
from pathlib import Path
from utils.json_storage import load_variables, save_variables
from utils.css_snippets import write_as_pills

COLOR_POOL = [
    "#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd",
    "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf",
]

class AddVariablePage:
    def __init__(self):
        ss = st.session_state
        if "variables" not in ss:
            ss.variables = load_variables()

        ss.setdefault("notification_times", [])
        ss.setdefault("notification_type", "")
        ss.setdefault("notif_edit", False)

        self.ss = ss
        self.build()

    
    def build(self):
        st.title("📊 Variable anlegen")

        c1,c2 = st.columns([1,2])
        with c1:
            st.text_input("Kurztitel", key="var_shortname")
        with c2:
            st.text_input("Ziel", key="var_goal")

        self.var_type_section()
        st.divider()
        self.notif_section()
        st.write("")

        if st.button("✅ Variable speichern"):
            self.save_variable()

        self.existing_vars()

    
    def var_type_section(self):
        v_types = ["Quantitativ","Checkbox","Zuletzt getan","Skala 1-10"]
        vt = st.selectbox("Art", v_types, key="type_selection")
        if vt=="Quantitativ":
            st.info("Zahlenbasierte Variable – z. B. Schritte.")
            c1,c2 = st.columns(2)
            with c1:
                st.selectbox("Einheit",["","kg","km","h","min","Stück"],key="unit_selection")
            with c2:
                st.selectbox("Was ist besser?",["Je mehr desto besser","Je weniger desto besser"],
                             key="quant_pref")
        elif vt=="Checkbox":
            st.info("Ja/Nein-Variable.")
        elif vt=="Zuletzt getan":
            st.info("Speichert, wann du etwas zuletzt getan hast.")
        else:
            st.info("Bewertung 1-10.")

    
    def notif_section(self):
        st.subheader("Benachrichtigungen")
        if not self.ss.notif_edit and not self.ss.notification_times:
            st.button("+ Benachrichtigung hinzufügen",
                      on_click=lambda:self.ss.update(notif_edit=True))
            return

        if self.ss.notification_times and not self.ss.notif_edit:
            st.write(f"🔔 {self.ss.notification_type}")
            write_as_pills(self.ss.notification_times)
            c1,c2=st.columns(2)
            if c1.button("🗑️ Löschen"):
                self.ss.notification_times=[]
                self.ss.notification_type=""
            if c2.button("✏️ Bearbeiten"):
                self.ss.notif_edit=True
            return

        
        nt = st.selectbox("Typ",["Daily","Weekly"],key="notif_type_temp")
        if nt=="Weekly":
            days = st.multiselect("Wochentage",
                   ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"])
        else:
            n = st.selectbox("Wie oft pro Tag?",[1,2,3],key="n_times")
            days=[st.time_input(f"{i+1}. Zeit",key=f"time_{i}").strftime("%H:%M")
                  for i in range(n)]

        c1,c2=st.columns(2)
        if c1.button("Speichern"):
            self.ss.update(notification_type=nt,notification_times=days,notif_edit=False)
        if c2.button("Abbrechen"):
            self.ss.notif_edit=False

   
    def save_variable(self):
        name=self.ss.get("var_shortname","").strip()
        if not name:
            st.warning("Namen eingeben."); return
        if any(v["name"]==name for v in self.ss.variables):
            st.warning("Variable existiert."); return

        used={v["color"] for v in self.ss.variables}
        free=[c for c in COLOR_POOL if c not in used] or ["#999999"]
        color=random.choice(free)

        self.ss.variables.append({
            "name":name,
            "goal":self.ss.get("var_goal",""),
            "type":self.ss.get("type_selection",""),
            "unit":self.ss.get("unit_selection",""),
            "color":color,
            "notification_type":self.ss.notification_type,
            "notification_times":self.ss.notification_times,
        })
        save_variables(self.ss.variables)
        st.success("Gespeichert.")

        
        for k in ["var_shortname","var_goal","unit_selection","quant_pref"]:
            self.ss.pop(k, None)
        self.ss.notification_times=[]
        self.ss.notification_type=""

   
    def existing_vars(self):
        if not self.ss.variables: return
        st.divider(); st.subheader("Bereits erstellt")
        for idx,v in enumerate(self.ss.variables):
            col1,col2=st.columns([5,1])
            with col1:
                st.markdown(
                    f"<span style='background:{v['color']};display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:6px;'></span>"
                    f"**{v['name']}** – {v['type']} {v.get('unit','')}",
                    unsafe_allow_html=True
                )
            if col2.button("🗑️",key=f"del_var_{idx}"):
                self.ss.variables.pop(idx)
                save_variables(self.ss.variables)


AddVariablePage()