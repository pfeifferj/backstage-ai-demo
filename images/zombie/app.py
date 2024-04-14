import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

target_website = os.environ.get('URL', 'https://www.example.com')

recorded_actions = [
    # Add recorded actions
    # read from files in dir maybe?
]

def perform_random_click():
    try:
        clickable_elements = driver.find_elements(By.CSS_SELECTOR, 'a, button, input[type="submit"], [onclick]')
        
        if clickable_elements:
            random_element = random.choice(clickable_elements)
            
            random_element.click()
            print(f"Clicked element: {random_element.tag_name}")
        else:
            print("No clickable elements found.")
    except (TimeoutException, NoSuchElementException):
        print("Element not found or timed out.")

def perform_recorded_action(action):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, action['selector']))
        )
        
        if action['type'] == 'click':
            element.click()
            print(f"Performed recorded click action on element: {action['selector']}")
    except (TimeoutException, NoSuchElementException):
        print(f"Element not found or timed out for recorded action: {action['selector']}")

driver.get(target_website)

while True:
    interval = random.uniform(0.1, 2)
    
    if random.random() < 0.5 and recorded_actions:
        random_action = random.choice(recorded_actions)
        perform_recorded_action(random_action)
    else:
        perform_random_click()
    
    time.sleep(interval)