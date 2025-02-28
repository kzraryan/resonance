import streamlit as st
import streamlit.components.v1 as components
from utils.constants import QDRANT_URL

# URL of your Qdrant UI

def visualize_view():

    # Embed the Qdrant UI using an iframe
    # components.iframe(f'{QDRANT_URL}/dashboard/#/collections/publication_vector/visualize', height=1000, width=1800)

    st.markdown(
        f"""
        <style>
          .big-button {{
              display: block;
              width: 100%;
              background-color: #FF9966;
              color: white;
              padding: 20px;
              text-align: center;
              font-size: 24px;
              border: none;
              border-radius: 8px;
              margin-bottom: 20px;
              text-decoration: none;
          }}
          .big-button:hover {{
              background-color: #FF7744
          }}
        </style>
        <a href="{QDRANT_URL}/dashboard/#/collections/publication_vector/visualize" target="_blank" class="big-button">
          Open Qdrant UI
        </a>
        """,
        unsafe_allow_html=True,
    )

    # st.markdown(f"[Open Qdrant UI]({QDRANT_URL}/dashboard/#/collections/publication_vector/visualize)", unsafe_allow_html=True)