from pathlib import Path
import fitz


def save_page_screenshot(pdf_path: Path, page_number: int, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    page = doc[page_number - 1]

    pix = page.get_pixmap(dpi=200)
    pix.save(output_path)

    return output_path
