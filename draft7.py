import requests

LIST_URL = "https://apicr.minzdrav.gov.ru/api.ashx?op=GetClinrecList"
PDF_URL = "https://apicr.minzdrav.gov.ru/api.ashx?op=GetClinrecPdf&id="

data = requests.get(LIST_URL).json()

for item in data:
    file_id = item["id"]

    try:
        r = requests.get(PDF_URL + file_id)

        if r.status_code == 200:
            with open(f"data/{file_id}.pdf", "wb") as f:
                f.write(r.content)

            print("✔", file_id)

    except Exception as e:
        print("❌", file_id, e)