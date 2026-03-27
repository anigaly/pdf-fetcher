import pandas as pd
import requests
import os

df = pd.read_excel('file.xlsx')

PDF_URL = "https://apicr.minzdrav.gov.ru/api.ashx?op=GetClinrecPdf&id="

# 📁 folder ստեղծում
os.makedirs("data", exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://cr.minzdrav.gov.ru/"
}

for file_id in df['ID']:
    try:
        url = PDF_URL + str(file_id)

        r = requests.get(url, headers=headers, timeout=20)

        if r.status_code == 200 and r.content:
            with open(f"data/{file_id}.pdf", "wb") as f:
                f.write(r.content)

            print(f"✅ Downloaded {file_id}")
        else:
            print(f"⚠️ Failed {file_id}")

    except Exception as e:
        print(f"❌ Error {file_id} → {e}")