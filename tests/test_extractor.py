from pathlib import Path

from pdf_fetcher.extractor import (
    remove_unwanted_sections,
    clean_text,
    extract_pages,
    split_text,
    extract_chunks_from_pdf,
)


# -------------------------
# remove_unwanted_sections
# -------------------------

def test_remove_references_section():
    text = """
    This is normal text

    REFERENCES
    some reference text
    """

    cleaned = remove_unwanted_sections(text)

    assert "reference text" not in cleaned.lower()


def test_remove_authors_section():
    text = """
    Normal text

    СПИСОК АВТОРОВ
    Ivan Ivanov
    Petr Petrov
    """

    cleaned = remove_unwanted_sections(text)

    assert "Ivan Ivanov" not in cleaned


# -------------------------
# clean_text
# -------------------------

def test_clean_text_removes_urls():
    text = "Text with url https://example.com"

    cleaned = clean_text(text)

    assert "https://example.com" not in cleaned


def test_clean_text_removes_emails():
    text = "email test@test.com"

    cleaned = clean_text(text)

    assert "test@test.com" not in cleaned


def test_clean_text_removes_references():
    text = "Some text [12]"

    cleaned = clean_text(text)

    assert "[12]" not in cleaned


def test_clean_text_removes_page_numbers():
    text = """
    12

    This is text
    """

    cleaned = clean_text(text)

    assert cleaned == "This is text"


def test_clean_text_returns_string():
    text = "normal text"

    cleaned = clean_text(text)

    assert isinstance(cleaned, str)


# -------------------------
# split_text
# -------------------------

def test_split_text_returns_list():
    text = "This is a very long text. " * 200

    chunks = split_text(text)

    assert isinstance(chunks, list)


def test_split_text_creates_multiple_chunks():
    text = "This is a very long text. " * 500

    chunks = split_text(text)

    assert len(chunks) > 1


def test_split_text_chunks_are_strings():
    text = "This is a very long text. " * 200

    chunks = split_text(text)

    assert isinstance(chunks[0], str)


# -------------------------
# extract_pages
# -------------------------

def test_extract_pages_returns_list():
    pdf_path = Path("data/pdfs/637_2.pdf")

    pages = extract_pages(pdf_path)

    assert isinstance(pages, list)


def test_extract_pages_not_empty():
    pdf_path = Path("data/pdfs/637_2.pdf")

    pages = extract_pages(pdf_path)

    assert len(pages) > 0


def test_extract_pages_has_required_fields():
    pdf_path = Path("data/pdfs/637_2.pdf")

    pages = extract_pages(pdf_path)

    first_page = pages[0]

    assert "file" in first_page
    assert "path" in first_page
    assert "page" in first_page
    assert "text" in first_page


# -------------------------
# extract_chunks_from_pdf
# -------------------------

def test_extract_chunks_from_pdf_returns_chunks():
    pdf_path = Path("data/pdfs/637_2.pdf")

    chunks = extract_chunks_from_pdf(pdf_path)

    assert isinstance(chunks, list)
    assert len(chunks) > 0


def test_chunk_has_required_fields():
    pdf_path = Path("data/pdfs/637_2.pdf")

    chunks = extract_chunks_from_pdf(pdf_path)

    first_chunk = chunks[0]

    assert "text" in first_chunk
    assert "file" in first_chunk
    assert "path" in first_chunk
    assert "page" in first_chunk
    assert "chunk_index" in first_chunk


def test_chunk_text_is_not_empty():
    pdf_path = Path("data/pdfs/637_2.pdf")

    chunks = extract_chunks_from_pdf(pdf_path)

    assert chunks[0]["text"].strip() != ""


def test_chunk_text_has_minimum_words():
    pdf_path = Path("data/pdfs/637_2.pdf")

    chunks = extract_chunks_from_pdf(pdf_path)

    assert len(chunks[0]["text"].split()) >= 15
