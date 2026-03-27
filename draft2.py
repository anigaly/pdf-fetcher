from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://cr.minzdrav.gov.ru/clin-rec"

driver = webdriver.Chrome()
driver.get(BASE_URL)

wait = WebDriverWait(driver, 15)

try:
    # սպասում ենք մինչև էլեմենտները հայտնվեն
    elements = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "_text_link_1inds_6"))
    )

    print("---- FIRST PAGE DATA ----\n")

    for el in elements:
        print(el.text)

finally:
    driver.quit()