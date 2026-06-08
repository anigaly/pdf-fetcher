from openai import OpenAI
from pathlib import Path
from config import OPENAI_API_KEY, OPENAI_BASE_URL



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
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
        )

        self.retriever = QdrantRetriever()
        print("Retriever initialized")

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
        context = "\n\n".join(
            result.payload["text"]
            for result in top_results
        )

        # Get payload data from the best result
        best = top_results[0].payload

        # Generate and save a screenshot of the matching PDF page
        screenshot_path = save_page_screenshot(
            pdf_path=Path(best["path"]),  # Full path to the PDF file
            page_number=best.get("page", 0), # If "page" is missing, it defaults to 0 instead of crashing
            output_path=Path("data/screenshots")
            / f"{best['file']}_page_{best['page']}.png",
        )

        prompt = f"""
        You are a medical assistant.

        Answer the user's question using ONLY the provided context.

        If the answer is not found in the context, say so.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        response = self.client.chat.completions.create(
            model="Qwen3.5-35B-A3B",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.1,
        )

        answer = response.choices[0].message.content

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
