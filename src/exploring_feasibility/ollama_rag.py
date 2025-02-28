from collecting_research_using_orcid import get_research_data
from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings

EMBED_MODEL = "nomic-embed-text:latest"
LLM_MODEL = "deepseek-r1:latest"
OLLAMA_URL = "http://localhost:11434/api"
QDRANT_URL = "http://localhost:6333"





def create_vector_embeddings(langchain_documents):
    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        # base_url= f'{OLLAMA_URL}/embed',
    )
    # store = Qdrant.from_documents(
    #     langchain_documents,
    #     embeddings,
    #     path="./tmp/test_run_9",
    #     collection_name="AI-Embeddings",
    # )
    store = Qdrant.from_documents(
        langchain_documents,
        embeddings,
        url=QDRANT_URL,
        prefer_grpc = False,
        collection_name="test_run_1",
    )

    return store


# Example usage:
if __name__ == "__main__":
    # Replace with a valid ORCID iD
    orcid_id_list = [
        {"author_id": "0000-0002-1859-0438", "author_name": "Dr. Praveen Rao"},
        {"author_id": "0000-0003-0122-7672", "author_name": "Md Kamruz Zaman Rana"},
    ]
    all_research = get_research_data(orcid_id_list)
    print(all_research)
    db = create_vector_embeddings(all_research)

    res = db.similarity_search_with_score(
        query="chemotherapy patient wellness",
        k=5
    )


    for i, (doc, score) in enumerate(res):
        print(doc.metadata['research_id'],doc.metadata['title'])




