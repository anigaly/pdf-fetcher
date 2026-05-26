import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pdf_fetcher.retriever import QdrantRetriever


# Create retriever
def test_retriever():
    retriever = QdrantRetriever()
    result = retriever.search("test query")
    assert result is not None


# Test medical question
question = "Какая дозировка дексаметазона используется для профилактики СДР плода?"


# Search relevant chunks
results = retriever.search(question, limit=5)


print(f"\nQUESTION:\n{question}\n")


print("TOP RESULTS:\n")


# Print retrieved chunks
for i, result in enumerate(results, start=1):

    payload = result.payload

    print(f"\nRESULT #{i}")
    print(f"Score: {result.score:.3f}")
    print(f"File: {payload['file']}")
    print(f"Page: {payload['page']}")

    print("\nTEXT:\n")

    print(payload["text"][:1000])

    print("\n" + "=" * 80)
