from pathlib import Path

# Import the retriever class used for searching relevant chunks in Qdrant
from pdf_fetcher.retriever import QdrantRetriever

# Import the function used to save a screenshot of a PDF page
from pdf_fetcher.screenshot import save_page_screenshot


class PDFRAG:
    """
    PDFRAG handles:
    1. Retrieving relevant PDF chunks from Qdrant
    2. Returning the best matching answer
    3. Generating a screenshot of the related PDF page
    """

    def __init__(self):
        """
        Initialize the retriever object.
        """
        self.retriever = QdrantRetriever()

    def ask(self, question: str) -> dict:
        """
        Search for an answer based on the user's question.

        Args:
            question (str): User question

        Returns:
            dict: Answer, sources, and screenshot path
        """

        # Search for relevant chunks in Qdrant
        # limit=20 means retrieve up to 20 results
        results = self.retriever.search(question, limit=20)

        # Return default response if no results are found
        if not results:
            return {
                "answer": "The answer isn't found.",
                "sources": [],
                "screenshot": None,
            }

        # Keep only the top 5 most relevant results
        top_results = results[:5]

        # Get payload data from the best result
        best = top_results[0].payload

        # Generate and save a screenshot of the matching PDF page
        screenshot_path = save_page_screenshot(
            pdf_path=Path(best["path"]),  # Full path to the PDF file
            page_number=best["page"],    # PDF page number
            output_path=Path("data/screenshots")
            / f"{best['file']}_page_{best['page']}.png",
        )

        # Use the text of the best result as the answer
        answer = top_results[0].payload["text"]

        # Build a list of source metadata
        sources = [
            {
                "file": result.payload["file"],   # PDF file name
                "page": result.payload["page"],   # Page number
                "score": result.score,            # Similarity score
            }
            for result in top_results
        ]

        # Return the final response
        return {
            "answer": answer,
            "sources": sources,
            "screenshot": str(screenshot_path),
        }
