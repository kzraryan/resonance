import streamlit as st
from views import signup, search, import_publications, researchers
from streamlit_option_menu import option_menu



def main():
    # Configure the page
    st.set_page_config(page_title="Researcher Portal", layout="wide")

    # Check for ORCID in session state to determine login status.
    if "orcid" not in st.session_state or not st.session_state["orcid"]:
        # If not logged in, always show the signup page.
        signup.signup_view()
    else:
        with st.sidebar:
            st.markdown("## Navigation")
            selected = option_menu(
                menu_title=None,  # No title to show
                options=["Import Publications", "Search Publications", "Researchers"],
                icons=["upload", "search", "book"],  # Use appropriate icons from Bootstrap Icons
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
            )
            # Display a logout button below the option menu.
            if st.button("Logout"):
                st.session_state.pop("orcid", None)
                st.rerun()

        # Render the selected view.
        if selected == "Import Publications":
            import_publications.import_publications_view()
        elif selected == "Search Publications":
            search.search_view()
        elif selected == "Researchers":
            researchers.exploration_view()


if __name__ == "__main__":
    main()
