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

    def index_pdf_folder(self, pdf_dir: Path):
        """
        Index all approved and non-processed PDF files from the specified directory.

        The process follows these steps:
        1. Loads the allowed PDF filenames from an Excel registry.
        2. Loads the list of previously indexed files from a JSON registry.
        3. Iterates through all PDF files in the target directory.
        4. Skips files that are either not allowed or already processed.
        5. Extracts text chunks from eligible PDFs.
        6. Generates vector embeddings for each text chunk.
        7. Batch-upserts the vector points along with their text payload into Qdrant.
        8. Updates the local JSON registry to track progress.

        Args:
            pdf_dir (Path): The directory path containing the PDF documents to index.

        Returns:
            None
        """
        # Load the whitelist of approved filenames
        allowed_files = get_allowed_pdf_files(Path("data/registry.xlsx"))
        indexed_file_path = Path("data/indexed_files.json")

        # Load already indexed files to avoid duplicate work
        if indexed_file_path.exists():
            with open(indexed_file_path, "r", encoding="utf-8") as f:
                indexed_files = set(json.load(f))
        else:
            indexed_files = set()

        # Iterate through all PDF files in the provided directory
        for pdf_path in pdf_dir.glob("*.pdf"):

            # Skip the file if it's not present in the allowed Excel whitelist
            if pdf_path.name not in allowed_files:
                print(f"Skipping not allowed: {pdf_path.name}")
                continue

            # Skip the file if it has already been processed in a previous run
            if pdf_path.name in indexed_files:
                print(f"Already indexed: {pdf_path.name}")
                continue

            print(f"\nProcessing: {pdf_path.name}")

            # Parse the PDF and extract text chunks with metadata
            chunks = extract_chunks_from_pdf(pdf_path)
            print(f"Chunks extracted: {len(chunks)}")

            # If the PDF is empty or unreadable, mark it as processed and skip
            if not chunks:
                indexed_files.add(pdf_path.name)
                self._save_indexed_files(indexed_file_path, indexed_files)
                continue

            points = []

            # Generate embeddings and construct Qdrant PointStructs
            for chunk in chunks:
                # Convert text chunk into a high-dimensional vector
                vector = self.embedder.embed(chunk["text"])

                # Create a database point with a unique UUID, vector, and text payload
                points.append(
                    PointStruct(
                        id=str(uuid4()),
                        vector=vector,
                        payload=chunk,
                    )
                )

            # Bulk upsert all generated vector points into the Qdrant collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )

            # Update the registry file to record successful indexing
            indexed_files.add(pdf_path.name)
            self._save_indexed_files(indexed_file_path, indexed_files)

            print(f"Saved: {pdf_path.name}")

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
