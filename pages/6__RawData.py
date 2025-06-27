import streamlit as st

ss = st.session_state
st.header("Raw Data:")
 
ss.variableHandle.read_variables()

for var in ss.variableHandle.current_variables:
    st.divider()
    st.subheader(f"- {var.name}") 
    st.write(f"Ziel: {var.goal}")
    
    for entry in var.data:
        st.write(f"{entry.date}: {entry.value} {var.unit}")