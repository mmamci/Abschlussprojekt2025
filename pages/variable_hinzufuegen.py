import streamlit as st

st.title("Variable Hinzufügen","variable_hinzufuegen")

st.text_input("Name der Variable")
st.text_input("Einheit")

if "notification_times" not in st.session_state:
    st.session_state.notification_times = []
if "notification_type" not in st.session_state:
    st.session_state.notification_type = ""
    
ss = st.session_state

@st.dialog("Create Notification")
def create_notificaiton():
    st.write("Benachrichtigung erstellen")
    notification_types = ["Daily", "Weekly", "Monthly"]
    
    ss.notification_type = st.selectbox("Benachrichtigungstyp", notification_types)
    

    if ss.notification_type == "Weekly":
        weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        st.pills("Wochentage", options=weekdays, selection_mode="multi")

    elif ss.notification_type == "Daily":
        times_a_day = st.selectbox("Wie oft pro Tag?", list(range(1, 11)))

        for i in range(1, times_a_day+1):
            notification_label = f"{str(i)}\\. Erinnerungszeitpunkt"
            ss.notification_times.insert(i-1, st.time_input(notification_label))

        if st.button("Fertig"):
            st.rerun()
        

# st.write("Benachrichtigungen")


if len(ss.notification_times) == 0:
    st.pills("Benachrichtigungen", ["\+"], on_change=create_notificaiton)

elif ss.notification_type == "Daily":
        notification_times_str = [i.strftime("%H:%M") for i in ss.notification_times]
        st.pills("Benachrichtigungen", notification_times_str)

st.text_input("Ziel der festgelegten variable")

st.button("Variable Erstellen")