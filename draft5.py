import pandas as pd

df = pd.read_excel('file.xlsx')

print(df.columns)

BASE_URL = "https://cr.minzdrav.gov.ru/preview-cr/"

for file_id in df['ID']:
    current_url = f"{BASE_URL}{str(file_id)}"
    print(current_url)