import streamlit as st

def display_as_pills(content):
    st.markdown(
        "<div style='display: flex; gap: 8px; margin-bottom: 1em;'>"
        + "".join(
        f"<span style='background: #eee; color: #333; border-radius: 16px; padding: 6px 16px; font-size: 0.95em; border: 1px solid #ccc;'>{element}</span>"
        for element in content
        )
        + "</div>",
        unsafe_allow_html=True,
    )
