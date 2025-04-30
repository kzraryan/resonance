import pandas as pd

from langchain_ollama import OllamaEmbeddings
from utils.constants import VECTOR_EMBED_MODEL, LOINC_VECTOR_DATABASE_NAME, QDRANT_URL
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

def search_loinc(loinc_nums):
    loincs = 'loinc.csv'
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


# Initialize the Qdrant vectorstore using a collection name (here, using ORCID)


bm = 'BIOMARKERS.csv'
bm_df = pd.read_csv(bm)

df = pd.DataFrame(columns=['LOINC_NUM', 'LONG_COMMON_NAME', 'BIOMARKER', 'SCORE'])

for index, row in bm_df.iterrows():
    results_df, scores = search_wrapper(row['BIOMARKER'], k=20)
    results_df['score']=scores
    print(row['BIOMARKER'])
    if len(results_df) > 0:
        temp = pd.DataFrame()
        temp['LOINC_NUM'] = results_df['LOINC_NUM']
        temp['LONG_COMMON_NAME'] = results_df['LONG_COMMON_NAME']
        temp['BIOMARKER'] = row['BIOMARKER']
        temp['SCORE'] = results_df['score']
        df = pd.concat([df, temp], ignore_index=True)


df.to_csv('loinc_biomarker_match.csv', index=False)