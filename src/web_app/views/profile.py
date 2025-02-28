import streamlit as st
from services.db_service import get_db
from controllers.publication import get_publications_by_researcher
from controllers.researcher import get_researcher_by_orcid
from utils.constants import DIVIDER_COLOR


def exploration_view():

    orcid = st.session_state.get("orcid", None)

    if not orcid:
        st.error("Please log in first.")
        return

    with next(get_db()) as db:
        researcher = get_researcher_by_orcid(db, orcid)
        if not researcher:
            st.error("Researcher not found. Please sign up first.")
            return

        publications = get_publications_by_researcher(db, researcher.id)
        if publications:
            st.subheader("Your Publications", divider=DIVIDER_COLOR)
            for pub in publications:
                st.write(f"**Title:** {pub.title}  \n**Year:** {pub.year}  \n**DOI:** {pub.doi}")
                st.write("---")
        else:
            st.write("No publications found for your account.")
