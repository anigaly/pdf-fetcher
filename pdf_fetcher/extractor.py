from pathlib import Path
import fitz


def clean_text(text: str) -> str:
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()


        if not line:
            continue


        if line.isdigit():
            continue


        if len(line) < 5:
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def extract_pages(pdf_path: Path) -> list[dict]:
    doc = fitz.open(pdf_path)
    pages = []

    for page_index, page in enumerate(doc):
        text = page.get_text()


        text = clean_text(text)


        if len(text.strip()) < 100:
            continue

        pages.append(
            {
                "file": pdf_path.name,
                "path": str(pdf_path),
                "page": page_index + 1,
                "text": text,
            }
        )

    return pages


def split_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        chunk = text[start:start + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def extract_chunks_from_pdf(pdf_path: Path) -> list[dict]:
    pages = extract_pages(pdf_path)
    chunks = []

    for page in pages:
        for index, chunk_text in enumerate(split_text(page["text"])):


            if len(chunk_text.split()) < 20:
                continue

            chunks.append(
                {
                    "text": chunk_text,
                    "file": page["file"],
                    "path": page["path"],
                    "page": page["page"],
                    "chunk_index": index,
                }
            )

    return chunks
