import streamlit as st


st.title("Variable Hinzufügen","variable_hinzufuegen")

st.text_input("Name der Variable")
st.text_input("Einheit")



@st.dialog("Create Notification")
def create_notificaiton():
    st.write("Benachrichtigung erstellen")
    notification_types = ["Daily", "Weekly", "Monthly"]
    
    notification_type = st.selectbox("Benachrichtigungstyp", notification_types)
    
    notification_times = []

    if notification_type == "Weekly":
        weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        st.pills("Wochentage", options=weekdays, selection_mode="multi")

    elif notification_type == "Daily":
        times_a_day = st.selectbox("Wie oft pro Tag?", list(range(1, 11)))

        for i in range(1, times_a_day+1):
            notification_label = f"{str(i)}\. Erinnerungszeitpunkt"
            notification_times.append(st.time_input(notification_label))

col1, col2 = st.columns([4, 1])
with col1:
    st.write("Keine Benachrichtigungen")
with col2:
    if st.button("Erstellen"):
        create_notificaiton()

st.text_input("Ziel der festgelegten variable")

st.button("Variable Erstellen")