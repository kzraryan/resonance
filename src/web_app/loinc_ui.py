import streamlit as st
import pandas as pd

from langchain_ollama import OllamaEmbeddings
from utils.constants import VECTOR_EMBED_MODEL, LOINC_VECTOR_DATABASE_NAME, QDRANT_URL, METADATA_LLM_MODEL
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import re

from langchain_ollama import OllamaLLM

# increased aortic root diameter heart imaging traits vascular assessment
# Increased total cholesterol and LDL cholesterol levels liver body fluid plasma

def search_loinc(loinc_nums):
    loincs = 'src/web_app/loinc.csv'
    loincs_df = pd.read_csv(loincs)

    result_df = loincs_df[loincs_df['LOINC_NUM'].isin(loinc_nums)]
    return result_df

def search_wrapper(search_text, k):
    embedding = OllamaEmbeddings(
        model=VECTOR_EMBED_MODEL
    )
    qdrant_client = QdrantClient(url=QDRANT_URL)

    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name='LOINC_SHORT',
        embedding=embedding
    )

    results_with_score = vector_store.similarity_search_with_score(query=search_text, k=k)
    loinc_nums = []
    scores = []
    for idx, (doc, score) in enumerate(results_with_score):
        # Extract metadata from the document
        loinc_nums.append(doc.metadata.get("LOINC_NUM"))
        scores.append(score)

    return search_loinc(loinc_nums), scores

def generate_publication_metadata(content):
    llm = OllamaLLM(
        model=METADATA_LLM_MODEL
    )
    prompt_text = """
        You are an expert medical laboratory coding expert. The goal provide user a confidence level between 0 to 1 of
         how likely a certain LOINC code is needed to calculate a BIOMARKER.
         The user will provide LOINC and BIOMARKER, your response should only be a number between 0 to 1."""

    prompt_text += content

    raw_response = llm.invoke(prompt_text)

    return raw_response

st.subheader("Search LOINCS")
search_text = st.text_input("Enter your search query:")

if st.button("Search"):


    # Initialize the Qdrant vectorstore using a collection name (here, using ORCID)

    with st.spinner("Importing publications, please wait..."):
        results_df, scores = search_wrapper(search_text, k=20)

    results_df['score']=scores

    filtered_df = results_df[results_df['score'] > 0.7]

    for index, row in filtered_df.iterrows():
        llm_result = generate_publication_metadata(f'LOINC:{row["LONG_COMMON_NAME"]}  BIOMARKER:{search_text}')
        filtered_df.at[index,'LLM_REASON'] = llm_result
        filtered_df.at[index,'LLM_SCORE'] = re.sub(r'<think>.*?</think>', '', llm_result, flags=re.DOTALL)

    if len(filtered_df) > 0:
        st.dataframe(filtered_df, hide_index=True)
    else:
        st.write("No results found.")