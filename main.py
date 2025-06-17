import streamlit as st

pages = st.navigation(
    [
        st.Page("pages/ansicht.py", title="Anischt", icon=":material/monitoring:"),
        st.Page("pages/highlights.py", title="Highlights"),
        st.Page("pages/variable_hinzufuegen.py", title="Variable Hinzufügen"),
    ]
)
pages.run()


# with open('./style.css') as f:
#     css = f.read()

#     st.html(f"<style>{css}</style>")