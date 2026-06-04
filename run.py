from pathlib import Path

from pdf_fetcher.indexer import QdrantIndexer
from pdf_fetcher.rag import PDFRAG

# 1. Initialize the Qdrant indexer client
indexer = QdrantIndexer()

# 2. Recreate collection only when you want to re-index from scratch
indexer.create_collection()

# 3. Define the path to your PDFs folder
pdf_directory = Path("data/pdfs")

# 4. FIXED: Call the updated universal function instead of index_pdf_folder
indexer.index_specific_pdfs(pdf_directory)

# 5. Close the indexer client connection safely
indexer.client.close()

# 6. Initialize the RAG engine for questioning
rag = PDFRAG()

# 7. Capture user intent via terminal input
question = input("Type question here: ")

# 8. Execute the RAG pipeline
result = rag.ask(question)

# 9. Print the generated natural language response from the LLM
print("\nAnswer:")
print(result["answer"])

# 10. Print formatted metadata references
print("\nSources:")
for source in result["sources"]:
    print(
        f"- {source['file']} | "
        f"page {source['page']} | "
        f"score={source['score']:.3f}"
    )

# 11. Print the file path to the generated page screenshot
print("\nSCREENSHOT:")
print(result["screenshot"])
