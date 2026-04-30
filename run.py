from pathlib import Path

from pdf_fetcher.indexer import QdrantIndexer
from pdf_fetcher.rag import PDFRAG

indexer = QdrantIndexer()
indexer.create_collection()
indexer.index_pdf_folder(Path("data/pdfs"))

rag = PDFRAG()

question = input("Type question here: ")
result = rag.ask(question)

print("\nAnswer")
print(result["answer"])
print("\nSource")
print(result["sources"])

print("\nSCREENSHOT")
print(result["screenshot"])
