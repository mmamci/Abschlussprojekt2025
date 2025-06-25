import streamlit as st

def write_as_pills(content):
    st.markdown(
        "<div style='display:flex;flex-wrap:wrap;gap:6px;'>" +
        "".join(f"<span style='background:#eee;border-radius:12px;padding:4px 10px;'>{c}</span>"
                for c in content) +
        "</div>", unsafe_allow_html=True
    )