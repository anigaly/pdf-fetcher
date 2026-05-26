from qdrant_client import QdrantClient
from pdf_fetcher.embedding_client import EmbeddingClient


class QdrantRetriever:
    """
    Performs semantic search over a Qdrant vector database collection.

    This class converts a user's natural-language question into an embedding
    vector and searches the Qdrant collection for the most semantically
    similar document chunks. It is typically used as the retrieval component
    of a Retrieval-Augmented Generation (RAG) pipeline.

    Workflow:
        User question
            ↓
        Generate embedding
            ↓
        Search Qdrant collection
            ↓
        Return most relevant chunks
    """

    def __init__(self):
        """
        Initialize the retriever and required dependencies.

        Creates:
            - A connection to the local Qdrant database.
            - An embedding client used to convert text into vectors.
            - The target collection name containing indexed PDF chunks.
        """

        # Name of the Qdrant collection that stores PDF embeddings
        self.collection_name = "pdf_rag"

        # Connect to the local Qdrant database
        self.client = QdrantClient(path="data/qdrant")

        # Initialize the embedding generator
        self.embedder = EmbeddingClient()

    def search(self, question: str, limit: int = 20):
        """
        Search for document chunks relevant to the user's question.

        The method:
            1. Converts the question into an embedding vector.
            2. Executes a similarity search against the Qdrant collection.
            3. Returns the most relevant vector points.

        Args:
            question (str):
                The user query or question to search for.

            limit (int, optional):
                Maximum number of matching results to return.
                Defaults to 20.

        Returns:
            list:
                A list of Qdrant Point objects.

                Each point typically contains:
                    - id: Unique identifier
                    - score: Similarity score
                    - payload: Stored metadata
                      (text chunk, file name, path, chunk index)
                    - vector: Embedding vector (if requested)


        """

        # Convert the user's question into a vector representation
        query_vector = self.embedder.embed(question)

        # Perform similarity search in the Qdrant collection
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
        )

        # Return matching points ordered by similarity score
        return results.points
