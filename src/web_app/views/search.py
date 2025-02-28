# views/search_view.py
import streamlit as st
from services.db_service import get_db
from controllers.search import search_research
from controllers.researcher import get_researcher_by_orcid



def search_view():
    st.title("Search Publications")
    query = st.text_input("Enter your search query:")

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
            # vectorstore = get_vectorstore(collection_name=orcid)
            # results = search_research(db, researcher.id, vectorstore, query, k=5)
            #
            # if results:
            #     st.subheader("Search Results")
            #     for result in results:
            #         st.write(f"**Title:** {result.get('title')}")
            #         st.write(f"**Publication ID:** {result.get('publication_id')}")
            #         st.write(f"**Score:** {result.get('score')}")
            #         st.write(f"**Metadata:** {result.get('metadata')}")
            #         st.write("---")
            # else:
            #     st.write("No results found.")
