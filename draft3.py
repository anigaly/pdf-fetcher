from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://cr.minzdrav.gov.ru/clin-rec"

driver = webdriver.Chrome()
driver.get(BASE_URL)

wait = WebDriverWait(driver, 10)

try:
    for page in range(1, 143):

        print(f"\n--- Page {page} ---")

        elements = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "_text_link_1inds_6"))
        )

        for el in elements:
            print(el.text)

        try:
            next_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Следующая страница']"))
            )

            old_element = elements[0]

            next_button.click()

            # սպասում ենք մինչև հինը վերանա
            wait.until(EC.staleness_of(old_element))

        except:
            print("No more pages")
            break

finally:
    driver.quit()
    with open('ids.txt', 'w') as file:
        file.write(str(elements))