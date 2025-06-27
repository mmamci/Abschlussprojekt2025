import streamlit as st
from utils.variable import Variable, VariableHandle

def build_main_page():
    st.set_page_config(
        page_title="Startseite",   
        page_icon="🏠",            
        layout="wide"
    )
    
    st.title("🏠 Willkommen zu deinem Gesundheits-Tracking-Dashboard")
    
    st.markdown(
        "Diese App hilft dir dabei, deine persönlichen Gesundheitsdaten einfach zu erfassen und zu analysieren.\n"
        "Nutze die Navigation links, um loszulegen:"
    )
    
    st.markdown("---")
    
    # Erste Reihe mit 2 Spalten
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.markdown("<h2 style='font-size:48px'>➕</h2>", unsafe_allow_html=True)
        st.subheader("Variable erstellen")
        st.write("Erstelle individuelle Variablen wie Schritte, Wasserzufuhr, Schlaf usw.")
    
    with row1_col2:
        st.markdown("<h2 style='font-size:48px'>✍️</h2>", unsafe_allow_html=True)
        st.subheader("Werte eintragen")
        st.write("Trage tägliche Werte zu deinen Variablen ein, um deinen Fortschritt zu verfolgen.")
    
    # Abstand einfügen (z.B. 3 leere Zeilen)
    st.write("")
    st.write("")
    st.write("")
    
    # Zweite Reihe mit 2 Spalten
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.markdown("<h2 style='font-size:48px'>📆</h2>", unsafe_allow_html=True)
        st.subheader("Kalenderansicht")
        st.write("Sieh dir alle Einträge übersichtlich im Kalender an.")
    
    with row2_col2:
        st.markdown("<h2 style='font-size:48px'>📈</h2>", unsafe_allow_html=True)
        st.subheader("Diagramm-Ansicht")
        st.write("Verfolge deine Fortschritte mit anschaulichen Diagrammen.")
    
    # Abstand
    st.write("")
    st.write("")
    
    # Dritte Reihe mit 1 Spalte (Highlight separat)
    st.markdown("<h2 style='font-size:48px'>🏆</h2>", unsafe_allow_html=True)
    st.subheader("Highlights entdecken")
    st.write("Besondere Erfolge und Entwicklungen deiner Gesundheitsreise auf einen Blick.")
    
    st.markdown("---")

build_main_page()