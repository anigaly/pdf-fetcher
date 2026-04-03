import requests
import pandas as pd
import logging
import time
from pathlib import Path


class ClinrecDownloader:
    def __init__(
        self,
        excel_url: str,
        pdf_base_url: str,
        headers: dict,
        output_dir: Path,
        excel_file: str,
        id_column: str = "ID"
    ):
        self.excel_url = excel_url
        self.pdf_base_url = pdf_base_url
        self.headers = headers

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.excel_path = self.output_dir / excel_file
        self.id_column = id_column

    def download_excel(self):
        logging.info("Downloading Excel file")

        response = requests.get(
            self.excel_url,
            headers=self.headers,
            timeout=(3, 10)
        )

        if response.status_code == 200 and len(response.content) > 1000:
            with open(self.excel_path, "wb") as f:
                f.write(response.content)
            logging.info("Excel downloaded successfully")
        else:
            logging.error(f"Failed to download Excel: {response.status_code}")
            raise RuntimeError("Excel download failed")

    def get_ids(self):
        logging.info("Reading Excel file")

        df = pd.read_excel(self.excel_path)
        logging.info(f"Columns found: {list(df.columns)}")

        if self.id_column not in df.columns:
            raise ValueError(f"Column '{self.id_column}' not found")

        ids = df[self.id_column].astype(str).tolist()
        logging.info(f"Total IDs: {len(ids)}")

        return ids

    def download_by_id(self, file_id: str):
        url = self.pdf_base_url + file_id

        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=(3, 5)
            )

            if response.status_code == 200 and len(response.content) > 1000:
                file_path = self.output_dir / f"{file_id}.pdf"

                with open(file_path, "wb") as f:
                    f.write(response.content)

                logging.info(f"Downloaded {file_id}")
            else:
                logging.warning(f"Failed to download {file_id}")

        except Exception as e:
            logging.error(f"Error downloading {file_id}: {e}")

    def download_all(self):
        self.download_excel()
        ids = self.get_ids()

        for file_id in ids:
            self.download_by_id(file_id)
            time.sleep(0.5)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    EXCEL_URL = "https://apicr.minzdrav.gov.ru/api.ashx?op=GetJsonClinrecsFilterV2Excel"

    PDF_BASE_URL = "https://apicr.minzdrav.gov.ru/api.ashx?op=GetClinrecPdf&id="

    HEADERS = {
        "User-Agent": "Mozilla/5.0"
    }

    downloader = ClinrecDownloader(
        excel_url=EXCEL_URL,
        pdf_base_url=PDF_BASE_URL,
        headers=HEADERS,
        output_dir=Path("data"),
        excel_file="data.xlsx",
        id_column="ID"
    )

    downloader.download_all()