import pandas as pd
import requests
import os
import time


print("=" * 60)
print("📥 PDF DOWNLOADER - AUTO READ FROM EXCEL")
print("=" * 60)


excel_file = "file.xlsx"


if not os.path.exists(excel_file):
    print(f"\n❌ ERROR: '{excel_file}' not found!")
    print(f"📁 Current folder: {os.getcwd()}")
    print("\n📋 Files in current folder:")
    for file in os.listdir():
        print(f"   - {file}")
    exit()

print(f"\n✅ Found Excel file: {excel_file}")


try:
    df = pd.read_excel(excel_file, engine='openpyxl')
    print(f"✅ Successfully read Excel file")
    print(f"📊 Total rows: {len(df)}")
    print(f"📋 Column names: {list(df.columns)}")
except Exception as e:
    print(f"❌ Error reading Excel: {e}")
    exit()


id_column = None
possible_names = ['ID', 'Id', 'id', '№', 'number', 'identifier']

for col in possible_names:
    if col in df.columns:
        id_column = col
        break


if id_column is None:
    print(f"\n⚠️ 'ID' column not found!")
    print(f"📋 Available columns: {list(df.columns)}")
    print(f"💡 Using first column as ID: {df.columns[0]}")
    id_column = df.columns[0]
else:
    print(f"\n✅ Found ID column: {id_column}")


ids = df[id_column].dropna().tolist()
print(f"📋 Total IDs found: {len(ids)}")
print(f"🔑 First 5 IDs: {ids[:5]}")

if len(ids) == 0:
    print("❌ No IDs found in Excel file!")
    exit()


PDF_URL = "https://apicr.minzdrav.gov.ru/api.ashx?op=GetClinrecPdf&id="


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://cr.minzdrav.gov.ru/clin-rec"
}

os.makedirs("data", exist_ok=True)


success = 0
failed = 0
total = len(ids)

print(f"\n🚀 Starting download of {total} PDFs...\n")

for index, file_id in enumerate(ids, 1):
    try:

        file_id = str(file_id).strip()

        if not file_id:
            print(f"⏭️ {index}/{total}: Empty ID, skipping")
            continue


        url = PDF_URL + file_id

        print(f"📥 {index}/{total}: {file_id}...", end=" ")


        response = requests.get(url, headers=headers, timeout=20)


        content_type = response.headers.get("Content-Type", "").lower()

        if response.status_code == 200 and "pdf" in content_type:

            file_path = f"data/{file_id}.pdf"
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"✅ ({len(response.content)} bytes)")
            success += 1
        elif response.status_code == 200:

            print(f"⚠️ HTML response (not PDF)")
            failed += 1
        else:
            print(f"⚠️ HTTP {response.status_code}")
            failed += 1


        time.sleep(0.5)

    except requests.exceptions.Timeout:
        print(f"❌ Timeout")
        failed += 1
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        failed += 1
    except Exception as e:
        print(f"❌ Error: {e}")
        failed += 1


print("\n" + "=" * 60)
print("🎉 DOWNLOAD COMPLETE")
print(f"✅ Successfully downloaded: {success}")
print(f"❌ Failed: {failed}")
print(f"📁 Files saved in: {os.path.abspath('data')}")
print("=" * 60)


if success > 0:
    print("\n📄 Downloaded PDFs:")
    pdf_files = [f for f in os.listdir("data") if f.endswith(".pdf")]
    for f in sorted(pdf_files):
        file_size = os.path.getsize(f"data/{f}")
        print(f"   - {f} ({file_size:,} bytes)")