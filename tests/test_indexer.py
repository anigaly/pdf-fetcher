import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pdf_fetcher.indexer import QdrantIndexer


# Create indexer
indexer = QdrantIndexer()

# Create collection
indexer.create_collection()

# Index only one PDF for testing
pdf_folder = Path("data/pdfs")

indexer.index_pdf_folder(pdf_folder)

print("Indexing finished successfully")
