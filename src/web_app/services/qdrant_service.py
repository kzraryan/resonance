
from langchain_ollama import OllamaEmbeddings
from utils.constants import VECTOR_EMBED_MODEL, PUBLICATION_VECTOR_DATABASE_NAME, QDRANT_URL
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# Qdrant server URL
def get_vector_store():

    embedding = OllamaEmbeddings(
        model=VECTOR_EMBED_MODEL
    )
    qdrant_client = QdrantClient(url=QDRANT_URL, embedding=embedding)


    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name="demo_collection"
    )
    return vector_store