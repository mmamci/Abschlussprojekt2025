import streamlit as st
from utility.fitfiles import read_fit_file
from utility.css_snippets import display_as_pills

class AddVariablePage:
    def __init__(self):
        self.ss = st.session_state
        if "notification_times" not in self.ss:
            self.ss.notification_times = []
        if "notification_type" not in self.ss:
            self.ss.notification_type = ""

        self.notifications = []
        self.variable_name = ""
        self.variable_type = ""
        self.unit = ""
        
        self.main_page()

    def main_page(self):
        st.text_input("Kurztitel der Variable", help="Bsp: Gelaufene Meter")

        self.variable_type_selection()

        self.create_notification_display()

        st.text_input("Ziel der festgelegten variable")

        st.button("Variable Erstellen")

    def variable_type_selection(self):
        variable_types = ["Quantitativ", "Checkbox", "Zuletzt getan", "Skala 1-10"]
        st.selectbox("Art der Variable", variable_types, key="type_selection", help="Wie misst man deine Variable?")

        if self.ss["type_selection"] == "Quantitativ":
            st.write("Deine Variable wird durch diskrete Zahlen beschrieben. Bsp: Gelaufene Meter, gegessene Kalorien ...")
            self.unit = st.selectbox("Welche Einheit hat deine Variable?", ["", "kg", "km", "h", "min", "Stück"], key="quant_einheit", accept_new_options=True)

            st.selectbox("Sind größere oder kleinere Werte besser?", ["Je mehr desto besser", "Je weniger desto besser"], help="Um so mehr Gelaufene Meter um so besser -> Je mehr desto besser. Um so weniger Kalorien konsumiert um so besser -> Je weniger desto besser")
            
        elif self.ss["type_selection"] == "Checkbox":
            st.write("Deine Variable kann mit Wahr oder Falsch beschrieben werden. Bsp: Hab ich heute Sport gemacht?")

        elif self.ss["type_selection"] == "Zuletzt getan":
            st.write("Deine Variable hält fest, wann du zuletzt etwas negatives gemacht hast. Bsp: Zuletzt geraucht")

    def create_notification_display(self):
        if len(self.ss.notification_times) == 0:
            st.pills("Benachrichtigungen", [r"\+"], on_change=self.create_notification_dialog)
    
        elif self.ss.notification_type == "Daily":
            st.write("Benachrichtigungen")
            notification_times_str = [i.strftime("%H:%M") for i in self.ss.notification_times]
            col1, col2 = st.columns([8, 1])
            with col1:
                display_as_pills(notification_times_str)
            with col2:
                st.pills(" ", [r"x"], on_change=lambda : self.ss.notification_times.clear(), label_visibility="collapsed")

        elif self.ss.notification_type == "Weekly":
            st.write("Benachrichtigungen")
            
            col1, col2 = st.columns([8, 1])
            with col1:
                display_as_pills(self.ss.notification_times)
            with col2:
                st.pills(" ", [r"x"], on_change=lambda : self.ss.notification_times.clear(), label_visibility="collapsed")

    @st.dialog("Create Notification")
    def create_notification_dialog(self):
        st.write("Benachrichtigung erstellen")
        notification_types = ["Daily", "Weekly"]
        self.notification_times = []
    
        self.ss.notification_type = st.selectbox("Benachrichtigungstyp", notification_types)
    
    
        if self.ss.notification_type == "Weekly":
            weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            st.pills("Wochentage", options=weekdays, selection_mode="multi", key="weekly_input")

            if st.button("Fertig"):
                self.ss.notification_times = self.ss["weekly_input"]
                st.rerun()

    
        elif self.ss.notification_type == "Daily":
            times_a_day = st.selectbox("Wie oft pro Tag?", list(range(1, 4)))
    
            for i in range(1, times_a_day+1):
                notification_label = f"{str(i)}\\. Erinnerungszeitpunkt"
                st.time_input(notification_label, key=f"time_input{i}")
    
            if st.button("Fertig"):
                for i in range(1, times_a_day+1):
                    self.ss.notification_times.append(self.ss[f"time_input{i}"])
                st.rerun()
    


    # def add_variable_with_fitfile():
    #     uploaded_file = st.file_uploader("FIT-Datei hochladen", type=["fit"])
    #     if uploaded_file is not None:
    #         fit_data = read_fit_file(uploaded_file)
    #         st.write("FIT-Daten:", fit_data)         



st.title("📊 Variable Hinzufügen", "variable_hinzufuegen")
page = AddVariablePage()

# selection = st.selectbox("Wie willst du deine Variable erstellen?", ["Manuell", "Fitfile"])

# if  selection == "Fitfile":
#     add_variable_with_fitfile()
# elif selection == "Manuell":
#     add_variable_manually()







