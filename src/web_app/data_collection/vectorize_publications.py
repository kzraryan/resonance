from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from utils.constants import VECTOR_EMBED_MODEL, QDRANT_URL, PUBLICATION_VECTOR_DATABASE_NAME
import pandas as pd


def prepare_documents(researcher_df, publication_df, publication_metadata_df):

    publication_df = publication_df.rename(columns={'id': 'publication_id'})
    researcher_df = researcher_df.rename(columns={'id': 'researcher_id'})


    merged_df = publication_df.merge(publication_metadata_df, on="publication_id", how="left") \
        .merge(researcher_df, on="researcher_id", how="left")

    documents = []
    for _, row in merged_df.iterrows():
        # Compose the page content from title and abstract.
        page_content = f"Title: {row['title']}\nAbstract: {row['abstract']}"

        # Build metadata: start with all columns from metadata_df.
        meta = {}
        for col in publication_metadata_df.columns:
            meta[col] = row.get(col, "")

        # Add publication year from publication_df.
        meta["year"] = row.get("year", "")

        # Add researcher info from researcher_df.
        meta["department"] = row.get("department", "")
        meta["title"] = row.get("title", "")
        meta["full_name"] = row.get("full_name", "")
        meta["position"] = row.get("position", "")

        # Optionally, also include ids.
        meta["publication_id"] = row.get("publication_id", "")
        meta["researcher_id"] = row.get("researcher_id", "")

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
        prefer_grpc = False,
        collection_name=PUBLICATION_VECTOR_DATABASE_NAME,
    )

    return store

if __name__ == '__main__':
    researchers = 'researchers_1.csv'
    publications = 'publications_1.csv'
    publication_metadata = 'publication_metadata_1.csv'

    rdf = pd.read_csv(researchers)
    pub_df = pd.read_csv(publications)
    pub_meta_df = pd.read_csv(publication_metadata)

    docs = prepare_documents(rdf, pub_df, pub_meta_df)
    create_vector_embeddings(docs)