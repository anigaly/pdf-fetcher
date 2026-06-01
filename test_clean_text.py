from pathlib import Path

from pdf_fetcher.extractor import (
    extract_document_text,
    remove_unwanted_sections,
)

# Define the paths to the source PDF files
pdfs = [
    Path("data/pdfs/637_2.pdf"),
    Path("data/pdfs/289_2.pdf"),
    Path("data/pdfs/331_2.pdf"),
]

# Define the output file path (will be created in the root directory)
output_file = Path("clean_text.txt")

# Open the file in write mode with UTF-8 encoding for proper Cyrillic support
with open(output_file, "w", encoding="utf-8") as f:

    for pdf_path in pdfs:
        print(f"\n{'=' * 50}")
        print(f"Processing: {pdf_path.name}")

        # Extract and clean text from the current PDF
        text = extract_document_text(pdf_path)
        cleaned = remove_unwanted_sections(text)

        # Print a short preview of the cleaned text to the console
        print("\n--- CLEANED TEXT PREVIEW ---")
        print(cleaned[:500] + "\n...")
        print("----------------------------\n")

        # Validation checks for specific sections
        checks = [
            "список литературы",
            "литература",
            "references",
            "список авторов",
            "состав рабочей группы",
            "приложение а1",
        ]

        for item in checks:
            found = item in cleaned.lower()
            print(f"{item}: {'FOUND' if found else 'REMOVED'}")

        # Write the file header and the cleaned text into the combined file
        f.write(f"=== FILE: {pdf_path.name} ===\n\n")
        f.write(cleaned)
        f.write("\n\n" + "="*50 + "\n\n")  # Section separator

print(f"\nSuccess! All cleaned texts have been saved to '{output_file}'")
