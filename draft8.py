import requests

url = "https://apicr.minzdrav.gov.ru/api.ashx?op=GetJsonClinrecsFilterV2Excel"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Referer": "https://cr.minzdrav.gov.ru/clin-rec"
}

response = requests.get(url, headers=headers)

with open("data.xlsx", "wb") as f:
    f.write(response.content)

print("Downloaded ✅")