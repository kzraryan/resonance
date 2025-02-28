from models.models import Search, SearchResult, to_dict
from langchain_community.vectorstores import Qdrant
from typing import List, Dict
from controllers.publication_metadata import get_metadata_by_publication
from langchain_ollama import OllamaEmbeddings
from utils.constants import VECTOR_EMBED_MODEL, PUBLICATION_VECTOR_DATABASE_NAME, QDRANT_URL
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

def log_search(db, researcher_id: int, search_text: str) -> Search:
    # Log a new search query for the given researcher.
    new_search = Search(researcher_id=researcher_id, search_text=search_text)
    db.add(new_search)
    db.commit()
    db.refresh(new_search)
    return new_search

def log_search_result(db, search_id: int, publication_id: int, order_index: int) -> SearchResult:
    # Log a search result with the given order index to preserve fetch order.
    result = SearchResult(search_id=search_id, publication_id=publication_id, order_index=order_index)
    db.add(result)
    db.commit()
    return result

def get_search_results(db, search_id: int):
    # Retrieve all search results for a search, ordered by their fetch order.
    return db.query(SearchResult).filter(SearchResult.search_id == search_id).order_by(SearchResult.order_index).all()

def search_wrapper(db, researcher_id,  search_text, k):
    embedding = OllamaEmbeddings(
        model=VECTOR_EMBED_MODEL
    )
    qdrant_client = QdrantClient(url=QDRANT_URL)

    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=PUBLICATION_VECTOR_DATABASE_NAME,
        embedding=embedding
    )

    return search_research(db, researcher_id, vector_store, search_text, k)

def search_research(db, researcher_id: int, vector_db, query: str, k: int = 5) -> List[Dict]:
    """
    Log a search query, perform a similarity search in the vector_db, log each search result,
    and return the results as a list of dictionaries.
    """


    # Log the search query in the DB
    search_entry = log_search(db, researcher_id, query)

    # Execute similarity search with the provided query string
    results_with_score = vector_db.similarity_search_with_score(query=query, k=k)
    print(results_with_score)
    results = []
    for idx, (doc, score) in enumerate(results_with_score):
        # Extract metadata from the document
        publication_id = doc.metadata.get("publication_id")
        title = doc.metadata.get("title")
        year = doc.metadata.get("year")
        department = doc.metadata.get("department")
        full_name = doc.metadata.get("full_name")
        position = doc.metadata.get("position")

        # Log each result into the DB, preserving the order
        log_search_result(db, search_entry.id, publication_id, order_index=idx)

        metadata_record = get_metadata_by_publication(db, publication_id)
        metadata_dict = to_dict(metadata_record) if metadata_record else {}

        results.append({
            "publication_id": publication_id,
            "title": title,
            "year": year,
            "department": department,
            "full_name": full_name,
            "position": position,
            "score": score,
            "order_index": idx,
            "metadata": metadata_dict
        })

    return results