from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


class QdrantRetriever:
    def __init__(self):
        self.collection_name = "pdf_rag"
        self.client = QdrantClient(host="localhost", port=6333)
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def search(self, question: str, limit: int = 3):
        query_vector = self.model.encode(question).tolist()

        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
        )
