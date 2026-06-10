from pathlib import Path
import pandas as pd


def get_allowed_pdf_files(excel_path: Path) -> set[str]:
    df = pd.read_excel(excel_path)


    search_text = df["Наименование"].astype(str)

    keywords = [
        "акушер",
        "беремен",
        "роды",
        "гинек",
        "плод",
        "новорожден",
        "перинат",
    ]

    mask = search_text.str.contains(
        "|".join(keywords),
        case=False,
        na=False,
        regex=True,
    )

    filtered = df[mask]

    allowed_files = set(
        filtered["ID"].astype(str).str.strip() + ".pdf"
    )

    print(f"Allowed files: {len(allowed_files)}")

    return allowed_files
