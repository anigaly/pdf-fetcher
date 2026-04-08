import requests
import pandas as pd
import logging
import time
import json
from pathlib import Path


class ClinrecDownloader:
    def __init__(
        self,
        excel_url: str,
        pdf_base_url: str,
        headers: dict,
        output_dir: Path,
        excel_file: str,
        id_column: str = "ID",
        delay: float = 0.5
    ):
        self.excel_url = excel_url
        self.pdf_base_url = pdf_base_url
        self.headers = headers

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.excel_path = self.output_dir / excel_file
        self.id_column = id_column
        self.delay = delay

    def download_excel(self):
        logging.info("Downloading Excel file")

        for attempt in range(3):
            try:
                response = requests.get(
                    self.excel_url,
                    headers=self.headers,
                    timeout=(5, 30)
                )

                if response.status_code == 200:
                    with open(self.excel_path, "wb") as f:
                        f.write(response.content)

                    logging.info("Excel downloaded successfully")
                    return

            except Exception as e:
                logging.warning(f"Attempt {attempt+1} failed: {e}")
                time.sleep(2)

        raise Exception("Excel download failed after retries")

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
                timeout=(5, 30)
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
            time.sleep(self.delay)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    with open("config.json", "r") as f:
        config = json.load(f)

    downloader = ClinrecDownloader(
        excel_url=config["excel_url"],
        pdf_base_url=config["pdf_base_url"],
        headers=config["headers"],
        output_dir=Path(config["output_dir"]),
        excel_file=config["excel_file"],
        id_column=config["id_column"],
        delay=config["delay"]
    )

    downloader.download_all()