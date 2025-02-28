import streamlit as st
from services.db_service import get_db
from controllers.researcher import get_researcher_by_orcid, create_researcher
from utils.constants import DIVIDER_COLOR



def signup_view():

    st.subheader("Signup / Login", divider=DIVIDER_COLOR)
    orcid_input = st.text_input("Enter your ORCID ID:")
    full_name = st.text_input("Enter your Full Name (if new):")
    department = st.text_input("Enter your Department Affiliation (if new):")
    position = st.selectbox("Select your position:", ["Student", "Postdoc", "Professor"])

    if st.button("Submit"):
        with next(get_db()) as db:
            if orcid_input:
                researcher = get_researcher_by_orcid(db, orcid_input)
                if researcher:
                    # Store the ORCID in session state for later use in other views.
                    st.session_state.orcid = orcid_input
                    st.rerun()
                else:
                    if full_name and department:
                        researcher = create_researcher(db, orcid_input, full_name, department, position)
                        # Store the ORCID in session state for later use in other views.
                        st.session_state.orcid = orcid_input
                        st.rerun()
                    else:
                        st.error("Please provide full name for new registration.")
            else:
                st.error("Please provide ORCID ID.")


