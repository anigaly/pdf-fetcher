import json
from pathlib import Path
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from pdf_fetcher.extractor import extract_chunks_from_pdf
from pdf_fetcher.file_filter import get_allowed_pdf_files
from pdf_fetcher.embedding_client import EmbeddingClient


class QdrantIndexer:
    def __init__(self):
        self.collection_name = "pdf_rag"
        self.client = QdrantClient(path="data/qdrant")

        self.embedder = EmbeddingClient()
        self.vector_size = 1024

    def create_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def index_pdf_folder(self, pdf_dir: Path):
        allowed_files = get_allowed_pdf_files(Path("data/registry.xlsx"))

        indexed_file_path = Path("data/indexed_files.json")

        if indexed_file_path.exists():
            with open(indexed_file_path, "r", encoding="utf-8") as f:
                indexed_files = set(json.load(f))
        else:
            indexed_files = set()

        for pdf_path in pdf_dir.glob("*.pdf"):

            allowed_test_files = {
                "637_2.pdf",
                "331_2.pdf",
                "289_2.pdf",
            }

            if pdf_path.name not in allowed_test_files:
                continue


            if pdf_path.name not in allowed_files:
                print(f"Skipping not selected by metadata: {pdf_path.name}")
                continue

            if pdf_path.name in indexed_files:
                print(f"Skipping already indexed: {pdf_path.name}")
                continue

            print(f"\nProcessing file: {pdf_path.name}")

            chunks = extract_chunks_from_pdf(pdf_path)
            print(f"Chunks: {len(chunks)}")

            if not chunks:
                indexed_files.add(pdf_path.name)
                self._save_indexed_files(indexed_file_path, indexed_files)
                continue

            points = []

            for chunk in chunks:
                vector = self.embedder.embed(chunk["text"])

                points.append(
                    PointStruct(
                        id=str(uuid4()),
                        vector=vector,
                        payload=chunk,
                    )
                )

            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

            indexed_files.add(pdf_path.name)
            self._save_indexed_files(indexed_file_path, indexed_files)

            print(f"Saved: {pdf_path.name}")

    def _save_indexed_files(self, indexed_file_path: Path, indexed_files: set):
        indexed_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(indexed_file_path, "w", encoding="utf-8") as f:
            json.dump(
                sorted(list(indexed_files)),
                f,
                ensure_ascii=False,
                indent=2,
            )
