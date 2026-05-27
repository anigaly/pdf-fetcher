from pathlib import Path
import re
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_document_text(pdf_path: Path) -> str:
    """
    Extract raw text from all pages of a PDF document.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Combined text from all pages as a single string.
    """
    doc = fitz.open(pdf_path)
    pages = []

    for page in doc:
        pages.append(page.get_text("text"))

    return "\n".join(pages)


def remove_unwanted_sections(text: str) -> str:
    """
    Remove bibliography, references, and author-related sections
    from the extracted document text.

    Args:
        text: Raw document text.

    Returns:
        Text with unwanted sections removed.
    """
    patterns = [
        # Remove bibliography and references sections
        r"(?is)^\s*(список литературы|литература|библиографический список|references)\s*\n.*?(?=^\s*приложение\s+[А-ЯA-Z0-9]|$)",
        # Remove author appendix (Appendix A1)
        r"(?is)^\s*приложение\s+А1\..*?(?=^\s*приложение\s+[А-ЯA-Z0-9]|$)",
        # Remove standalone author headings
        r"(?is)^\s*(список авторов|авторы|состав рабочей группы).*$",
    ]

    for pattern in patterns:
        text = re.sub(
            pattern,
            " ",
            text,
            flags=re.MULTILINE,
        )

    return text


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing metadata, citations,
    page numbers, and extra whitespace.

    Args:
        text: Document text.

    Returns:
        Normalized and cleaned text.
    """
    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+", " ", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove citation references such as [12] or [1, 2]
    text = re.sub(r"\[[\d,\s\-–]+\]", " ", text)

    # Remove table of contents section
    text = re.sub(
        r"Оглавление.*?(?=Список сокращений|Термины и определения|1\.\s*Краткая информация)",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Remove standalone page numbers
        if re.fullmatch(r"\d+", line):
            continue

        cleaned_lines.append(line)

    text = " ".join(cleaned_lines)

    # Normalize consecutive whitespace characters
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_text(
    text: str,
    chunk_size: int = 2500,
    overlap: int = 500,
) -> list[str]:
    """
    Split text into overlapping chunks for embedding and retrieval.

    Args:
        text: Input text.
        chunk_size: Maximum chunk size in characters.
        overlap: Number of overlapping characters between chunks.

    Returns:
        List of text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "; ",
            ": ",
            ", ",
            ") ",
            " ",
            "",
        ],
    )

    return splitter.split_text(text)


def extract_chunks_from_pdf(pdf_path: Path) -> list[dict]:
    """
    Extract, clean, and split a PDF document into chunks.

    Processing pipeline:
        1. Extract text from the entire document.
        2. Remove references and author sections.
        3. Clean and normalize text.
        4. Split text into chunks.
        5. Attach metadata to each chunk.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        List of chunk dictionaries containing text and metadata.
    """
    # Extract full document text
    text = extract_document_text(pdf_path)

    # Remove bibliography and author-related sections
    text = remove_unwanted_sections(text)

    # Clean and normalize text
    text = clean_text(text)

    chunks = []

    # Split cleaned text into chunks
    for index, chunk_text in enumerate(split_text(text)):
        chunk_text = chunk_text.strip()

        if not chunk_text:
            continue

        # Skip very small chunks with little semantic value
        if len(chunk_text.split()) < 15:
            continue

        chunks.append(
            {
                "text": chunk_text,
                "file": pdf_path.name,
                "path": str(pdf_path),
                "chunk_index": index,
            }
        )

    return chunks


def get_clean_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from a PDF, remove unwanted sections (bibliography, authors),
    and return a single cleaned and normalized text string without splitting.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Cleaned document text as a single string.
    """
    # 1. Extract the full raw text from the document
    text = extract_document_text(pdf_path)

    # 2. Remove bibliography, TOC, and author-related sections
    text = remove_unwanted_sections(text)

    # 3. Clean text from metadata (URLs, emails, citations) and normalize whitespace
    text = clean_text(text)

    return text
