# views/search_view.py
import pandas as pd
import streamlit as st
from services.db_service import get_db
from controllers.search import search_research, search_wrapper
from controllers.researcher import get_researcher_by_orcid
from services.qdrant_service import get_vector_store
from utils.constants import DIVIDER_COLOR
from collections import Counter
import json


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

            with st.spinner("Importing publications, please wait..."):
                results = search_wrapper(db, researcher.id,search_text, k=5)


            # print(results)

            results_df = pd.DataFrame(results)
            results_df["year"] = results_df["year"].astype(str)
            # df_reduced =

            if results:
                st.dataframe(results_df.drop(columns=["publication_id", "score", "order_index", "metadata"]), hide_index=True)
            else:
                st.write("No results found.")

            counter = Counter()
            print(results_df.head())

            for obj in results_df["metadata"]:
                # Get all values from the dictionary and convert to string if necessary
                for value in obj.values():
                    # Skip None values.
                    if value is None:
                        continue
                    # If value is a numeric type, skip it.
                    if isinstance(value, (int, float)):
                        continue
                    # If it's a string that represents a number, skip it.
                    if isinstance(value, str):
                        try:
                            float_val = float(value)
                            # If conversion is successful, skip this value.
                            continue
                        except ValueError:
                            # Not a numeric string, so keep it.
                            pass
                    # Otherwise, update counter (convert to string for consistency).
                    counter.update([str(value)])

                # Get the most common value (returns a list of (value, count) tuples)
            print(counter)


            options = [key for key,_ in counter.items()]
            selected = st.selectbox("Top Keywords", options)


