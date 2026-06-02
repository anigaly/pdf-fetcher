from pathlib import Path

from pdf_fetcher.indexer import QdrantIndexer
from pdf_fetcher.rag import PDFRAG

# 1. Initialize the Qdrant indexer client
indexer = QdrantIndexer()

# 2. Recreate collection only when you want to re-index from scratch
indexer.create_collection()

# 3. Define the specific list of PDFs to be indexed
specific_pdfs = [
    Path("data/pdfs/637_2.pdf"),
    Path("data/pdfs/289_2.pdf"),
    Path("data/pdfs/331_2.pdf"),
]

# 4. Index only the specified PDF files instead of the whole folder
indexer.index_specific_pdfs(specific_pdfs)

# 5. Close the indexer client connection safely
indexer.client.close()

# 6. Initialize the RAG engine for questioning
rag = PDFRAG()

# 7. Capture user intent via terminal input
question = input("Type question here: ")

# 8. Execute the RAG pipeline
result = rag.ask(question)

# 9. Print the generated natural language response from the LLM
print("\nAnswer")
print(result["answer"])

# 10. Print formatted metadata references with exact file name, page, and similarity score
print("\nSources:")
for source in result["sources"]:
    print(
        f"- {source['file']} | "
        f"page {source['page']} | "
        f"score={source['score']:.3f}"
    )

# 11. Print the file path to the generated page screenshot
print("\nSCREENSHOT")
print(result["screenshot"])
