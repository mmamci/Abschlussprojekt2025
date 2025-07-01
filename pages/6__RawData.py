import streamlit as st


def view_page():
    ss = st.session_state
    st.header("Raw Data:")

    ss.variableHandle.read_variables()

    for var in ss.variableHandle.current_variables:
        st.divider()
        st.subheader(f"- {var.name}")
        st.write(f"Ziel: {var.goal}")

        print(var.data)

        for entry in var.data:
            st.write(f"{entry.date}: {entry.value} {var.unit}")

# view_page() For debugging purpouses
