from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time


# debugginger purposes

def find_website_elements(url):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    
    # Wait for page to load
    time.sleep(5)
    
    try:
        print("\nSearching for dropdown elements:")
        selects = driver.find_elements(By.TAG_NAME, 'select')
        custom_dropdowns = driver.find_elements(By.XPATH, """
            //div[contains(@class, 'dropdown') or 
                contains(@class, 'select') or 
                contains(@role, 'listbox') or 
                .//button[contains(@aria-haspopup, 'true')]]
        """)
        
        if not selects and not custom_dropdowns:
            print("No dropdown elements found")
        else:
            for element in selects:
                try:
                    print(f"aria-Label: {element.get_attribute('aria-label')}")
                    print(f"text: {element.text}") 
                    print(f"id: {element.get_attribute('id')}")
                    select = Select(element)
                    print("Options:", [option.text for option in select.options])
                    print("---")
                except Exception as e:
                    print(f"Error processing traditional dropdown: {str(e)}")
                    continue
            
            for element in custom_dropdowns:
                try:
                    print("\ndropdown")
                    print(f"Aria-Label: {element.get_attribute('aria-label')}")
                    print(f"Text: {element.text}") 
                    print(f"ID: {element.get_attribute('id')}")
                    print(f"Class: {element.get_attribute('class')}")
                    print(f"Role: {element.get_attribute('role')}")
                    # Try to find options if they exist
                    options = element.find_elements(By.XPATH, ".//li | .//div[@role='option']")
                    if options:
                        print("Options:", [opt.text for opt in options])
                    print("---")
                except Exception as e:
                    print(f"Error processing custom dropdown: {str(e)}")
                    continue
        
        # Find input elements
        inputs = driver.find_elements(By.TAG_NAME, 'input')
        print("Found input elements:")
        for element in inputs:
            try:
                print(f"Aria-Label: {element.get_attribute('aria-label')}")
                print(f"ID: {element.get_attribute('id')}")
                print(f"Type: {element.get_attribute('type')}")  
                print("---")
            except Exception as e:
                continue    
    finally:
        driver.quit()

# fill in
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
            {'by': By.ID, 'value': 'last_name'},  
        ],
        'email': [
            {'by': By.XPATH, 'value': "//input[@aria-label='Email']"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'email')]"},
            {'by': By.XPATH, 'value': "//input[@type='email']"},  
        ],
        'phone': [
            {'by': By.XPATH, 'value': "//input[@aria-label='Phone']"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'phone')]"},
            {'by': By.ID, 'value': 'phone'},  
        ],
        'linkedin': [
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'Linkedin')]"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'linkedin')]"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'Profile')]"},
            {'by': By.ID, 'value': 'linkedin'},  
        ],
        'github': [
            {'by': By.XPATH, 'value': "//input[contains(@aria-label='GitHub')]"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label, 'github')]"},
            {'by': By.ID, 'value': 'github'},  
        ],
        'school': [
            {'by': By.XPATH, 'value': "//input[contains(@aria-label='School')]"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label='School')]"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label='University')]"},
            {'by': By.XPATH, 'value': "//input[contains(@aria-label='Attending')]"},
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
    
    # Updated dropdown handling for custom dropdowns
    dropdown_selectors = {
        'degree': [
            {'by': By.XPATH, 'value': "//label[contains(text(), 'degree')]//following::input[1]"},
            {'by': By.XPATH, 'value': "//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'degree')]//following::input[1]"},
            {'by': By.XPATH, 'value': "//input[@id='degree--0']"},
            {'by': By.XPATH, 'value': "//div[contains(@class, 'degree')]//input"},
        ],
        'school': [
            {'by': By.XPATH, 'value': "//label[contains(text(), 'school')]//following::input[1]"},
            {'by': By.XPATH, 'value': "//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'school')]//following::input[1]"},
            {'by': By.XPATH, 'value': "//div[contains(@class, 'school')]//input"},
        ],
        'willyouneedsponsership': [
            {'by': By.XPATH, 'value': "//label[contains(text(), 'sponsor')]//following::input[1]"},
            {'by': By.XPATH, 'value': "//div[contains(text(), 'sponsor')]//following::input[1]"},
            {'by': By.XPATH, 'value': "//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sponsor')]//following::input[1]"},
        ],
        'legal': [
            {'by': By.XPATH, 'value': "//label[contains(text(), 'legal')]//following::input[1]"},
            {'by': By.XPATH, 'value': "//div[contains(text(), 'legal')]//following::input[1]"},
            {'by': By.XPATH, 'value': "//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'legal')]//following::input[1]"},
        ]
    }
    
    # Try different selectors for each dropdown field
    for field, selectors in dropdown_selectors.items():
        for selector in selectors:
            try:
                element = driver.find_element(selector['by'], selector['value'])
                element.send_keys(info[field])  # Just send keys instead of using Select
                print(f"Found and filled dropdown {field} using {selector}")
                element.send_keys(Keys.RETURN)
                break
            except Exception as e:
                continue

    # Keep browser open to verify
    time.sleep(50)
    driver.quit()


def fill_in_resume(r_path):
    driver.

if __name__ == "__main__":

    test_url = "https://job-boards.greenhouse.io/perpay/jobs/4034578007?grnh=4b81b4407us"
    ## essential info
    essential_info = {
        "first_name": "Felicia",
        "last_name": "Feng",
        "email": "ffeng2003@gmail.com",
        "phone": "530-761-6869",
        "linkedin": "https://www.linkedin.com/in/felicia-feng/",
        "school": "University of California - Davis",
        "degree": "Bachelor's Degree",
        "graduation_year": "2025",
        "willyouneedsponsership": "No",
        "legal": "Yes",
    }


    find_website_elements(test_url)
    auto_apply(test_url, essential_info)