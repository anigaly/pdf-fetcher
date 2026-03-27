from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

# 📁 քո download folder-ը
DOWNLOAD_DIR = r"C:\Users\YourName\Downloads"

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": DOWNLOAD_DIR}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.get("https://cr.minzdrav.gov.ru/clin-rec")

wait = WebDriverWait(driver, 20)

try:
    # 🔽 սեղմում ենք "Скачать"
    download_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Скачать')]")
        )
    )
    download_button.click()

    print("Downloading file...")

    # ⏳ սպասում ենք մինչև ֆայլը ներբեռնվի
    time.sleep(5)  # կարող ես մեծացնել եթե պետք լինի

finally:
    driver.quit()

# 📂 գտնում ենք վերջին ներբեռնված Excel ֆայլը
files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".xlsx")]
latest_file = max([os.path.join(DOWNLOAD_DIR, f) for f in files], key=os.path.getctime)

print("File:", latest_file)

# 📊 կարդում ենք Excel-ը
df = pd.read_excel(latest_file)

# 👇 տես column-ները (մեկ անգամ ստուգելու համար)
print(df.columns)

# ⚠️ Փոխիր "ID" ըստ իրական սյունակի անվան
ids = df["ID"]

# 💾 պահում ենք txt
with open("ids.txt", "w", encoding="utf-8") as f:
    for i in ids:
        f.write(str(i) + "\n")

print("DONE ✅")