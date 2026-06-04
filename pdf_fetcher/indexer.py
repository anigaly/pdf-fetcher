import collections
import json
from pathlib import Path
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from pdf_fetcher.extractor import extract_chunks_from_pdf
from pdf_fetcher.file_filter import get_allowed_pdf_files
from pdf_fetcher.embedding_client import EmbeddingClient


class QdrantIndexer:
    """
    Handles the creation and population of a Qdrant vector database collection
    for PDF-based Retrieval-Augmented Generation (RAG).

    This class extracts text chunks from PDF documents, generates high-dimensional
    embeddings for each chunk using an external embedding client, and stores them
    as vector points in a local Qdrant collection. It also manages a local registry
    to prevent redundant processing of already indexed files.
    """

    def __init__(self):
        """
        Initialize the Qdrant indexer client and configuration.

        Sets up the connection to the local Qdrant instance, initializes the
        embedding model client, defines the target collection name, and sets
        the embedding vector dimensionality.
        """
        self.collection_name = "pdf_rag"

        # Initialize the local Qdrant client specifying the storage path
        self.client = QdrantClient(path="data/qdrant")

        # Initialize the client responsible for generating text embeddings
        self.embedder = EmbeddingClient()

        # Define the dimensionality of the vectors (e.g., 1024 for large models)
        self.vector_size = 1024

    def create_collection(self):
        """
        Create the Qdrant collection if it does not already exist.

        Fetches all existing collections from the Qdrant database. If the target
        collection (`self.collection_name`) is missing, it creates a new one
        configured with Cosine similarity and the specified vector size.

        Returns:
            None
        """
        # Fetch the list of all existing collections from the database
        collections_response = self.client.get_collections()

        # Extract names into a set for O(1) lookups
        existing_names = {
            col.name for col in collections_response.collections
        }

        # Abort if the collection is already present
        if self.collection_name in existing_names:
            print(f"Collection already exists: {self.collection_name}")
            return

        # Create a new collection with the required vector configurations
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )
        print(f"Collection created: {self.collection_name}")

    def index_specific_pdfs(self, pdf_paths: list[Path] | Path):
        """
        Index PDF files. Accepts either a list of specific file paths or a single
        directory path. If a directory path is given, it extracts all PDF files from it.
        """
        # --- FIXED: Check if the input is a single directory path ---
        if isinstance(pdf_paths, Path) and pdf_paths.is_dir():
            print(f"Directory detected. Scanning for all PDFs in: {pdf_paths}")
            pdf_paths = list(pdf_paths.glob("*.pdf"))

        indexed_file_path = Path("data/indexed_files.json")

        # Load already indexed files
        if indexed_file_path.exists():
            with open(indexed_file_path, "r", encoding="utf-8") as f:
                indexed_files = set(json.load(f))
        else:
            indexed_files = set()

        # Iterate through the provided files
        for pdf_path in pdf_paths:
            if not pdf_path.exists():
                print(f"File does not exist: {pdf_path}")
                continue

            if pdf_path.name in indexed_files:
                print(f"Already indexed: {pdf_path.name}")
                continue

            print(f"\nProcessing: {pdf_path.name}")
            chunks = extract_chunks_from_pdf(pdf_path)
            print(f"Extracted {len(chunks)} chunks")

            if not chunks:
                indexed_files.add(pdf_path.name)
                self._save_indexed_files(indexed_file_path, indexed_files)
                continue

            points = []
            for chunk in chunks:
                try:
                    vector = self.embedder.embed(chunk["text"])
                    points.append(
                        PointStruct(
                            id=str(uuid4()),
                            vector=vector,
                            payload=chunk,
                        )
                    )
                except Exception as e:
                    print(f"Embedding failed for a chunk in {pdf_path.name}: {e}")
                    continue

            if not points:
                print(f"No valid chunks to upload for: {pdf_path.name}")
                continue

            # Upload vectors to Qdrant database
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

            # Save progress to the indexed files list
            indexed_files.add(pdf_path.name)
            self._save_indexed_files(indexed_file_path, indexed_files)
            print(f"Successfully saved to database: {pdf_path.name}")

    def _save_indexed_files(self, file_path: Path, indexed_files: set):
        """
        Save the updated set of indexed files back to the JSON registry.

        Converts the Python `set` into a `list` to make it JSON serializable,
        then writes it to the disk with clean formatting.

        Args:
            file_path (Path): The destination path for the JSON registry file.
            indexed_files (set): A set containing the names of processed files.

        Returns:
            None
        """
        with open(file_path, "w", encoding="utf-8") as f:
            # Convert set to list since sets cannot be directly serialized to JSON
            json.dump(list(indexed_files), f, ensure_ascii=False, indent=4)
