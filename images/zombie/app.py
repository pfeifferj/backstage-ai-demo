import time
import random
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.binary_location = "/usr/bin/google-chrome"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def navigate_to_website(url):
    driver.get(url)

def click_random_button():
    buttons = driver.find_elements(By.TAG_NAME, "button")
    if buttons:
        random.choice(buttons).click()

def fill_random_text_field():
    text_fields = driver.find_elements(By.TAG_NAME, "input")
    if text_fields:
        field = random.choice(text_fields)
        field.send_keys("Random Text" + Keys.RETURN)

def navigate_random_link():
    links = driver.find_elements(By.TAG_NAME, "a")
    if links:
        random.choice(links).click()

actions = [click_random_button, fill_random_text_field, navigate_random_link]

def perform_random_actions(url, action_count=10):
    navigate_to_website(url)
    for _ in range(action_count):
        random.choice(actions)()
        time.sleep(2)  # Wait for 2 seconds between actions

if __name__ == "__main__":
    perform_random_actions(os.getenv('URL', 'example.com'), 20)
