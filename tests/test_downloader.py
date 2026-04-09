import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import pandas as pd
import sys

# fix import path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from main import ClinrecDownloader


@pytest.fixture
def downloader(tmp_path):
    return ClinrecDownloader(
        excel_url="https://apicr.minzdrav.gov.ru/api.ashx?op=GetJsonClinrecsFilterV2Excel",
        pdf_base_url="https://apicr.minzdrav.gov.ru/api.ashx?op=GetClinrecPdf&id=",
        headers={},
        output_dir=tmp_path,
        excel_file="excel_file",
        id_column="ID",
        delay=0



    )




# Excel download tests
@patch("main.requests.get")
def test_download_excel_success(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"excel data"

    mock_get.return_value = mock_response

    downloader.download_excel()

    assert downloader.excel_path.exists()


@patch("main.requests.get")
def test_download_excel_fail(mock_get, downloader):
    mock_get.side_effect = Exception("Connection error")

    with pytest.raises(Exception):
        downloader.download_excel()



# get_ids tests
def test_get_ids_success(downloader):
    df = pd.DataFrame({"ID": ["1", "2", "3"]})
    df.to_excel(downloader.excel_path, index=False)

    ids = downloader.get_ids()

    assert ids == ["1", "2", "3"]


def test_get_ids_empty_excel(downloader):
    df = pd.DataFrame({"ID": []})
    df.to_excel(downloader.excel_path, index=False)

    ids = downloader.get_ids()

    assert ids == []


def test_get_ids_numbers(downloader):
    df = pd.DataFrame({"ID": [1, 2, 3]})
    df.to_excel(downloader.excel_path, index=False)

    ids = downloader.get_ids()

    assert ids == ["1", "2", "3"]


def test_get_ids_mixed_types(downloader):
    df = pd.DataFrame({"ID": [1, "2", None]})
    df.to_excel(downloader.excel_path, index=False)

    ids = downloader.get_ids()

    assert "1" in ids
    assert "2" in ids


def test_get_ids_missing_column(downloader):
    df = pd.DataFrame({"WRONG": ["1"]})
    df.to_excel(downloader.excel_path, index=False)

    with pytest.raises(ValueError):
        downloader.get_ids()


# download_by_id tests

@patch("main.requests.get")
def test_download_by_id_success(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"x" * 2000

    mock_get.return_value = mock_response

    downloader.download_by_id("123")

    file_path = downloader.output_dir / "123.pdf"
    assert file_path.exists()


@patch("main.requests.get")
def test_download_by_id_fail(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.content = b""

    mock_get.return_value = mock_response

    downloader.download_by_id("123")

    file_path = downloader.output_dir / "123.pdf"
    assert not file_path.exists()


@patch("main.requests.get")
def test_download_by_id_small_content(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"small"

    mock_get.return_value = mock_response

    downloader.download_by_id("123")

    file_path = downloader.output_dir / "123.pdf"
    assert not file_path.exists()


@patch("main.requests.get")
def test_download_by_id_exception(mock_get, downloader):
    mock_get.side_effect = Exception("Network error")

    downloader.download_by_id("123")

    file_path = downloader.output_dir / "123.pdf"
    assert not file_path.exists()


@patch("main.requests.get")
def test_download_by_id_number(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"x" * 2000

    mock_get.return_value = mock_response

    downloader.download_by_id(123)

    file_path = downloader.output_dir / "123.pdf"
    assert file_path.exists()


def test_download_by_id_empty_string(downloader):
    downloader.download_by_id("")

    file_path = downloader.output_dir / ".pdf"
    assert not file_path.exists()