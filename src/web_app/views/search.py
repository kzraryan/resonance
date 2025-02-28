# views/search_view.py
import streamlit as st
from services.db_service import get_db
from controllers.search import search_research, search_wrapper
from controllers.researcher import get_researcher_by_orcid
from services.qdrant_service import get_vector_store
from utils.constants import DIVIDER_COLOR


def search_view():
    st.subheader("Search Publications", divider=DIVIDER_COLOR)
    search_text = st.text_input("Enter your search query:")

    if st.button("Search"):
        # Use the ORCID from session state (set during signup)
        orcid = st.session_state.get("orcid", None)
        if not orcid:
            st.error("Please log in first.")
            return

        with next(get_db()) as db:
            researcher = get_researcher_by_orcid(db, orcid)
            if not researcher:
                st.error("Researcher not found. Please sign up first.")
                return

            # Initialize the Qdrant vectorstore using a collection name (here, using ORCID)

            results = search_wrapper(db, researcher.id,search_text, k=5)

            print(results)

            if results:
                st.subheader("Search Results")
                st.table(results)
            else:
                st.write("No results found.")
