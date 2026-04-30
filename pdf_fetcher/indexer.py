from pathlib import Path
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

from pdf_fetcher.extractor import extract_chunks_from_pdf


class QdrantIndexer:
    def __init__(self):
        self.collection_name = "pdf_rag"
        self.client = QdrantClient(host="localhost", port=6333)
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.vector_size = self.model.get_sentence_embedding_dimension()

    def create_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def index_pdf_folder(self, pdf_dir: Path):
        points = []

        for pdf_path in pdf_dir.glob("*.pdf"):
            print(f"\nProcessing file: {pdf_path.name}")

            chunks = extract_chunks_from_pdf(pdf_path)
            print(f"Chunks: {len(chunks)}")

            for chunk in chunks:
                vector = self.model.encode(chunk["text"]).tolist()

                points.append(
                    PointStruct(
                        id=str(uuid4()),
                        vector=vector,
                        payload=chunk,
                    )
                )

        print("\nUploading to Qdrant...")
        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

        print("Done indexing!")
