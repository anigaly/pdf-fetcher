from pathlib import Path
import re
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter

def remove_unwanted_sections(text: str) -> str:

    patterns = [

        # Remove references / bibliography sections
        r"(?is)^\s*(список литературы|литература|библиографический список|references)\s*\n.*?(?=^\s*приложение\s+[А-ЯA-Z0-9]|$)",

        # Remove authors / working group appendix
        r"(?is)^\s*приложение\s+А1\..*?(?=^\s*приложение\s+[А-ЯA-Z0-9]|$)",

        # Remove standalone author sections
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


    # URLs
    text = re.sub(r"http\S+|www\.\S+", " ", text)

    # emails
    text = re.sub(r"\S+@\S+", " ", text)

    # references [12]
    text = re.sub(r"\[[\d,\s\-–]+\]", " ", text)

    # remove TOC
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
        # remove pure page numbers
        if re.fullmatch(r"\d+", line):
            continue

        cleaned_lines.append(line)

    text = " ".join(cleaned_lines)
    text = re.sub(r"\s+", " ", text)

    return text.strip()



def extract_pages(pdf_path: Path) -> list[dict]:
    doc = fitz.open(pdf_path)

    pages = []

    for page_index, page in enumerate(doc):

        text = page.get_text("text")

        text = remove_unwanted_sections(text)
        text = clean_text(text)

        if not text:
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

def split_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[str]:

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

    pages = extract_pages(pdf_path)

    chunks = []

    for page in pages:

        for index, chunk_text in enumerate(split_text(page["text"])):

            chunk_text = chunk_text.strip()

            if not chunk_text:
                continue

            # skip very tiny chunks
            if len(chunk_text.split()) < 15:
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
