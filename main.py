import requests
import pandas as pd


class ClinrecService:
    BASE_URL = "https://apicr.minzdrav.gov.ru/api.ashx"

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
            "Referer": "https://cr.minzdrav.gov.ru/clin-rec"
        }

    def download_excel(self):
        url = f"{self.BASE_URL}?op=GetJsonClinrecsFilterV2Excel"
        response = requests.get(url, headers=self.headers)

        with open("data.xlsx", "wb") as f:
            f.write(response.content)

        print("Excel downloaded ✅")

    def get_ids_from_excel(self):
        df = pd.read_excel("data.xlsx")

        print(df.columns)  # տես՝ որ սյունակն է id

        ids = df["id"].dropna().astype(str).tolist()
        return ids

    def download_by_id(self, file_id):
        url = f"{self.BASE_URL}?op=GetClinrecPdf&id={file_id}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                with open(f"{file_id}.pdf", "wb") as f:
                    f.write(response.content)

                print(f"Downloaded: {file_id}")
            else:
                print(f"Failed: {file_id}")

        except Exception as e:
            print(f"Error with {file_id}: {e}")

    def download_all(self, ids):
        for file_id in ids:
            self.download_by_id(file_id)


# ▶️ run
service = ClinrecService()

service.download_excel()

ids = service.get_ids_from_excel()

service.download_all(ids)