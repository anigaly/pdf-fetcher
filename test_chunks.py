import re
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf_fetcher.extractor import extract_document_text, remove_unwanted_sections


# --- FIXED CLEAN TEXT FUNCTION (Retains newlines) ---
def clean_text_keep_newlines(text: str) -> str:
    """
    Cleans the text but keeps normal newlines for readable chunking.
    """
    # Remove URLs and emails
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove citation references like [12] or [1, 2]
    text = re.sub(r"\[[\d,\s\-–]+\]", " ", text)

    # Remove table of contents
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
        # Skip standalone page numbers
        if re.fullmatch(r"\d+", line):
            continue
        cleaned_lines.append(line)

    # CRITICAL FIX: Join with newline '\n' instead of space ' '
    return "\n".join(cleaned_lines)


# --- FIXED SPLITTER (Prioritizes newlines) ---
def split_text_smart(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""],  # Strictly prefers breaking at line ends
    )
    return splitter.split_text(text)


# --- MAIN EXECUTION ---
pdfs = [
    Path("data/pdfs/637_2.pdf"),
    Path("data/pdfs/289_2.pdf"),
    Path("data/pdfs/331_2.pdf"),
]

output_file = Path("readable_chunks.txt")

with open(output_file, "w", encoding="utf-8") as f:
    for pdf_path in pdfs:
        if not pdf_path.exists():
            continue

        print(f"Processing and structural chunking for: {pdf_path.name}")

        # Process pipeline using the modified readable cleaner
        raw_text = extract_document_text(pdf_path)
        no_unwanted = remove_unwanted_sections(raw_text)
        final_clean = clean_text_keep_newlines(no_unwanted)

        # Split into structured chunks
        chunks = split_text_smart(final_clean)

        f.write(f"{'=' * 60}\n")
        f.write(f"FILE: {pdf_path.name} | TOTAL CHUNKS: {len(chunks)}\n")
        f.write(f"{'=' * 60}\n\n")

        for index, chunk_content in enumerate(chunks):
            f.write(f"--- CHUNK {index} ---\n")
            # Write the content as it is, preserving lines
            f.write(chunk_content.strip())
            f.write("\n" + "-" * 40 + "\n\n")

print(f"\nDone! Open '{output_file}' to view visually structured chunks.")
