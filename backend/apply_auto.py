from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def find_website_elements(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    elements = driver.find_elements(By.TAG_NAME, 'input')
    print("Found input elements:")
    for element in elements:
        print(f"Aria-Label: {element.get_attribute('aria-label')}")
        print(f"ID: {element.get_attribute('id')}")
        print(f"Class: {element.get_attribute('class')}")
        print("---")

def auto_apply(url, info):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    
    # Wait for page to load
    time.sleep(5)
    
    # Common field identifiers using aria-labels
    field_selectors = {
        'first_name': [
            {'by': By.XPATH, 'value': "//input[@aria-label='First Name']"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'first name')]"},
            {'by': By.ID, 'value': 'first_name'},  # fallback to ID
        ],
        'last_name': [
            {'by': By.XPATH, 'value': "//input[@aria-label='Last Name']"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'last name')]"},
            {'by': By.ID, 'value': 'last_name'},  # fallback to ID
        ],
        'email': [
            {'by': By.XPATH, 'value': "//input[@aria-label='Email']"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'email')]"},
            {'by': By.XPATH, 'value': "//input[@type='email']"},  # fallback to type
        ],
        'phone': [
            {'by': By.XPATH, 'value': "//input[@aria-label='Phone']"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'phone')]"},
            {'by': By.ID, 'value': 'phone'},  # fallback to ID
        ],
        'github': [
            {'by': By.XPATH, 'value': "//input[contains(@aria-label='GitHub')]"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'github')]"},
            {'by': By.ID, 'value': 'github'},  # fallback to ID
        ]
    }
    
    # Try different selectors for each field
    for field, selectors in field_selectors.items():
        for selector in selectors:
            try:
                element = driver.find_element(selector['by'], selector['value'])
                element.send_keys(info[field])
                print(f"Found and filled {field} using {selector}")
                break
            except Exception as e:
                continue
    
    # Keep browser open to verify
    time.sleep(30)
    driver.quit()

if __name__ == "__main__":

    test_url = "https://job-boards.greenhouse.io/perpay/jobs/4034578007?grnh=4b81b4407us"
    info = {
        "first_name": "Felicia",
        "last_name": "Feng",
        "email": "ffeng2003@gmail.com",
        "phone": "530-761-6869",
        "github": "felfeng",
    }
    find_website_elements(test_url)
    auto_apply(test_url, info)