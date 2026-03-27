import pandas as pd
import requests

df = pd.read_excel('file.xlsx')

PDF_URL = "https://apicr.minzdrav.gov.ru/api.ashx?op=GetClinrecPdf&id="

for file_id in df['ID']:
    try:
        url = PDF_URL + str(file_id)

        r = requests.get(url, timeout=20)

        if r.status_code == 200:
            with open(f"data/{file_id}.pdf", "wb") as f:
                f.write(r.content)

            print(f"✅ Downloaded {file_id}")
        else:
            print(f"⚠️ Failed {file_id}")

    except Exception as e:
        print(f"❌ Wrong {file_id} → {e}")