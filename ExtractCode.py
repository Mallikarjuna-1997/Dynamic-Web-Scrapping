import logging
import os
import re
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Edge WebDriver service
service = EdgeService(executable_path=r"C:\Users\prade\OneDrive\Desktop\msedgedriver.exe")
driver = webdriver.Edge(service=service)

# Base URL
base_url = "https://www.maynoothuniversity.ie"

# Accept cookies and maximize window
def setup_browser():
    driver.get(base_url)
    driver.maximize_window()
    try:
        print("Waiting for the cookie consent button")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']"))
        ).click()
        print("Cookie consent button clicked")
    except Exception as e:
        print(f"No cookie button found or error occurred: {e}")

# Remove illegal characters for Excel
def sanitize(text):
    return re.sub(r'[^\x20-\x7E]', '', text)  # Removes non-ASCII characters

results = []
setup_browser()

for page in range(6):  # Assuming there are 6 pages
    page_url = f"{base_url}/people?fields_start_with=&field_organisational_unit_nid=178&page={page}"
    print(f"Opening the page: {page_url}")
    driver.get(page_url)
    time.sleep(2)

    person_links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/people/"]')
    person_urls = list(set(link.get_attribute('href') for link in person_links))

    for person_url in person_urls:
        full_person_url = f"{base_url}{person_url}" if not person_url.startswith(base_url) else person_url
        driver.get(full_person_url)
        time.sleep(5)

        try:
            publications_tab = driver.find_element(By.XPATH, "//li[@class='nav-item']//a[@id='Publications-tab']")
            publications_tab.click()
            time.sleep(5)

            publication_sections = driver.find_elements(By.CLASS_NAME, 'publication-section')
            for section in publication_sections:
                header = sanitize(section.find_element(By.TAG_NAME, 'h3').text)
                rows = section.find_elements(By.TAG_NAME, 'tr')[1:]
                for row in rows:
                    columns = row.find_elements(By.TAG_NAME, 'td')
                    if len(columns) >= 3:
                        year = sanitize(columns[1].text)
                        detail = sanitize(columns[2].text)
                        results.append({'url': full_person_url, 'type': header, 'year': year, 'detail': detail})
        except NoSuchElementException:
            results.append({'url': full_person_url, 'publications': 'Publications tab not found'})

driver.quit()
df = pd.DataFrame(results)
csv_filename = "publications.csv"
excel_filename = "publications.xlsx"
csv_filepath = os.path.join(os.getcwd(), csv_filename)
excel_filepath = os.path.join(os.getcwd(), excel_filename)

df.to_csv(csv_filepath, index=False)
df.to_excel(excel_filepath, index=False)

logging.info(f"Data saved to {csv_filepath} and {excel_filepath}")
