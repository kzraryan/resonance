import streamlit as st
from services.db_service import get_db
from controllers.publication import get_publications_by_researcher
from controllers.researcher import get_all_researchers
from utils.constants import DIVIDER_COLOR


def exploration_view():
    orcid = st.session_state.get("orcid", None)

    if not orcid:
        st.error("Please log in first.")
        return

    with next(get_db()) as db:
        researchers = get_all_researchers(db)
        if not researchers:
            st.warning("No researchers found.")
            return

        # Build a list of all publications from all researchers.

        for researcher in researchers:
            if researcher.orcid_id != orcid:
                pubs = get_publications_by_researcher(db, researcher.id)
                pubs_count = len(pubs)
                with st.expander(f'{researcher.full_name} - {pubs_count} publications', expanded=False):
                    all_publications = []
                    for pub in pubs:
                        all_publications.append({
                            "researcher": researcher.full_name,
                            "orcid": researcher.orcid_id,
                            "title": pub.title,
                            "year": pub.year,
                            "doi": pub.doi
                        })
                    if all_publications:
                        st.dataframe(all_publications)
                    else:
                        st.warning("No publications found.")



