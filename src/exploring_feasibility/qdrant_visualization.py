import streamlit as st
import pandas as pd
import numpy as np
from qdrant_client import QdrantClient
from sklearn.decomposition import PCA
import plotly.express as px
from utils.constants import PUBLICATION_VECTOR_DATABASE_NAME

# Configuration for Qdrant
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = PUBLICATION_VECTOR_DATABASE_NAME

# Create a Qdrant client (using HTTP)
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def get_points(collection_name: str, limit: int = 1000):
    """Retrieve points from the Qdrant collection using scroll."""
    scroll_result = client.scroll(collection_name=collection_name, limit=limit)
    return scroll_result.points if scroll_result and scroll_result.points else []


# Retrieve points from Qdrant
points = get_points(COLLECTION_NAME, limit=500)

if not points:
    st.error("No points found in the Qdrant collection.")
else:
    # Convert points to a DataFrame. Each point should have an id, vector, and payload.
    data = []
    for point in points:
        # Assume each point has a payload field (which is a dict) and a vector field.
        payload = point.payload if point.payload else {}
        data.append({
            "id": point.id,
            **payload,
            "vector": point.vector
        })

    df = pd.DataFrame(data)

    st.write("Raw Data from Qdrant:")
    st.dataframe(df.head())

    # Check that vector column exists and is not empty.
    if "vector" in df.columns and not df.empty:
        # Convert list of vectors to a NumPy array.
        vectors = np.array(df["vector"].tolist())

        # Optionally, apply PCA to reduce dimensions to 2D for visualization.
        if vectors.shape[1] > 2:
            pca = PCA(n_components=2)
            reduced = pca.fit_transform(vectors)
            df["pca1"] = reduced[:, 0]
            df["pca2"] = reduced[:, 1]
        else:
            # If vectors already have 2 dimensions, use them directly.
            df["pca1"] = df["vector"].apply(lambda v: v[0])
            df["pca2"] = df["vector"].apply(lambda v: v[1])

        # Create an interactive scatter plot.
        fig = px.scatter(
            df,
            x="pca1",
            y="pca2",
            hover_data=df.columns.tolist(),  # show all columns in tooltip
            title="Qdrant Collection Visualization (2D Projection)"
        )
        st.plotly_chart(fig)
    else:
        st.error("No vectors found in the retrieved data.")
