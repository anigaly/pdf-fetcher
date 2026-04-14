from pathlib import Path
import json
import logging
from pdf_fetcher.downloader import ClinrecDownloader

def run():
    logging.basicConfig(level=logging.INFO)

    with open("config.json") as f:
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
