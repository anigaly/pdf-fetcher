import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pdf_fetcher.extractor import extract_chunks_from_pdf


# Path to test PDF document
pdf_path = Path("data/pdfs/637_2.pdf")


# Extract chunks from PDF
chunks = extract_chunks_from_pdf(pdf_path)


# Print total number of extracted chunks
print("Total chunks:", len(chunks))


# Check if any chunks were extracted
if chunks:
    print("\nFIRST CHUNK:\n")

    # Print first 1000 characters of the first chunk
    print(chunks[0]["text"][:1000])

else:
    print("No chunks extracted")
