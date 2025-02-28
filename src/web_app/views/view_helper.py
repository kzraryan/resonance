import streamlit as st

def central_subheader(content):
    return st.markdown(
        f"<div style='text-align: center; font-size: 1.75rem; font-weight: 600; margin-bottom: 1rem;'>{content}</div>",
        unsafe_allow_html=True,
    )
