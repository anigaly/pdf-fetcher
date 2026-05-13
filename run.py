from pathlib import Path

from pdf_fetcher.indexer import QdrantIndexer
from pdf_fetcher.rag import PDFRAG


indexer = QdrantIndexer()

# Recreate collection only when you want to re-index from scratch
indexer.create_collection()

indexer.index_pdf_folder(Path("data/pdfs"))

indexer.client.close()

rag = PDFRAG()

question = input("Type question here: ")
result = rag.ask(question)

print("\nAnswer")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(
        f"- {source['file']} | "
        f"page {source['page']} | "
        f"score={source['score']:.3f}"
    )

print("\nSCREENSHOT")
print(result["screenshot"])
