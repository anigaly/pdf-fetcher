# Clinrec PDF Downloader

#  Description

This project automatically downloads clinical recommendation PDF files from the Russian Ministry of Health website.

The script:

1. Downloads an Excel file containing all available clinical recommendation IDs
2. Extracts IDs from the Excel file
3. Downloads corresponding PDF files using the API


#  Technologies

* Python 3.10+
* requests
* pandas
* openpyxl


#  How it works

The workflow is fully automated:

1. Excel file is downloaded from API
2. IDs are extracted from the Excel file
3. PDFs are downloaded using these IDs

```
Excel → IDs → PDF files
```

# Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the script

```bash
python main.py
```

---

# Project structure

```
project/
 ├── main.py
 ├── data/        # generated автоматически
 ├── README.md
 └── .gitignore
```

---

# Notes

* Excel and PDF files are **not stored in the repository**
* They are downloaded automatically at runtime
* Make sure you have a stable internet connection



# Configuration

All key parameters are configurable:

* Excel URL
* PDF base URL
* Headers
* Output directory
* Excel file name
* ID column name

These are passed to the class constructor.



# Features

* No hardcoded values inside the class
* Uses `pathlib` for file handling
* Uses `logging` instead of print
* Handles network errors and timeouts
* Retry mechanism for stability


# Example

```python
downloader = ClinrecDownloader(
    excel_url=EXCEL_URL,
    pdf_base_url=PDF_BASE_URL,
    headers=HEADERS,
    output_dir=Path("data"),
    excel_file="data.xlsx",
    id_column="ID"
)

downloader.download_all()
```


