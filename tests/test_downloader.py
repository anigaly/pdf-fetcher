import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import pandas as pd

from main import ClinrecDownloader


@pytest.fixture
def downloader(tmp_path):
    return ClinrecDownloader(
        excel_url="https://apicr.minzdrav.gov.ru/api.ashx?op=GetJsonClinrecsFilterV2Excel",
        pdf_base_url="https://apicr.minzdrav.gov.ru/api.ashx?op=GetClinrecPdf&id=",
        headers={},
        output_dir=tmp_path,
        excel_file="test.xlsx",
        id_column="ID",
        delay=0
    )


@patch("main.requests.get")
def test_download_excel_success(mock_get, downloader):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"data"

    mock_get.return_value = mock_response

    downloader.download_excel()

    assert downloader.excel_path.exists()