from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from utils.constants import VECTOR_EMBED_MODEL, QDRANT_URL, LOINC_VECTOR_DATABASE_NAME
import pandas as pd


def prepare_documents(df):
    documents = []
    for _, row in df.iterrows():
        # Compose the page content from title and abstract.
        page_content = f"{row['LONG_COMMON_NAME']}"

        # Build metadata: start with all columns from metadata_df.
        meta = {"LOINC_NUM": row['LOINC_NUM']}

        documents.append(
            Document(
                page_content=page_content,
                metadata=meta
            )
        )
    return documents


def create_vector_embeddings(langchain_documents):
    embeddings = OllamaEmbeddings(
        model=VECTOR_EMBED_MODEL,

    )
    store = Qdrant.from_documents(
        langchain_documents,
        embeddings,
        url=QDRANT_URL,
        prefer_grpc=False,
        collection_name='LOINC_SHORT',
    )

    return store


if __name__ == '__main__':
    # researchers = 'BIOMARKERS.csv'
    loincs = 'loinc.csv'

    loincs_df = pd.read_csv(loincs)

    docs = prepare_documents(loincs_df)
    create_vector_embeddings(docs)
