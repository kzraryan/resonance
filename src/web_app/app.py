import streamlit as st

from utils.constants import MENU_IMPORT_PUBLICATION, MENU_EXPLORE, MENU_PUBLICATIONS, MENU_PROFILE, MENU_VISUALIZE, \
    MENU_CODE_SPACE
from views import signup, search, import_publications, researchers, profile, visualize
from streamlit_option_menu import option_menu


def add_logo():
    st.markdown("""
                                <div style="display: flex; align-items: center; justify-content: center;
                                            background-color: #f0f2f6;  border-radius: 8px;">
                                    <h1 style="color: #FF5733; margin: 0; font-size: 40px">Resonance</h1>
                                </div>
                            """, unsafe_allow_html=True)
    return



def main():
    # Configure the page
    st.set_page_config(page_title="Researcher Portal", layout="wide")

    # Check for ORCID in session state to determine login status.
    if "orcid" not in st.session_state or not st.session_state["orcid"]:
        with st.sidebar:
            add_logo()
        # If not logged in, always show the signup page.
        signup.signup_view()
    else:
        src = "resources/images/logo.png"
        with st.sidebar:
            add_logo()
            selected = option_menu(
                menu_title=None,  # No title to show
                options=[MENU_IMPORT_PUBLICATION, MENU_EXPLORE, MENU_PUBLICATIONS, MENU_CODE_SPACE, MENU_VISUALIZE, MENU_PROFILE],
                icons=["upload", "search", "book", "code", "bar-chart", "person-circle"],  # appropriate icons from Bootstrap Icons
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
            )
            # Display a logout button below the option menu.
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Logout"):
                    st.session_state.clear()
                    st.rerun()

        # Render the selected view.
        if selected == MENU_IMPORT_PUBLICATION:
            import_publications.import_publications_view()
        elif selected == MENU_EXPLORE:
            search.search_view()
        elif selected == MENU_PUBLICATIONS:
            researchers.exploration_view()
        elif selected == MENU_CODE_SPACE:
            researchers.exploration_view()
        elif selected == MENU_VISUALIZE:
            visualize.visualize_view()
        elif selected == MENU_PROFILE:
            profile.exploration_view()


if __name__ == "__main__":
    main()
