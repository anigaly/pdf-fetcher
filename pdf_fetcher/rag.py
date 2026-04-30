from pathlib import Path

from pdf_fetcher.retriever import QdrantRetriever
from pdf_fetcher.screenshot import save_page_screenshot


class PDFRAG:
    def __init__(self):
        self.retriever = QdrantRetriever()

    def ask(self, question: str) -> dict:
        results = self.retriever.search(question, limit=3)

        if not results:
            return {
                "answer": "Պատասխան չգտնվեց։",
                "sources": [],
                "screenshot": None,

            }

        best = results[0].payload

        screenshot_path = save_page_screenshot(
            pdf_path=Path(best["path"]),
            page_number=best["page"],
            output_path=Path("data/screenshots") / f"{best['file']}_page_{best['page']}.png",
        )

        answer = "\n\n".join(
            result.payload["text"]
            for result in results
        )

        return {
            "answer": answer,
            "sources": [
                {
                    "file": result.payload["file"],
                    "page": result.payload["page"],
                    "score": result.score,
                }
                for result in results
            ],
            "screenshot": str(screenshot_path),
        }
