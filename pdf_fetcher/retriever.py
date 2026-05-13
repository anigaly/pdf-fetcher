from qdrant_client import QdrantClient
from pdf_fetcher.embedding_client import EmbeddingClient


class QdrantRetriever:
    def __init__(self):
        self.collection_name = "pdf_rag"

        self.client = QdrantClient(path="data/qdrant")

        self.embedder = EmbeddingClient()

    def search(self, question: str, limit: int = 20):
        query_vector = self.embedder.embed(question)

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
        )

        return results.points
