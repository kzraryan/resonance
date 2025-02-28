import streamlit as st
from services.db_service import get_db
from controllers.researcher import get_researcher_by_orcid
from controllers.publication import import_publications_from_online, include_publications
from utils.constants import DIVIDER_COLOR
from views.view_helper import central_subheader


def import_publications_view():
    # st.subheader("Import Publications from Online Sources", divider=DIVIDER_COLOR)
    orcid = st.session_state.get("orcid", None)

    if not orcid:
        st.error("Please log in first.")
        return

    with next(get_db()) as db:
        researcher = get_researcher_by_orcid(db, orcid)
        if not researcher:
            st.error("Researcher not found. Please sign up first.")
            return

        # st.subheader("Fetched Publications")
        import_btn = st.button("Import Selected Publications", type="secondary")
        # central_subheader("All Publications")

        # Only import publications if not already in session_state
        if "imported_publications" not in st.session_state:
            with st.spinner("Importing publications, please wait..."):
                st.session_state.imported_publications = import_publications_from_online(db, researcher.id)

        imported_publications = st.session_state.imported_publications
        selected_indices = []

        if imported_publications:
            for idx, pub in enumerate(imported_publications):
                # Display checkboxes for selection; using title and year as display
                if st.checkbox(f"{pub.title} ({pub.year})", key=f"pub_{idx}", value=True):
                    selected_indices.append(idx)

            if import_btn:
                # Build a list of publication data dictionaries for selected publications.
                publications_data = []
                for idx in selected_indices:
                    pub = imported_publications[idx]
                    publications_data.append({
                        "doi": pub.doi,
                        "title": pub.title,
                        "abstract": pub.abstract,
                        "year": pub.year
                    })

                if publications_data:
                    # Include publications (insert into the DB) without duplicates.
                    created = include_publications(db, researcher.id, publications_data)
                    st.success(f"{len(created)} new publications imported.")
                else:
                    st.error("No publications imported.")
        else:
            st.write("No publications were imported from online sources.")
