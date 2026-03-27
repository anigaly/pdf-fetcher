from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://cr.minzdrav.gov.ru/clin-rec")

wait = WebDriverWait(driver, 15)

try:
    # սպասում ենք մինչև Download կոճակը երևա
    download_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Скачать')]")
        )
    )

    download_button.click()

    print("Download started")

finally:
    driver.quit()