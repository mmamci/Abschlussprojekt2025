import streamlit as st

class Authenticator:
    def __init__(self):
        self.ss = st.session_state

        with open("data/userlist.txt", "r", encoding="utf-8") as f:
            self.userlist = f.readlines()

        if "authenticated" not in self.ss:
            self.ss.authenticated = False

        if not self.ss.authenticated:
            self.create_authentication_popup()
        else:
            st.info(f"Angemeldet als: {self.ss.variableHandle.user}")

    @st.dialog("Anmeldung")
    def create_authentication_popup(self):
        st.header("Login")
        self.username = st.text_input("Benutzername")

        if self.username != "":
            if self.username in self.userlist:
                self.password = st.text_input("Passwort", type="password")

                if st.button("Login"):
                    self.ss.variableHandle.user = self.username
                    print(self.ss.variableHandle.user)
                    self.ss.variableHandle.password = self.password
                    self.ss.authenticated = True
                    st.rerun()

            else:
                self.password = st.text_input("Passwort", type="password")
                repeat_password = st.text_input("Passwort Wiederholen", type="password")

                if repeat_password == self.password:
                    if st.button("Create New Account"):
                        self.ss.variableHandle.user = self.username
                        self.ss.variableHandle.password = self.password

                        with open("data/userlist.txt", "a", encoding="utf-8") as f:
                            f.write(self.username)

                        self.ss.authenticated = True
                        st.rerun()

                else:
                    st.warning("Passwords did not Match")
            
            
    


