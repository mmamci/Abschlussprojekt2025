import streamlit as st

class Authenticator:
    def __init__(self):
        self.ss = st.session_state
    
        if "authenticated" not in self.ss:
            self.ss.authenticated = False

        if not self.ss.authenticated:
            self.create_authentication_popup()
        else:
            st.header(f"Angemeldet als: {self.ss.variableHandle.user}")

    @st.dialog("Anmeldung")
    def create_authentication_popup(self):
        st.header("Login")
        self.username = st.text_input("Benutzername")
        self.password = st.text_input("Passwort", type="password")

        if st.button("Login"):
            self.ss.variableHandle.user = self.username
            print(self.ss.variableHandle.user)
            self.ss.variableHandle.password = self.password
            self.ss.authenticated = True
            st.rerun()
            
    


