from pathlib import Path
from pdf_fetcher.extractor import extract_clean_text



pdf_path = Path("data/pdfs/637_2.pdf")

text = extract_clean_text(pdf_path)

with open(
    "clean_text.txt",
    "w",
    encoding="utf-8",
) as f:
    f.write(text)

print("Saved to clean_text.txt")
